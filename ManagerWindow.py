# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : Omero RT
Description          : Omero plugin
Date                 : August 15, 2010 
copyright            : (C) 2010 by Giuseppe Sucameli (Faunalia)
email                : sucameli@faunalia.it
 ***************************************************************************/

Omero plugin
Works done from Faunalia (http://www.faunalia.it) with funding from Regione 
Toscana - S.I.T.A. (http://www.regione.toscana.it/territorio/cartografia/index.html)

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
import resources

from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import AutomagicallyUpdater
from Utils import *

class ManagerWindow(QDockWidget):

	# nomi tabelle contenenti le geometrie
	TABLE_GEOM_ORIG = "GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZA".lower()
	TABLE_GEOM_MODIF = "GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE".lower()

	# nomi dei layer in TOC
	LAYER_GEOM_ORIG = "Geom. Originali"
	LAYER_GEOM_MODIF = "Geom. Suddivise o Ex-Novo"
	LAYER_FOTO = "Foto Edifici"

	# ID dei layer contenenti geometrie e wms
	VLID_GEOM_ORIG = ''
	VLID_GEOM_MODIF = ''
	VLID_FOTO = ''
	RLID_WMS = {}

	# stile per i layer delle geometrie
	STYLE_PATH = "styles"
	STYLE_GEOM_ORIG = "stile_geometrie_originali.qml"
	STYLE_GEOM_MODIF = "stile_geometrie_modificate.qml"
	STYLE_FOTO = "stile_fotografie.qml"

	SCALE_IDENTIFY = 5000
	SCALE_MODIFY = 2000

	DEFAULT_SRID = 3003

	instance = None
	
	def __init__(self, parent=None, iface=None):
		QDockWidget.__init__(self, parent)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setupUi()

		ManagerWindow.instance = self
		self.iface = iface
		self.canvas = self.iface.mapCanvas()
		self.scheda = None
		self.uvScheda = None
		self.isApriScheda = True
		self.srid = ManagerWindow.DEFAULT_SRID
		self.startedYet = False

		# crea la label da visualizzare nella status bar
		self.status = ManagerWindow.StatusWidget( self.iface.mainWindow().statusBar() )

		MapTool.canvas = self.canvas

		self.nuovaPointEmitter = FeatureFinder()
		self.nuovaPointEmitter.registerStatusMsg( u"Click per identificare la geometria da associare alla nuova scheda" )
		QObject.connect(self.nuovaPointEmitter, SIGNAL("pointEmitted"), self.identificaNuovaScheda)

		self.esistentePointEmitter = FeatureFinder()
		QObject.connect(self.esistentePointEmitter, SIGNAL("pointEmitted"), self.identificaSchedaEsistente)

		self.polygonDrawer = PolygonDrawer()
		self.polygonDrawer.registerStatusMsg( u"Click sx per disegnare la nuova gemetria, click dx per chiuderla" )
		QObject.connect(self.polygonDrawer, SIGNAL("geometryEmitted"), self.creaNuovaGeometria)

		self.lineDrawer = LineDrawer()
		self.lineDrawer.registerStatusMsg( u"Click sx per disegnare la linea di taglio, click dx per chiuderla" )
		QObject.connect(self.lineDrawer, SIGNAL("geometryEmitted"), self.spezzaGeometriaEsistente)

		self.fotoPointEmitter = FeatureFinder()
		self.fotoPointEmitter.registerStatusMsg( u"Click su una foto per visualizzarla" )
		QObject.connect(self.fotoPointEmitter, SIGNAL("pointEmitted"), self.identificaFoto)

		self.connect(self.iface.mapCanvas(), SIGNAL( "mapToolSet(QgsMapTool *)" ), self.toolChanged)

		self.connect(self.btnSelNuovaScheda, SIGNAL("clicked()"), self.identificaNuovaScheda)
		self.connect(self.btnSelSchedaEsistente, SIGNAL("clicked()"), self.apriScheda)
		self.connect(self.btnEliminaScheda, SIGNAL("clicked()"), self.eliminaScheda)
		self.connect(self.btnSpezzaGeometriaEsistente, SIGNAL("clicked()"), self.spezzaGeometriaEsistente)
		self.connect(self.btnCreaNuovaGeometria, SIGNAL("clicked()"), self.creaNuovaGeometria)
		self.connect(self.btnRipulisciGeometrie, SIGNAL("clicked()"), self.ripulisciGeometrie)
		self.connect(self.btnRiepilogoSchede, SIGNAL("clicked()"), self.riepilogoSchede)
		self.connect(self.btnStradario, SIGNAL("clicked()"), self.gestioneStradario)
		self.connect(self.btnSelFoto, SIGNAL("clicked()"), self.identificaFoto)
		self.connect(self.btnAbout, SIGNAL("clicked()"), self.about)

	def setupUi(self):
		self.setObjectName( "rt_omero_dockwidget" )
		self.setWindowTitle( "Omero RT" )

		child = QWidget()
		vLayout = QVBoxLayout( child )


		group = QGroupBox( "Schede edificio", child )
		vLayout.addWidget( group )
		gridLayout = QGridLayout( group )

		text = u"Nuova"
		self.btnSelNuovaScheda = QPushButton( QIcon(":/icons/nuova_scheda.png"), text, group )
		#text = u"Identifica la geometria per la creazione di una nuova scheda edificio"
		text = u"Crea nuova scheda edificio"
		self.btnSelNuovaScheda.setToolTip( text )
		self.btnSelNuovaScheda.setCheckable(True)
		gridLayout.addWidget(self.btnSelNuovaScheda, 0, 0, 1, 1)

		text = u"Modifica"
		self.btnSelSchedaEsistente = QPushButton( QIcon(":/icons/modifica_scheda.png"), text, group )
		#text = u"Identifica la geometria per l'apertura di una scheda già esistente su di essa"
		text = u"Modifica scheda edificio esistente"
		self.btnSelSchedaEsistente.setToolTip( text )
		self.btnSelSchedaEsistente.setCheckable(True)
		gridLayout.addWidget(self.btnSelSchedaEsistente, 0, 1, 1, 1)

		text = u"Elimina"
		self.btnEliminaScheda = QPushButton( QIcon(":/icons/cancella_scheda.png"), text, group )
		text = u"Elimina scheda edificio"
		self.btnEliminaScheda.setToolTip( text )
		self.btnEliminaScheda.setCheckable(True)
		gridLayout.addWidget(self.btnEliminaScheda, 0, 2, 1, 1)

		text = u"Riepilogo schede edificio"
		self.btnRiepilogoSchede = QPushButton( QIcon(":/icons/riepilogo_schede.png"), text, group )
		self.btnRiepilogoSchede.setToolTip( text )
		gridLayout.addWidget(self.btnRiepilogoSchede, 1, 0, 1, 3)


		group = QGroupBox( "Geometrie", child )
		vLayout.addWidget( group )
		gridLayout = QGridLayout( group )

		text = u"Crea nuova"
		self.btnCreaNuovaGeometria = QPushButton( QIcon(":/icons/crea_geometria.png"), text, group )
		text = u"Crea nuova geometria"
		self.btnCreaNuovaGeometria.setToolTip( text )
		self.btnCreaNuovaGeometria.setCheckable(True)
		gridLayout.addWidget(self.btnCreaNuovaGeometria, 0, 0, 1, 1)

		text = u"Suddividi"
		self.btnSpezzaGeometriaEsistente = QPushButton( QIcon(":/icons/spezza_geometria.png"), text, group )
		text = u"Suddividi una geometria"
		self.btnSpezzaGeometriaEsistente.setToolTip( text )
		self.btnSpezzaGeometriaEsistente.setCheckable(True)
		gridLayout.addWidget(self.btnSpezzaGeometriaEsistente, 0, 1, 1, 1)

		text = u"Ripulisci geometrie non associate"
		self.btnRipulisciGeometrie = QPushButton( QIcon(":/icons/ripulisci.png"), text, group )
		self.btnRipulisciGeometrie.setToolTip( text )
		gridLayout.addWidget(self.btnRipulisciGeometrie, 1, 0, 1, 2)


		text = u"Gestione stradario"
		self.btnStradario = QPushButton( QIcon(":/icons/stradario.png"), text, child )
		self.btnStradario.setToolTip( text )
		vLayout.addWidget( self.btnStradario )
		#gridLayout.addWidget(self.btnStradario, 6, 0, 1, 2)

		text = u"Visualizza foto"
		self.btnSelFoto = QPushButton( QIcon(":/icons/foto.png"), text, child )
		self.btnSelFoto.setToolTip( text )
		self.btnSelFoto.setCheckable(True)
		vLayout.addWidget( self.btnSelFoto )
		#gridLayout.addWidget(self.btnSelFoto, 7, 0, 1, 1)

		text = u"About"
		self.btnAbout = QPushButton( QIcon(":/icons/about.png"), text, child )
		self.btnAbout.setToolTip( text )
		vLayout.addWidget( self.btnAbout )
		#gridLayout.addWidget(self.btnAbout, 7, 1, 1, 1)

		self.setWidget(child)

	def about(self):
		from DlgAbout import DlgAbout
		DlgAbout(self).exec_()


	def toolChanged(self, tool):
		self.status.clear()
		if tool == None:
			return

		self.btnSelSchedaEsistente.setChecked( self.isApriScheda and self.esistentePointEmitter.isActive() )
		if self.btnSelSchedaEsistente.isChecked():
			self.status.show( u"Click per identificare la scheda da variare" )

		self.btnEliminaScheda.setChecked( not self.isApriScheda and self.esistentePointEmitter.isActive() )
		if self.btnEliminaScheda.isChecked():
			self.status.show( u"Click per identificare la scheda da eliminare" )

		self.btnSelNuovaScheda.setChecked( self.nuovaPointEmitter.isActive() )
		self.btnCreaNuovaGeometria.setChecked( self.polygonDrawer.isActive() )
		self.btnSpezzaGeometriaEsistente.setChecked( self.lineDrawer.isActive() )
		self.btnSelFoto.setChecked( self.fotoPointEmitter.isActive() )

		# imposta il messaggio di stato dei tool
		for tool, statusMessage in MapTool.registeredToolStatusMsg.iteritems():
			if tool.isActive():
				self.status.show( statusMessage )


	def permettiAzione(self, btn, maxScale):
		if int(self.canvas.scale()) > maxScale:
			QMessageBox.warning( self, "Azione non permessa", u"L'azione \"%s\" è ammessa solo dalla scala 1:%d" % (btn.toolTip(), maxScale) )
			return False
		return True


	def riepilogoSchede(self):
		from DlgRiepilogoSchede import DlgRiepilogoSchede
		return DlgRiepilogoSchede(self).exec_()

	def gestioneStradario(self):
		from DlgStradario import DlgStradario
		return DlgStradario(self).exec_()


	def identificaNuovaScheda(self, point=None, button=None):

		if not self.permettiAzione( self.btnSelNuovaScheda, self.SCALE_IDENTIFY ) or point == None:
			return self.nuovaPointEmitter.startCapture()

		if button != Qt.LeftButton:
			self.btnSelNuovaScheda.setChecked(False)
			return

		layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
		if layerModif == None:
			self.btnSelNuovaScheda.setChecked(False)
			return

		feat = self.nuovaPointEmitter.findAtPoint(layerModif, point)
		if feat != None:
			# controlla se tale geometria ha qualche scheda associata
			codice = feat.attributeMap()[0].toString()
			numUV = AutomagicallyUpdater.Query( "SELECT count(*) FROM SCHEDA_UNITA_VOLUMETRICA WHERE GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW = ?", [codice] ).getFirstResult()
			if int( numUV ) > 0:
				# NO, c'è già una scheda associata
				QMessageBox.warning( self, "RT Omero", "La geometria selezionata appartiene ad un edificio gia' esistente" )
				return self.nuovaPointEmitter.startCapture()

			# OK, non esiste alcuna scheda associata a tale geometria
			# associa la UV a tale geometria
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			self.apriScheda(codice)
			QApplication.restoreOverrideCursor()
			self.btnSelNuovaScheda.setChecked(False)
			return
			
		layerOrig = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_ORIG )
		if layerOrig == None:
			self.btnSelNuovaScheda.setChecked(False)
			return

		feat = self.nuovaPointEmitter.findAtPoint(layerOrig, point)		
		if feat != None:
			uvID = self.copiaGeometria(feat)
			if uvID == None:
				return

			self.apriScheda(uvID)
			QApplication.restoreOverrideCursor()
			self.btnSelNuovaScheda.setChecked(False)
			return

		return self.nuovaPointEmitter.startCapture()


	def identificaSchedaEsistente(self, point=None, button=None):

		def getButton():
			return self.btnSelSchedaEsistente if self.isApriScheda else self.btnEliminaScheda

		if not self.permettiAzione( getButton(), self.SCALE_IDENTIFY ) or point == None:
			return self.esistentePointEmitter.startCapture()

		if button != Qt.LeftButton:
			getButton().setChecked(False)
			return

		layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
		if layerModif == None:
			getButton().setChecked(False)
			return

		feat = self.esistentePointEmitter.findAtPoint(layerModif, point)
		if feat != None:
			# controlla se tale geometria ha qualche scheda associata
			codice = feat.attributeMap()[0].toString()
			numUV = AutomagicallyUpdater.Query( "SELECT count(*) FROM SCHEDA_UNITA_VOLUMETRICA WHERE GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW = ?", [codice] ).getFirstResult()
			if int( numUV ) > 0:
				# OK, c'è già una scheda associata
				codice = feat.attributeMap()[0].toString()
				if self.isApriScheda:
					self.apriScheda( codice )
				else:
					self.eliminaScheda( codice )
				getButton().setChecked(False)
				return

			# NO, non esiste alcuna scheda associata a tale geometria
			QMessageBox.warning( self, "RT Omero", "Non esiste alcun edificio sulla geometria selezionata" )
			return self.esistentePointEmitter.startCapture()

		return self.esistentePointEmitter.startCapture()


	def identificaFoto(self, point=None, button=None):

		if not self.permettiAzione( self.btnSelFoto, self.SCALE_IDENTIFY ) or point == None:
			return self.fotoPointEmitter.startCapture()

		if button != Qt.LeftButton:
			self.btnSelFoto.setChecked(False)
			return

		layerFoto = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_FOTO )
		if layerFoto == None:
			self.btnSelFoto.setChecked(False)
			return

		featIds = self.fotoPointEmitter.findAtPoint(layerFoto, point, False, True)
		if len(featIds) > 0:
			from DlgVisualizzaFoto import DlgVisualizzaFoto
			dlg = DlgVisualizzaFoto(self)
			dlg.exec_( featIds )
			self.btnSelFoto.setChecked(False)
			return

		return self.fotoPointEmitter.startCapture()


	def spezzaGeometriaEsistente(self, line=None):

		def salvaGeometriaSpezzata(codice, stato, wkb):
			if stato != '9':
				# se la geometria iniziale era copiata o spezzata, 
				# crea una nuova geometria spezzata
				newID = AutomagicallyUpdater._insertGeometriaSpezzata( wkb, self.srid, codice )

			else:
				# altrimenti crea una geometria non presente tra le 
				# geometrie originali
				newID = AutomagicallyUpdater._insertGeometriaNuova( wkb, self.srid )

			return newID

		if not self.permettiAzione( self.btnSpezzaGeometriaEsistente, self.SCALE_MODIFY ):
			self.lineDrawer.stopCapture()
			self.btnSpezzaGeometriaEsistente.setChecked(False)
			return
		if line == None:
			return self.lineDrawer.startCapture()

		#TODO: fai qui i test sulla linea

		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# copia le geometrie originali non ancora copiate e che intersecano la linea
			query = ConnectionManager.getNewQuery( AutomagicallyUpdater.EDIT_CONN_TYPE )
			if query == None:
				return False

			query.prepare( "SELECT CODICE, ST_AsText(geometria) FROM GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZA WHERE ST_Intersects(geometria, ST_GeomFromWkb(?, ?)) AND CODICE NOT IN (SELECT GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE)" )
			query.addBindValue( QByteArray(line.asWkb()) )
			query.addBindValue( self.srid )
			if not query.exec_():
				AutomagicallyUpdater._onQueryError( query.lastQuery(), query.lastError().text(), self )
				return False

			featureList = []
			while query.next():
				ID = None
				codice = query.value(0).toString()
				wkt = query.value(1).toString()
				featureList.append( (ID, codice, wkt) )

			for ID, codice, wkt in featureList:
				geom = QgsGeometry.fromWkt( wkt )
				(retval, newGeometries, topologyTestPoints) = geom.splitGeometry( line.asPolyline(), False )
				if retval == 1:	# nessuna spezzatura
					continue

				# copia la geometria nel layer delle geometrie modificate
				ID = AutomagicallyUpdater._insertGeometriaCopiata( codice )
				if ID == None:
					return False

			# recupera le geometrie modificate che intersecano la linea e non hanno scheda abbinata
			query.prepare( "SELECT ID_UV_NEW, GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE, ZZ_STATO_GEOMETRIAID, ST_AsText(geometria) FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE WHERE ST_Intersects(geometria, ST_GeomFromWkb(?, ?)) AND ABBINATO_A_SCHEDA = '0'" )
			query.addBindValue( QByteArray(line.asWkb()) )
			query.addBindValue( self.srid )
			if not query.exec_():
				AutomagicallyUpdater._onQueryError( query.lastQuery(), query.lastError().text(), self )
				return False

			featureList = []
			while query.next():
				ID = query.value(0).toString()
				codice = query.value(1).toString()
				stato = query.value(2).toString()
				wkt = query.value(3).toString()
				featureList.append( (ID, codice, stato, wkt) )

			for ID, codice, stato, wkt in featureList:
				geom = QgsGeometry.fromWkt( wkt )
				(retval, newGeometries, topologyTestPoints) = geom.splitGeometry( line.asPolyline(), False )
				if retval == 1:	# nessuna spezzatura
					continue

				if stato != '9':
					# imposta la geometria iniziale come spezzata
					AutomagicallyUpdater._updateValue( { 'ZZ_STATO_GEOMETRIAID' : '2' }, 'GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE', 'ID_UV_NEW', ID )
				# aggiorna la geometria iniziale con la nuova geometria
				wkb = QByteArray( geom.asWkb() )
				AutomagicallyUpdater._updateGeometria( ID, wkb, self.srid )

				# salva le nuove geometrie create dalla spezzatura
				for geometry in newGeometries:
					newWkb = QByteArray(geometry.asWkb())
					newID = salvaGeometriaSpezzata(codice, stato, newWkb)
					del geometry

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", e.toString())
			return False

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()
			self.btnSpezzaGeometriaEsistente.setChecked(False)

		# aggiorna il layer con le geometrie modificate
		self.aggiornaLayerModif()
		return True

	def creaNuovaGeometria(self, polygon=None):

		if not self.permettiAzione( self.btnCreaNuovaGeometria, self.SCALE_MODIFY ):
			self.polygonDrawer.stopCapture()
			self.btnCreaNuovaGeometria.setChecked(False)
			return
		if polygon == None:
			return self.polygonDrawer.startCapture()

		# TODO: fai qui i test sul poligono

		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# inserisce la nuova geometria nel layer
			wkb = QByteArray(polygon.asWkb())
			if None == AutomagicallyUpdater._insertGeometriaNuova( wkb, self.srid ):
				return False

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", e.toString())
			return False

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()
			self.btnCreaNuovaGeometria.setChecked(False)

		# aggiorna il layer con le geometrie modificate
		self.aggiornaLayerModif()
		return True


	@classmethod
	def copiaGeometria(self, feat):
		if feat == None:
			return

		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# copia la geometria selezionata nel layer delle geometrie nuove o modificate
			codice = feat.attributeMap()[0].toString()
			ID = AutomagicallyUpdater._insertGeometriaCopiata( codice )
			if ID == None:
				return

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(None, "Errore", e.toString())
			return

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

		# aggiorna il layer con le geometrie modificate
		self.aggiornaLayerModif()

		return ID


	def ripulisciGeometrie(self):
		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

			# avvisa l'utente segnalando quante UV si stanno per eliminare
			# quindi chiedi se vuole davvero eliminarle
			numUV = AutomagicallyUpdater.Query( "SELECT count(*) FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE AS gm1 WHERE (gm1.ZZ_STATO_GEOMETRIAID <> '2' /* non spezzate */ AND gm1.ID_UV_NEW NOT IN (SELECT GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW FROM SCHEDA_UNITA_VOLUMETRICA) /* senza scheda associata */ ) OR (gm1.ZZ_STATO_GEOMETRIAID = '2' /* spezzate */ AND 0 = (SELECT count(*) FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE as gm2 JOIN SCHEDA_UNITA_VOLUMETRICA AS uv ON gm2.ID_UV_NEW = uv.GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW WHERE gm1.GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE = gm2.GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE) /* fanno parte dello stesso edificio */ ) /* i cui pezzi sono tutti senza geometria associata */" ).getFirstResult()
		except:
			raise
		finally:
			QApplication.restoreOverrideCursor()

		if numUV == None:
			return

		if int(numUV) <= 0:
			QMessageBox.information(self, "Nessuna geometria trovata", "Non esistono geometrie senza scheda associata." )
			return

		if QMessageBox.Ok != QMessageBox.warning(self, "Eliminazione geometrie non associate", u"Esistono %s geometrie senza alcuna scheda associata. Vuoi eliminarle? L'operazione non è reversibile." % numUV, QMessageBox.Ok|QMessageBox.Cancel ):
			return

		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# eliminazione geometrie non associate ad alcuna scheda: vedi query precedente
			AutomagicallyUpdater._deleteGeometria( None, "ID_UV_NEW IN (SELECT gm1.ID_UV_NEW FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE AS gm1 WHERE (gm1.ZZ_STATO_GEOMETRIAID <> '2' /* non spezzate */ AND gm1.ID_UV_NEW NOT IN (SELECT GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW FROM SCHEDA_UNITA_VOLUMETRICA) /* senza scheda associata */ ) OR (gm1.ZZ_STATO_GEOMETRIAID = '2' AND 0 = (SELECT count(*) FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE as gm2 JOIN SCHEDA_UNITA_VOLUMETRICA AS uv ON gm2.ID_UV_NEW = uv.GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW WHERE gm1.GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE = gm2.GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE)))" )

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", e.toString())
			return

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

		# aggiorna il layer con le geometrie modificate
		self.aggiornaLayerModif()

	def apriScheda(self, uvID=None):
		if uvID == None:
			self.isApriScheda = True
			return self.identificaSchedaEsistente()

		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		self.chiudiSchedaAperta()

		self.uvScheda = uvID
		self.scheda = self.recuperaScheda( uvID )
		if self.scheda._ID == None:
			# imposta la geometria come abbinata a scheda
			try:
				QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
				ConnectionManager.startTransaction()
				self.scheda.save()
				AutomagicallyUpdater._updateValue( { "ABBINATO_A_SCHEDA" : '1' }, "GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE", "ID_UV_NEW", uvID )
			except ConnectionManager.AbortedException, e:
				QMessageBox.critical(self, "Errore", e.toString())
				return

			finally:
				ConnectionManager.endTransaction()
				QApplication.restoreOverrideCursor()
			
		self.scheda.show()
		QApplication.restoreOverrideCursor()
		return True

	def recuperaScheda(self, uvID):
		query = AutomagicallyUpdater.Query( "SELECT SCHEDA_EDIFICIOID FROM SCHEDA_UNITA_VOLUMETRICA WHERE GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW = ?", [ uvID ] )
		schedaID = query.getFirstResult()

		from SchedaEdificio import SchedaEdificio
		return SchedaEdificio(self, schedaID)


	def chiudiSchedaAperta(self):
		if self.scheda != None:
			try:
				self.scheda.close()
			except RuntimeError:
				pass
			self.scheda = None

	def eliminaScheda(self, codice=None):
		if codice == None:
			self.isApriScheda = False
			return self.identificaSchedaEsistente()

		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		# avvisa l'utente segnalando quante UV sono collegate a questa scheda
		# quindi chiedi se vuole davvero eliminare la scheda
		numUV = AutomagicallyUpdater.Query( "SELECT count(*) FROM SCHEDA_UNITA_VOLUMETRICA WHERE SCHEDA_EDIFICIOID IN (SELECT ed.ID FROM SCHEDA_EDIFICIO AS ed JOIN SCHEDA_UNITA_VOLUMETRICA AS uv ON uv.SCHEDA_EDIFICIOID = ed.ID WHERE uv.GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW = ?)", [codice] ).getFirstResult()

		QApplication.restoreOverrideCursor()
		if numUV == None:
			return

		if QMessageBox.Ok != QMessageBox.warning( self, "Eliminazione scheda", u"La scheda ha %s UV associate. Eliminare? L'operazione non è reversibile." % numUV, QMessageBox.Ok|QMessageBox.Cancel ):
			return

		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# elimina la scheda
			scheda = self.recuperaScheda( codice )
			scheda.delete()

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", e.toString())
			return

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

		# aggiorna il layer con le geometrie modificate
		self.aggiornaLayerModif()
		return True

	def selezionaScheda(self, uvID, centra=True):
		if uvID == None:
			return

		layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
		if layerModif == None:
			return

		geomID = AutomagicallyUpdater.Query( "SELECT ROWID FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE WHERE ID_UV_NEW = ?", [uvID] ).getFirstResult()

		if geomID == None:
			layerModif.removeSelection()
			return

		layerModif.removeSelection(False)
		layerModif.select(int(geomID), not centra)
		if centra:
			self.canvas.zoomToSelected( layerModif )

		return True


	def getPathToDB(self, forceDialog=False):
		from DlgSelezionaDB import DlgSelezionaDB

		pathToDB = AutomagicallyUpdater._getPathToDb()
		if pathToDB.isEmpty() or not QFileInfo( pathToDB ).exists():
			if not DlgSelezionaDB( self ).exec_():
				return
			return AutomagicallyUpdater._getPathToDb()

		if forceDialog:
			return DlgSelezionaDB.selezionaDB( self )

		return pathToDB


	def setDBConnection(self):
		path = self.getPathToDB()
		while( path != None ):
			if ConnectionManager.setConnection(path):
				return True

			QMessageBox.critical(self, "RT Omero", "Connessione non riuscita. \nImpossibile collegarsi al database %s" % path )
			path = self.getPathToDB(True)

		return False


	def exec_(self):
		# controlla la presenza della patch per il layer in sola lettura
		if QGis.QGIS_SVN_VERSION < 14451:
			QMessageBox.critical(self, "RT Omero", "E' richiesto l'uso di QGis almeno alla versione 1.6 e alla revisione r14451")
			return

		if not self.setDBConnection():
			return

		AutomagicallyUpdater._reset()

		from DlgSceltaRilevatore import DlgSceltaRilevatore
		if not DlgSceltaRilevatore().exec_():
			if not self.startedYet:
				ConnectionManager.closeConnection()
			return

		self.iface.addDockWidget(Qt.LeftDockWidgetArea, self)

		loadLastExtent = not self.startedYet
		self.startedYet = True

		if not self.loadLayersInCanvas( loadLastExtent ):
			QMessageBox.critical(self, "RT Omero", "Impossibile caricare i layer richiesti dal database selezionato")
			return


	def loadLayersInCanvas(self, reloadExtent=True):
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		# disabilita il rendering
		prevRenderFlag = self.canvas.renderFlag()
		self.canvas.setRenderFlag( False )

		# recupera ed imposta il CRS della canvas
		query = AutomagicallyUpdater.Query( 'SELECT DISTINCT srid FROM geometry_columns' )
		srid = query.getFirstResult()
		try:
			self.srid = int( srid )
		except ValueError, e:
			self.srid = ManagerWindow.DEFAULT_SRID

		srs = QgsCoordinateReferenceSystem( self.srid, QgsCoordinateReferenceSystem.EpsgCrsId )
		renderer = self.canvas.mapRenderer()
		renderer.setDestinationSrs(srs)
		renderer.setMapUnits( srs.mapUnits() )


		# carica i layer WMS
		loadedWMS = QStringList()
		for order, rlid in ManagerWindow.RLID_WMS.iteritems():
			if QgsMapLayerRegistry.instance().mapLayer( rlid ) != None:
				loadedWMS << "'%s'" % order
		loadedWMS = loadedWMS.join( "," )

		query = AutomagicallyUpdater.Query( 'SELECT * FROM ZZ_WMS WHERE "ORDER" NOT IN (%s) ORDER BY "ORDER" ASC' % loadedWMS )
		query = query.getQuery()
		if not query.exec_():
			AutomagicallyUpdater._onQueryError( query.lastQuery(), query.lastError().text(), self )
		else:
			while query.next():
				order = query.value(0).toInt()[0]
				title = query.value(1).toString()
				url = query.value(2).toString()
				layers = query.value(3).toString()
				crs = query.value(4).toString()
				format = query.value(5).toString()
				transparent = query.value(6).toString()
				version = query.value(7).toString()

				layers = layers.split(",")
				styles = [ 'pseudo' ] * len(layers)
				format = "image/%s" % format.toLower()

				rl = QgsRasterLayer(0, url, title, 'wms', layers, styles, format, crs)
				if not rl.isValid():
					self.canvas.setRenderFlag( prevRenderFlag )
					QApplication.restoreOverrideCursor()
					return False

				ManagerWindow.RLID_WMS[order] = str(rl.getLayerID())
				QgsMapLayerRegistry.instance().addMapLayer(rl)
				self.iface.legendInterface().setLayerVisible( rl, False )

		import os.path
		conn = ConnectionManager.getConnection()

		# carica il layer con le geometrie originali
		if QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_ORIG ) == None:
			ManagerWindow.VLID_GEOM_ORIG = ''

			uri = QgsDataSourceURI()
			uri.setDatabase(conn.databaseName())
			uri.setDataSource('', self.TABLE_GEOM_ORIG, 'geometria')
			vl = QgsVectorLayer( uri.uri(), self.LAYER_GEOM_ORIG, "spatialite" )
			if vl == None or not vl.isValid() or not vl.setReadOnly(True):
				self.canvas.setRenderFlag( prevRenderFlag )
				QApplication.restoreOverrideCursor()
				return False

			# imposta lo stile del layer
			style_path = os.path.join( os.path.dirname(__file__), ManagerWindow.STYLE_PATH, ManagerWindow.STYLE_GEOM_ORIG )
			(errorMsg, result) = vl.loadNamedStyle( style_path )
			self.iface.legendInterface().refreshLayerSymbology(vl)

			ManagerWindow.VLID_GEOM_ORIG = vl.getLayerID()
			QgsMapLayerRegistry.instance().addMapLayer(vl)


		# carica il layer con le geometrie modificate
		if QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF ) == None:
			ManagerWindow.VLID_GEOM_MODIF = ''

			uri = QgsDataSourceURI()
			uri.setDatabase(conn.databaseName())
			uri.setDataSource('', self.TABLE_GEOM_MODIF, 'geometria')
			vl = QgsVectorLayer( uri.uri(), self.LAYER_GEOM_MODIF, "spatialite" )
			if vl == None or not vl.isValid() or not vl.setReadOnly(True):
				self.canvas.setRenderFlag( prevRenderFlag )
				QApplication.restoreOverrideCursor()
				return False

			# imposta lo stile del layer
			style_path = os.path.join( os.path.dirname(__file__), ManagerWindow.STYLE_PATH, ManagerWindow.STYLE_GEOM_MODIF )
			(errorMsg, result) = vl.loadNamedStyle( style_path )
			self.iface.legendInterface().refreshLayerSymbology(vl)

			ManagerWindow.VLID_GEOM_MODIF = vl.getLayerID()
			QgsMapLayerRegistry.instance().addMapLayer(vl)

		# carica il layer con le foto
		self.loadLayerFoto()

		if reloadExtent:
			# imposta l'ultimo extent usato
			self.loadLastUsedExtent()

		# ripristina il rendering
		self.canvas.setRenderFlag( prevRenderFlag )

		QApplication.restoreOverrideCursor()
		return True

	def loadLayerFoto(self):
		# carica il layer con le foto
		if QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_FOTO ) == None:
			ManagerWindow.VLID_FOTO = ''

			query = "SELECT ROWID AS pk, ID, MakePoint(GEOREF_PROIET_X, GEOREF_PROIET_Y, 3003) AS geometria FROM FOTO_GEOREF WHERE geometria IS NOT NULL"

			conn = ConnectionManager.getConnection()
			uri = QgsDataSourceURI()
			uri.setDatabase(conn.databaseName())
			uri.setDataSource('', "(%s)" % query, 'geometria', '', 'pk')
			vl = QgsVectorLayer( uri.uri(), self.LAYER_FOTO, "spatialite" )
			if vl == None or not vl.isValid() or not vl.setReadOnly(True):
				return False

			# imposta lo stile del layer
			import os.path
			style_path = os.path.join( os.path.dirname(__file__), ManagerWindow.STYLE_PATH, ManagerWindow.STYLE_FOTO )
			(errorMsg, result) = vl.loadNamedStyle( style_path )
			self.iface.legendInterface().refreshLayerSymbology(vl)

			ManagerWindow.VLID_FOTO = vl.getLayerID()
			QgsMapLayerRegistry.instance().addMapLayer(vl)
		return True


	def removeLayersFromCanvas(self):
		prevRenderFlag = self.canvas.renderFlag()
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		self.canvas.setRenderFlag(False)

		# rimuovi i layer WMS
		for order, rlid in ManagerWindow.RLID_WMS.iteritems():
			if QgsMapLayerRegistry.instance().mapLayer( rlid ) != None:
				QgsMapLayerRegistry.instance().removeMapLayer(rlid)
		ManagerWindow.RLID_WMS = {}

		# rimuovi i layer delle geometrie
		if QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_ORIG ) != None:
			QgsMapLayerRegistry.instance().removeMapLayer(ManagerWindow.VLID_GEOM_ORIG)
		if QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF ) != None:
			QgsMapLayerRegistry.instance().removeMapLayer(ManagerWindow.VLID_GEOM_MODIF)
		if QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_FOTO ) != None:
			QgsMapLayerRegistry.instance().removeMapLayer(ManagerWindow.VLID_FOTO)

		self.canvas.setRenderFlag(prevRenderFlag)
		QApplication.restoreOverrideCursor()
		return True


	@classmethod
	def aggiornaLayerModif(self):
		layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
		if layerModif == None:
			return

		# aggiorna il layer
		layerModif.dataProvider().setSubsetString( "" )	# trick! aggiorna l'extent del provider
		layerModif.triggerRepaint()
		layerModif.updateExtents()

	def aggiornaLayerFoto(self):
		layerFoto = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_FOTO )
		if layerFoto == None:
			return self.loadLayerFoto()

		# aggiorna il layer
		layerFoto.triggerRepaint()
		layerFoto.updateExtents()


	def loadLastUsedExtent(self):
		# recupera l'extent memorizzato
		query = AutomagicallyUpdater.Query( "SELECT XMIN, YMIN, XMAX, YMAX FROM ZZ_DISCLAIMER" ).getQuery()
		if query.exec_() and query.next():
			xmin, ok1 = query.value(0).toDouble()
			ymin, ok2 = query.value(1).toDouble()
			xmax, ok3 = query.value(2).toDouble()
			ymax, ok4 = query.value(3).toDouble()

			# imposta l'extent memorizzato come attuale
			if ok1 and ok2 and ok3 and ok4:
				extent = QgsRectangle( xmin, ymin, xmax, ymax )
				self.canvas.setExtent( extent )
				return

		# nessuno extent memorizzato o extent non valido, 
		# fai zoom all'estenzione del layer delle geometrie originali
		layerOrig = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_ORIG )
		if layerOrig == None:
			return
		self.iface.setActiveLayer( layerOrig )
		self.iface.zoomToActiveLayer()

	def storeLastUsedExtent(self):
		# memorizza l'extent corrente
		extent = self.canvas.extent()
		name2valueDict = {
			'XMIN' : extent.xMinimum(), 
			'YMIN' : extent.yMinimum(), 
			'XMAX' : extent.xMaximum(), 
			'YMAX' : extent.yMaximum()
		}
		AutomagicallyUpdater._updateValue( name2valueDict, "ZZ_DISCLAIMER", None, None )

	def closeEvent(self, event):
		self.storeLastUsedExtent()
		self.chiudiSchedaAperta()
		self.removeLayersFromCanvas()
		TemporaryFile.clear()
		ConnectionManager.closeConnection()

		self.disconnect(self.iface.mapCanvas(), SIGNAL( "mapToolSet(QgsMapTool *)" ), self.toolChanged)
		del self.status

		self.nuovaPointEmitter.deleteLater()
		del self.nuovaPointEmitter
		self.esistentePointEmitter.deleteLater()
		del self.esistentePointEmitter
		self.fotoPointEmitter.deleteLater()
		del self.fotoPointEmitter
		self.polygonDrawer.deleteLater()
		del self.polygonDrawer
		self.lineDrawer.deleteLater()
		del self.lineDrawer

		self.emit( SIGNAL("closed()") )
		return QDockWidget.closeEvent(self, event)


	class StatusWidget:
		def __init__(self, statusBar):
			self.statusBar = statusBar
			self.widget = QLabel()
			self.widget.clear()
			self.statusBar.addWidget( self.widget )
			self.statusBar.removeWidget( self.widget )

		def show(self, msg):
			self.widget.setText( msg )
			self.statusBar.clearMessage()
			self.statusBar.addWidget( self.widget )
			self.widget.show()

		def clear(self):
			self.widget.clear()
			self.statusBar.removeWidget( self.widget )

		def __del__(self):
			self.clear()
			self.widget.deleteLater()
			del self.widget

