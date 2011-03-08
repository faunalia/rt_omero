
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgFoto_ui import Ui_Form
from AutomagicallyUpdater import *

class WdgFoto(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "FOTO_GEOREF")
		self.setupUi(self)

		self.imageBytes = None

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

	def delete(self):
		self.imageBytes = None
		return MappingOne2One.delete(self)


	def setValue(self, widget, valueOld):
		widget = self._getRealWidget(widget)
		value = self._getRealValue(valueOld)

		if widget == self.IMAGE:
			if isinstance(value, str) or isinstance(value, QString):
				infile = open( unicode(value).encode('utf8'), "rb" )
				self.imageBytes = QByteArray( infile.read() )
				infile.close()

			elif isinstance(value, QByteArray):
				self.imageBytes = value

			image = QPixmap()
			if image.loadFromData( self.imageBytes ):
				value = image.scaled( widget.width()-10, widget.height()-10, Qt.KeepAspectRatio )

		AutomagicallyUpdater.setValue(widget, value)

	def getValue(self, widget):
		widget = self._getRealWidget(widget)

		if widget == self.IMAGE:
			return self._getRealValue( self.imageBytes )
		return AutomagicallyUpdater.getValue(widget)

	def toHtml(self, index):
		annotazione = self.getValue(self.ANNOTAZIONE)
		return """
<table class="border">
	<tr>
		<td>Foto #%d</td><td class="value">%s</td>
	</tr>
	<tr>
		<td colspan="2"><img class="border" src="%s" alt="foto"></td>
	</tr>
	<tr>
		<td colspan="2" class="value">%s</td>
	</tr>
	<tr>
		<td>Annotazioni</td><td class="value">%s</td>
	</tr>
</table>
""" % ( index+1, self.ZZ_FRONTE_EDIFICIOID.currentText(), "foto.jpg", self.getValue(self.FILENAME), annotazione if annotazione != None else '' )

