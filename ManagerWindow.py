# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
import qgis.gui

from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import AutomagicallyUpdater
from MapTools import *

class ManagerWindow(QDockWidget):

	# nomi tabelle contenenti le geometrie
	TABLE_GEOM_ORIG = "GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZA".lower()
	TABLE_GEOM_MODIF = "GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE".lower()

	# ID dei layer contenenti geometrie e wms
	VLID_GEOM_ORIG = ''
	VLID_GEOM_MODIF = ''
	RLID_WMS = {}

	# stile per i layer delle geometrie
	STYLE_PATH = "styles"
	STYLE_GEOM_ORIG = "stile-geometrie-originali.qml"
	STYLE_GEOM_MODIF = "stile-geometrie-modificate.qml"

	DEFAULT_SRID = 3003

	instance = None
	iface = None
	scheda = None
	uvScheda = None

	def __init__(self, parent=None, iface=None):
		QDockWidget.__init__(self, parent)
		self.setAttribute(Qt.WA_DeleteOnClose)
		ManagerWindow.instance = self
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
		self.connect(self.btnSelSchedaEsistente, SIGNAL("clicked()"), self.apriScheda)
		self.connect(self.btnEliminaScheda, SIGNAL("clicked()"), self.eliminaScheda)
		self.connect(self.btnSpezzaGeometriaEsistente, SIGNAL("clicked()"), self.spezzaGeometriaEsistente)
		self.connect(self.btnCreaNuovaGeometria, SIGNAL("clicked()"), self.creaNuovaGeometria)
		self.connect(self.btnRipulisciGeometrie, SIGNAL("clicked()"), self.ripulisciGeometrie)
		self.connect(self.btnRiepilogoSchede, SIGNAL("clicked()"), self.riepilogoSchede)

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

		text = QString.fromUtf8( "Riepilogo schede edificio" )
		self.btnRiepilogoSchede = QPushButton( text, self.child )
		gridLayout.addWidget(self.btnRiepilogoSchede, 6, 0, 1, 1)

		self.setWidget(self.child)


	def riepilogoSchede(self):
		from DlgRiepilogoSchede import DlgRiepilogoSchede
		return DlgRiepilogoSchede(self).exec_()


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
				newID = AutomagicallyUpdater._insertGeometriaSpezzata( wkb, ManagerWindow.srid, codice )

			else:
				# altrimenti crea una geometria non presente tra le 
				# geometrie originali
				newID = AutomagicallyUpdater._insertGeometriaNuova( wkb, ManagerWindow.srid )

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

			query.prepare( "SELECT CODICE, ST_AsText(geometria) FROM GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZA WHERE ST_Intersects(geometria, ST_GeomFromWkb(?, ?)) AND CODICE NOT IN (SELECT GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE)" )
			query.addBindValue( QByteArray(line.asWkb()) )
			query.addBindValue( ManagerWindow.srid )
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
			query.addBindValue( ManagerWindow.srid )
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
				AutomagicallyUpdater._updateGeometria( ID, wkb, ManagerWindow.srid )

				# salva le nuove geometrie create dalla spezzatura
				for geometry in newGeometries:
					newWkb = QByteArray(geometry.asWkb())
					newID = salvaGeometriaSpezzata(codice, stato, newWkb)
					del geometry

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", e.toString())
			return

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
			if None == AutomagicallyUpdater._insertGeometriaNuova( wkb, ManagerWindow.srid ):
				return False

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", e.toString())
			return

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

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", e.toString())
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
			query = AutomagicallyUpdater.Query( "SELECT count(*) FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE AS gm1 WHERE (gm1.ZZ_STATO_GEOMETRIAID <> '2' /* non spezzate */ AND gm1.ID_UV_NEW NOT IN (SELECT GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW FROM SCHEDA_UNITA_VOLUMETRICA) /* senza scheda associata */ ) OR (gm1.ZZ_STATO_GEOMETRIAID = '2' /* spezzate */ AND 0 = (SELECT count(*) FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE as gm2 JOIN SCHEDA_UNITA_VOLUMETRICA AS uv ON gm2.ID_UV_NEW = uv.GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW WHERE gm1.GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE = gm2.GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE) /* fanno parte dello stesso edificio */ ) /* i cui pezzi sono tutti senza geometria associata */" )
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

	@classmethod
	def apriScheda(self, uvID=None):
		if uvID == None:
			ManagerWindow.instance.isApriScheda = True
			return ManagerWindow.instance.identificaSchedaEsistente()

		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		self.chiudiSchedaAperta()

		ManagerWindow.scheda = self.recuperaScheda( uvID )
		if ManagerWindow.scheda._ID == None:
			# imposta la geometria come abbinata a scheda
			try:
				QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
				ConnectionManager.startTransaction()
				ManagerWindow.scheda.save()
				AutomagicallyUpdater._updateValue( { "ABBINATO_A_SCHEDA" : '1' }, "GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE", "ID_UV_NEW", uvID )
			except ConnectionManager.AbortedException, e:
				QMessageBox.critical(ManagerWindow.instance, "Errore", e.toString())
				return

			finally:
				ConnectionManager.endTransaction()
				QApplication.restoreOverrideCursor()
			
		ManagerWindow.scheda.show()
		QApplication.restoreOverrideCursor()

	@classmethod
	def recuperaScheda(self, uvID):
		query = AutomagicallyUpdater.Query( "SELECT SCHEDA_EDIFICIOID FROM SCHEDA_UNITA_VOLUMETRICA WHERE GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW = ?", [ uvID ] )
		schedaID = query.getFirstResult()

		ManagerWindow.uvScheda = uvID

		from SchedaEdificio import SchedaEdificio
		return SchedaEdificio(ManagerWindow.instance, schedaID)


	@classmethod
	def chiudiSchedaAperta(self):
		if ManagerWindow.scheda != None:
			try:
				ManagerWindow.scheda.close()
			except RuntimeError:
				pass
			ManagerWindow.scheda = None

	@classmethod
	def eliminaScheda(self, codice=None):
		if codice == None:
			ManagerWindow.instance.isApriScheda = False
			return ManagerWindow.instance.identificaSchedaEsistente()

		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		# avvisa l'utente segnalando quante UV sono collegate a questa scheda
		# quindi chiedi se vuole davvero eliminare la scheda
		query = AutomagicallyUpdater.Query( "SELECT count(*) FROM SCHEDA_UNITA_VOLUMETRICA WHERE SCHEDA_EDIFICIOID IN (SELECT ed.ID FROM SCHEDA_EDIFICIO AS ed JOIN SCHEDA_UNITA_VOLUMETRICA AS uv ON uv.SCHEDA_EDIFICIOID = ed.ID WHERE uv.GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW = ?)", [codice] )

		numUV = query.getFirstResult()

		QApplication.restoreOverrideCursor()
		if numUV == None:
			return

		if QMessageBox.Ok != QMessageBox.warning( ManagerWindow.instance, "Eliminazione scheda", QString( u"La scheda ha %1 UV associate. Eliminare? L'operazione non è reversibile." ).arg( numUV ), QMessageBox.Ok|QMessageBox.Cancel ):
			return

		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# elimina la scheda
			scheda = self.recuperaScheda( codice )
			scheda.delete()

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(ManagerWindow.instance, "Errore", e.toString())
			return

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

		# aggiorna il layer con le geometrie modificate
		self.aggiornaLayerModif()


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
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		# disabilita il rendering
		prevRenderFlag = self.canvas.renderFlag()
		self.canvas.setRenderFlag( False )

		# recupera ed imposta il CRS della canvas
		query = AutomagicallyUpdater.Query( 'SELECT DISTINCT srid FROM geometry_columns' )
		srid = query.getFirstResult()
		try:
			ManagerWindow.srid = int( srid )
		except ValueError, e:
			ManagerWindow.DEFAULT_SRID
		srs = QgsCoordinateReferenceSystem( ManagerWindow.srid, QgsCoordinateReferenceSystem.EpsgCrsId )
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
				order = query.value(0).toString()
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

		import os.path
		conn = ConnectionManager.getConnection()

		# carica il layer con le geometrie originali
		if QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_ORIG ) == None:
			ManagerWindow.VLID_GEOM_ORIG = ''

			uri = QgsDataSourceURI()
			uri.setDatabase(conn.databaseName())
			uri.setDataSource('', self.TABLE_GEOM_ORIG, 'geometria')
			vl = QgsVectorLayer( uri.uri(), self.TABLE_GEOM_ORIG, "spatialite" )
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
			vl = QgsVectorLayer( uri.uri(), self.TABLE_GEOM_MODIF, "spatialite" )
			if vl == None or not vl.isValid() or not vl.setReadOnly(True):
				self.canvas.setRenderFlag( prevRenderFlag )
				QApplication.restoreOverrideCursor()
				return False

			if False:
				# imposta lo stile del layer
				style_path = os.path.join( os.path.dirname(__file__), ManagerWindow.STYLE_PATH, ManagerWindow.STYLE_GEOM_MODIF )
				(errorMsg, result) = vl.loadNamedStyle( style_path )
				self.iface.legendInterface().refreshLayerSymbology(vl)

			ManagerWindow.VLID_GEOM_MODIF = vl.getLayerID()
			QgsMapLayerRegistry.instance().addMapLayer(vl)

		# imposta l'ultimo extent usato
		self.loadLastUsedExtent()

		# ripristina il rendering
		self.canvas.setRenderFlag( prevRenderFlag )

		QApplication.restoreOverrideCursor()
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


	def loadLastUsedExtent(self):
		# recupera l'extent memorizzato
		query = AutomagicallyUpdater.Query( "SELECT XMIN, YMIN, XMAX, YMAX FROM ZZ_DISCLAIMER" ).getQuery()
		if query.exec_():
			if query.next():
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
		# ingrandisci all'estenzione del layer delle geometrie originali
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
		self.removeLayersFromCanvas()
		ConnectionManager.closeConnection()

		self.nuovaPointEmitter.stopCapture()
		self.esistentePointEmitter.stopCapture()
		self.polygonDrawer.stopCapture()
		self.lineDrawer.stopCapture()

		self.emit( SIGNAL("closed()") )
		return QDockWidget.closeEvent(self, event)

