
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgFoto_ui import Ui_Form
from AutomagicallyUpdater import *
from Utils import TemporaryFile

class WdgFoto(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "FOTO_GEOREF")
		self.setupUi(self)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_FRONTE_EDIFICIOID: AutomagicallyUpdater.ZZTable( "ZZ_FRONTE_EDIFICIO" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			(self.GEOREF_EPSG3003_X, AutomagicallyUpdater.OPTIONAL), 
			(self.GEOREF_EPSG3003_Y, AutomagicallyUpdater.OPTIONAL), 
			(self.GEOREF_EPSG4326_X, AutomagicallyUpdater.OPTIONAL), 
			(self.GEOREF_EPSG4326_X2, AutomagicallyUpdater.OPTIONAL), 
			(self.FILENAME, AutomagicallyUpdater.OPTIONAL), 
			(self.ANNOTAZIONE, AutomagicallyUpdater.OPTIONAL), 
			(self.IMAGE, AutomagicallyUpdater.OPTIONAL), 
			self.ZZ_FRONTE_EDIFICIOID
		]
		self.setupValuesUpdater(childrenList)

		self.connect(self.IMAGE, SIGNAL( "openPicRequested" ), self.apriFoto)


	def caricaImmagine(self, filename):
		rl = qgis.core.QgsRasterLayer( filename )
		if not rl.isValid():
			return False

		# TODO: recupera georef info
		metadata = rl.metadata()

		GPSmetadata = { "EXIF_GPSLatitude" : None, "EXIF_GPSLongitude" : None, "EXIF_GPSAltitude" : None }
		for k in GPSmetadata.keys():
			# e.g. EXIF_GPSLatitude=(46) (42.5) (0)</p>
			rx = QRegExp( "%s=\((\d+(?:\.\d+)?)\) ?(?:\((\d+(?:\.\d+)?)\) ?(?:\((\d+(?:\.\d+)?)\)))</p>" % k )
			pos = rx.indexIn(metadata, 0)
			if pos != -1 and rx.pos(1) != -1:
				value = float(rx.cap(1))
				if rx.pos(2) != -1:
					value = value + float(rx.cap(2))/60
				if rx.pos(3) != -1:
					value = value + float(rx.cap(3))/60/60

				GPSmetadata[k] = value

		longitude = GPSmetadata["EXIF_GPSLongitude"]
		latitude = GPSmetadata["EXIF_GPSLatitude"]
		if latitude != None and longitude != None:
			point4326 = qgis.core.QgsPoint(longitude, latitude)

			self.setValue( self.GEOREF_EPSG4326_X, str(point4326.x()) )
			self.setValue( self.GEOREF_EPSG4326_X2, str(point4326.y()) )

			fromCrs = qgis.core.QgsCoordinateReferenceSystem( 4236, qgis.core.QgsCoordinateReferenceSystem.EpsgCrsId )
			toCrs = qgis.core.QgsCoordinateReferenceSystem( 3003, qgis.core.QgsCoordinateReferenceSystem.EpsgCrsId )
			point3003 = qgis.core.QgsCoordinateTransform( fromCrs, toCrs ).transform( point4326 )
		
			self.setValue( self.GEOREF_EPSG3003_X, str(point3003.x()) )
			self.setValue( self.GEOREF_EPSG3003_Y, str(point3003.y()) )

		self.setValue(self.FILENAME, filename)
		self.setValue(self.IMAGE, filename)	# mostra la preview

		return True

	def getValue(self, widget):
		if self._getRealWidget(widget) != self.IMAGE or self._ID == None:
			return MappingOne2One.getValue(widget)

		return AutomagicallyUpdater.Query( "SELECT IMAGE FROM FOTO_GEOREF WHERE ID = ?", [self._ID] ).getFirstResult()


	def setValue(self, widget, value):
		widget = self._getRealWidget(widget)
		MappingOne2One.setValue(widget, value)
		# disabilita il caching se l'immagine è già stata memorizzata sul db
		if widget == self.IMAGE and self._ID != None:
			self.IMAGE.clearCache()

	def salvaFotoSuFile(self, imgData):
		if imgData == None:
			return

		tmp = TemporaryFile.getNewFile( 'SchedaEdificio' )
		if not tmp.open():
			TemporaryFile.delFile( tmp, 'SchedaEdificio' )
			return

		outfile = open( tmp.fileName().toUtf8(), "wb" )
		outfile.write( str(imgData) )
		outfile.close()

		tmp.close()
		return tmp.fileName()

	def apriFoto(self):
		filename = self.salvaFotoSuFile( self.getValue(self.IMAGE) )
		if filename == None:
			return False
		url = QUrl.fromLocalFile( filename )
		QDesktopServices.openUrl( url )
		return True


	def _saveValue(self, name2valueDict, table, pk, ID=None):
		# non aggiornare le immagini per evitare overhead inutile: 
		# la GUI non permette di cambiare l'immagine salvata, l'unico modo è 
		# creare una nuova immagine ed eliminare quella vecchia
		if ID != None and name2valueDict.has_key( self.IMAGE.objectName() ):
			del name2valueDict[ self.IMAGE.objectName() ]
		return AutomagicallyUpdater._saveValue(name2valueDict, table, pk, ID)


	def toHtml(self, index):
		filename = self.salvaFotoSuFile( self.getValue(self.IMAGE) )
		fronte_edificio = self.ZZ_FRONTE_EDIFICIOID.currentText() if self.getValue(self.ZZ_FRONTE_EDIFICIOID) >= 0 else ''
		annotazione = self.getValue(self.ANNOTAZIONE)

		georef_x = self.getValue(self.GEOREF_EPSG3003_X)
		georef_y = self.getValue(self.GEOREF_EPSG3003_Y)
		georef = '%s , %s' % ( str(georef_x), str(georef_y) ) if georef_x != None and georef_y != None else ''
		
		return """
<table class="border %s">
	<tr>
		<td>Foto #%d</td><td class="value">%s</td>
	</tr>
	<tr>
		<td colspan="2"><img class="foto border" src="%s" alt="foto"></td>
	</tr>
	<tr>
		<td>Coordinate EPSG:3003</td><td class="value">%s</td>
	</tr>
	<tr>
		<td>Annotazioni</td><td class="value">%s</td>
	</tr>
</table>
""" % ( 'newPage' if index > 0 and index%2 == 0 else '', index+1, fronte_edificio, filename, georef, annotazione if annotazione != None else '' )

