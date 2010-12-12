# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
import qgis.gui

from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import AutomagicallyUpdater
from MapTools import *

class ManagerWindow(QDockWidget):

	GEOM_ORIGINALI_TABLENAME = "GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZA".lower()
	GEOM_MODIFICATE_TABLENAME = "GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE".lower()

	VLID_GEOM_ORIG = ''
	VLID_GEOM_MODIF = ''

	iface = None
	scheda = None
	uvScheda = None

	def __init__(self, parent=None, iface=None):
		QDockWidget.__init__(self, parent)
		self.setAttribute(Qt.WA_DeleteOnClose)
		ManagerWindow.iface = iface
		self.canvas = iface.mapCanvas()
		self.setupUi()

		self.isApriScheda = True

		MapTool.canvas = self.canvas

		self.nuovaPointEmitter = FeatureFinder()
		QObject.connect(self.nuovaPointEmitter, SIGNAL("pointEmitted(const QgsPoint &, Qt::MouseButton)"), self.identificaNuovaScheda)

		self.esistentePointEmitter = FeatureFinder()
		QObject.connect(self.esistentePointEmitter, SIGNAL("pointEmitted(const QgsPoint &, Qt::MouseButton)"), self.identificaSchedaEsistente)

		self.polygonDrawer = PolygonDrawer()
		QObject.connect(self.polygonDrawer, SIGNAL("geometryEmitted(const QgsGeometry *)"), self.creaNuovaGeometria)

		self.lineDrawer = LineDrawer()
		QObject.connect(self.lineDrawer, SIGNAL("geometryEmitted(const QgsGeometry *)"), self.spezzaGeometriaEsistente)

		self.connect(self.btnSelNuovaScheda, SIGNAL("clicked()"), self.identificaNuovaScheda)
		self.connect(self.btnSelSchedaEsistente, SIGNAL("clicked()"), self.identificaSchedaEsistente)
		self.connect(self.btnEliminaScheda, SIGNAL("clicked()"), self.eliminaScheda)
		self.connect(self.btnSpezzaGeometriaEsistente, SIGNAL("clicked()"), self.spezzaGeometriaEsistente)
		self.connect(self.btnCreaNuovaGeometria, SIGNAL("clicked()"), self.creaNuovaGeometria)
		self.connect(self.btnRipulisciGeometrie, SIGNAL("clicked()"), self.ripulisciGeometrie)

	def setupUi(self):
		self.setObjectName( "rt_omero_dockwidget" )
		self.setWindowTitle( "Omero RT" )
		self.child = QWidget()
		gridLayout = QGridLayout(self.child)

		text = QString.fromUtf8( "Identifica la geometria per \nla creazione di una nuova \nscheda edificio" )
		self.btnSelNuovaScheda = QPushButton( text, self.child )
		#self.btnSelNuovaScheda.setCheckable(True)
		gridLayout.addWidget(self.btnSelNuovaScheda, 0, 0, 1, 1)

		text = QString.fromUtf8( "Identifica la geometria per \nla apertura di una scheda \ngià esistente su di essa" )
		self.btnSelSchedaEsistente = QPushButton( text, self.child )
		#self.btnSelSchedaEsistente.setCheckable(True)
		gridLayout.addWidget(self.btnSelSchedaEsistente, 1, 0, 1, 1)

		text = QString.fromUtf8( "Elimina scheda edificio" )
		self.btnEliminaScheda = QPushButton( text, self.child )
		#self.btnEliminaScheda.setCheckable(True)
		gridLayout.addWidget(self.btnEliminaScheda, 2, 0, 1, 1)

		text = QString.fromUtf8( "Crea una nuova geometria da zero" )
		self.btnCreaNuovaGeometria = QPushButton( text, self.child )
		#self.btnCreaNuovaGeometria.setCheckable(True)
		gridLayout.addWidget(self.btnCreaNuovaGeometria, 3, 0, 1, 1)

		text = QString.fromUtf8( "Spezza una geometria esistente" )
		self.btnSpezzaGeometriaEsistente = QPushButton( text, self.child )
		#self.btnSpezzaGeometriaEsistente.setCheckable(True)
		gridLayout.addWidget(self.btnSpezzaGeometriaEsistente, 4, 0, 1, 1)

		text = QString.fromUtf8( "Ripulisci geometrie non associate" )
		self.btnRipulisciGeometrie = QPushButton( text, self.child )
		gridLayout.addWidget(self.btnRipulisciGeometrie, 5, 0, 1, 1)

		self.setWidget(self.child)


	def identificaNuovaScheda(self, point=None, button=None):
		if point == None:
			return self.nuovaPointEmitter.startCapture()

		if button != Qt.LeftButton:
			return

		layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
		if layerModif == None:
			return

		feat = self.nuovaPointEmitter.findAtPoint(layerModif, point)
		if feat != None:
			# controlla se tale geometria ha qualche scheda associata
			codice = feat.attributeMap()[0].toString()
			query = AutomagicallyUpdater.Query( "SELECT count(*) FROM SCHEDA_UNITA_VOLUMETRICA WHERE GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW = ?", [codice] )
			if int( query.getFirstResult() ) > 0:
				# NO, c'è già una scheda associata
				QMessageBox.warning( self, "RT Omero", "La geometria selezionata appartiene ad un edificio gia' esistente" )
				return self.nuovaPointEmitter.startCapture()

			# OK, non esiste alcuna scheda associata a tale geometria
			# associa la UV a tale geometria
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			self.apriScheda(codice)
			QApplication.restoreOverrideCursor()
			return
			
		layerOrig = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_ORIG )
		if layerOrig == None:
			return

		feat = self.nuovaPointEmitter.findAtPoint(layerOrig, point)		
		if feat != None:
			uvID = self.copiaGeometria(feat)
			if uvID == None:
				return

			self.apriScheda(uvID)
			QApplication.restoreOverrideCursor()
			return

		return self.nuovaPointEmitter.startCapture()


	def identificaSchedaEsistente(self, point=None, button=None):
		if point == None:
			return self.esistentePointEmitter.startCapture()

		if button != Qt.LeftButton:
			return

		layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
		if layerModif == None:
			return

		feat = self.esistentePointEmitter.findAtPoint(layerModif, point)
		if feat != None:
			# controlla se tale geometria ha qualche scheda associata
			codice = feat.attributeMap()[0].toString()
			query = AutomagicallyUpdater.Query( "SELECT count(*) FROM SCHEDA_UNITA_VOLUMETRICA WHERE GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW = ?", [codice] )
			if int( query.getFirstResult() ) > 0:
				# OK, c'è già una scheda associata
				codice = feat.attributeMap()[0].toString()
				if self.isApriScheda:
					self.apriScheda( codice )
				else:
					self.eliminaScheda( codice )
				return

			# NO, non esiste alcuna scheda associata a tale geometria
			QMessageBox.warning( self, "RT Omero", "Non esiste alcun edificio sulla geometria selezionata" )
			return self.esistentePointEmitter.startCapture()
			
		layerOrig = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_ORIG )
		if layerOrig == None:
			return

		feat = self.esistentePointEmitter.findAtPoint(layerOrig, point)		
		if feat != None:
			QMessageBox.warning( self, "RT Omero", "Non esiste alcun edificio sulla geometria selezionata" )
			return self.esistentePointEmitter.startCapture()

		return self.esistentePointEmitter.startCapture()


	def spezzaGeometriaEsistente(self, line=None):

		def salvaGeometriaSpezzata(codice, stato, wkb):
			if stato != '9':
				# se la geometria iniziale era copiata o spezzata, 
				# crea una nuova geometria spezzata
				newID = AutomagicallyUpdater._insertGeometriaSpezzata( wkb, codice )

			else:
				# altrimenti crea una geometria non presente tra le 
				# geometrie originali
				newID = AutomagicallyUpdater._insertGeometriaNuova( wkb )

			return newID


		if line == None:
			return self.lineDrawer.startCapture()

		# fai qui i test sulla linea

		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# copia le geometrie originali non ancora copiate e che intersecano la linea
			query = ConnectionManager.getNewQuery( AutomagicallyUpdater.EDIT_CONN_TYPE )
			if query == None:
				return False

			query.prepare( "SELECT CODICE, AsText(geometria) FROM (SELECT CODICE, geometria FROM GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZA WHERE Intersects(geometria, GeomFromWkb(?))) AS orig WHERE CODICE NOT IN (SELECT GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE)" )
			query.addBindValue( QByteArray(line.asWkb()) )
			if not query.exec_():
				AutomagicallyUpdater._onQueryError( query.lastQuery(), query.lastError().text(), self )
				return False

			featureList = []
			while query.next():
				ID = None
				codice = query.value(0).toString()
				stato = '1'
				wkt = query.value(1).toString()
				featureList.append( (ID, codice, stato, wkt) )

			for ID, codice, stato, wkt in featureList:
				geom = QgsGeometry.fromWkt( wkt )
				(retval, newGeometries, topologyTestPoints) = geom.splitGeometry( line.asPolyline(), False )
				if retval == 1:	# nessuna spezzatura
					continue

				# copia la geometria nel layer delle geometrie modificate
				ID = AutomagicallyUpdater._insertGeometriaCopiata( codice )
				if ID == None:
					return False

			# recupera le geometrie modificate che intersecano la linea
			query.prepare( "SELECT ID_UV_NEW, GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE, ZZ_STATO_GEOMETRIAID, AsText(geometria) FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE WHERE Intersects(geometria, GeomFromWkb(?))" )
			query.addBindValue( QByteArray(line.asWkb()) )

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
				AutomagicallyUpdater._updateGeometria( ID, wkb )

				# salva le nuove geometrie create dalla spezzatura
				for geometry in newGeometries:
					newWkb = QByteArray(geometry.asWkb())
					newID = salvaGeometriaSpezzata(codice, stato, newWkb)
					del geometry

		except Exception, e:
			if isinstance(e, ConnectionManager.AbortedException):
				QMessageBox.critical(self, "Errore", e.toString())
				return False
			raise

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

		# aggiorna il layer con le geometrie modificate
		self.aggiornaLayerModif()

		return True

	def creaNuovaGeometria(self, polygon=None):
		if polygon == None:
			return self.polygonDrawer.startCapture()

		# TODO: fai qui i test sul poligono

		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# inserisce la nuova geometria nel layer
			wkb = QByteArray(polygon.asWkb())
			if None == AutomagicallyUpdater._insertGeometriaNuova( wkb ):
				return False

		except Exception, e:
			if isinstance(e, ConnectionManager.AbortedException):
				QMessageBox.critical(self, "Errore", e.toString())
				return False
			raise

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

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

		except Exception, e:
			if isinstance(e, ConnectionManager.AbortedException):
				QMessageBox.critical(self, "Errore", e.toString())
				return
			raise

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
			query = AutomagicallyUpdater.Query( "SELECT count(*) FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE WHERE ID_UV_NEW NOT IN (SELECT GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW FROM SCHEDA_UNITA_VOLUMETRICA)" )
			numUV = query.getFirstResult()
		except:
			raise
		finally:
			QApplication.restoreOverrideCursor()

		if numUV == None:
			return

		if int(numUV) <= 0:
			QMessageBox.information(self, "Nessuna geometria trovata", "Non esistono geometrie senza scheda associata." )
			return

		if QMessageBox.Ok != QMessageBox.warning(self, "Eliminazione geometrie non associate", QString( u"Esistono %1 geometrie senza alcuna scheda associata. Vuoi eliminarle? L'operazione non è reversibile." ).arg( numUV ), QMessageBox.Ok|QMessageBox.Cancel ):
			return

		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# eliminazione geometrie non associate ad alcuna scheda
			AutomagicallyUpdater._deleteGeometria( None, "ID_UV_NEW NOT IN (SELECT GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW FROM SCHEDA_UNITA_VOLUMETRICA)" )

		except Exception, e:
			if isinstance(e, ConnectionManager.AbortedException):
				QMessageBox.critical(self, "Errore", e.toString())
				return
			raise

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

		# aggiorna il layer con le geometrie modificate
		self.aggiornaLayerModif()


	def apriScheda(self, uvID=None):
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		self.chiudiSchedaAperta()

		ManagerWindow.uvScheda = uvID
		ManagerWindow.scheda = self.recuperaScheda( ManagerWindow.uvScheda )
		ManagerWindow.scheda.show()

		QApplication.restoreOverrideCursor()

	def recuperaScheda(self, uvID):
		query = AutomagicallyUpdater.Query( "SELECT SCHEDA_EDIFICIOID FROM SCHEDA_UNITA_VOLUMETRICA WHERE GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW = ?", [ uvID ] )
		idScheda = query.getFirstResult()

		from SchedaEdificio import SchedaEdificio
		scheda = SchedaEdificio(self, self.iface)
		if idScheda != None:
			scheda.setupLoader(idScheda)
		return scheda

	def eliminaScheda(self, codice=None):
		if codice == None:
			self.isApriScheda = False
			return self.identificaSchedaEsistente()
		self.isApriScheda = True

		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		# avvisa l'utente segnalando quante UV sono collegate a questa scheda
		# quindi chiedi se vuole davvero eliminare la scheda
		query = AutomagicallyUpdater.Query( "SELECT count(*) FROM SCHEDA_UNITA_VOLUMETRICA WHERE SCHEDA_EDIFICIOID IN (SELECT ed.ID FROM SCHEDA_EDIFICIO AS ed JOIN SCHEDA_UNITA_VOLUMETRICA AS uv ON uv.SCHEDA_EDIFICIOID = ed.ID WHERE uv.GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW = ?)", [codice] )

		numUV = query.getFirstResult()

		QApplication.restoreOverrideCursor()
		if numUV == None:
			return

		if QMessageBox.Ok != QMessageBox.warning(self, "Eliminazione scheda", QString( u"La scheda ha %1 UV associate. Eliminare? L'operazione non è reversibile." ).arg( numUV ), QMessageBox.Ok|QMessageBox.Cancel ):
			return

		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# elimina la scheda
			scheda = self.recuperaScheda( codice )
			scheda.delete()

		except Exception, e:
			if isinstance(e, ConnectionManager.AbortedException):
				QMessageBox.critical(self, "Errore", e.toString())
				return
			raise

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

		# aggiorna il layer con le geometrie modificate
		self.aggiornaLayerModif()

	def chiudiSchedaAperta(self):
		if ManagerWindow.scheda != None:
			try:
				ManagerWindow.scheda.close()
			except RuntimeError:
				pass
			ManagerWindow.scheda = None


	def getPathToDB(self, forceDialog=False):
		settings = QSettings()
		pathToSqliteDB = settings.value( "/omero_RT/pathToSqliteDB", QVariant("") ).toString()

		if pathToSqliteDB.isEmpty() or not QFileInfo(pathToSqliteDB).exists() or forceDialog:
			newPath = QFileDialog.getOpenFileName(self, "Seleziona il DB", pathToSqliteDB, "Sqlite DB (*.sqlite *.db3);;Tutti i file (*)" )
			if newPath.isEmpty():
				return None

			pathToSqliteDB = newPath
			settings.setValue( "/omero_RT/pathToSqliteDB", QVariant(pathToSqliteDB) )

		return pathToSqliteDB


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
			return

		self.iface.addDockWidget(Qt.LeftDockWidgetArea, self)

		if not self.loadLayersInCanvas():
			QMessageBox.critical(self, "RT Omero", "Impossibile caricare i layer richiesti dal database selezionato")


	def loadLayersInCanvas(self):
		conn = ConnectionManager.getConnection()

		prevRenderFlag = self.canvas.renderFlag()
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		self.canvas.setRenderFlag( False )

		# carica il layer con le geometrie originali in sola lettura
		if QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_ORIG ) == None:
			ManagerWindow.VLID_GEOM_ORIG = ''

			uri = QgsDataSourceURI()
			uri.setDatabase(conn.databaseName())
			uri.setDataSource('', self.GEOM_ORIGINALI_TABLENAME, 'geometria')
			vl = QgsVectorLayer( uri.uri(), self.GEOM_ORIGINALI_TABLENAME, "spatialite" )
			if vl == None or not vl.isValid() or not vl.setReadOnly(True):
				self.canvas.setRenderFlag( prevRenderFlag )
				QApplication.restoreOverrideCursor()
				return False

			ManagerWindow.VLID_GEOM_ORIG = vl.getLayerID()
			QgsMapLayerRegistry.instance().addMapLayer(vl)

		# carica il layer con le geometrie modificate
		if QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF ) == None:
			ManagerWindow.VLID_GEOM_MODIF = ''

			uri = QgsDataSourceURI()
			uri.setDatabase(conn.databaseName())
			uri.setDataSource('', self.GEOM_MODIFICATE_TABLENAME, 'geometria')
			vl = QgsVectorLayer( uri.uri(), self.GEOM_MODIFICATE_TABLENAME, "spatialite" )
			if vl == None or not vl.isValid():# or not vl.setReadOnly(True):
				self.canvas.setRenderFlag( prevRenderFlag )
				QApplication.restoreOverrideCursor()
				return False

			ManagerWindow.VLID_GEOM_MODIF = vl.getLayerID()
			QgsMapLayerRegistry.instance().addMapLayer(vl)

			# ingrandisci all'estenzione del layer delle geometrie modificate
			#self.iface.setActiveLayer(vl)
			#self.iface.zoomToActiveLayer()

		self.canvas.setRenderFlag( prevRenderFlag )
		QApplication.restoreOverrideCursor()
		return True

	def removeLayersFromCanvas(self):
		prevRenderFlag = self.canvas.renderFlag()
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		self.canvas.setRenderFlag(False)
		if QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_ORIG ) != None:
			QgsMapLayerRegistry.instance().removeMapLayer(ManagerWindow.VLID_GEOM_ORIG)
		if QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF ) != None:
			QgsMapLayerRegistry.instance().removeMapLayer(ManagerWindow.VLID_GEOM_MODIF)
		self.canvas.setRenderFlag(prevRenderFlag)
		QApplication.restoreOverrideCursor()
		return True

	@classmethod
	def aggiornaLayerModif(self):
		layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
		if layerModif == None:
			return

		layerModif.updateExtents()
		layerModif.triggerRepaint()

	def closeEvent(self, event):
		self.removeLayersFromCanvas()
		ConnectionManager.closeConnection()

		self.nuovaPointEmitter.stopCapture()
		self.esistentePointEmitter.stopCapture()
		self.polygonDrawer.stopCapture()
		self.lineDrawer.stopCapture()

		self.emit( SIGNAL("closed()") )
		return QDockWidget.closeEvent(self, event)

