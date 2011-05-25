# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
import qgis.gui

from ui.mainSchedaEdificio_ui import Ui_SchedaEdificio
from AutomagicallyUpdater import *

class SchedaEdificio(QMainWindow, MappingOne2One, Ui_SchedaEdificio):

	def __init__(self, parent=None, schedaID=None):
		QMainWindow.__init__(self, parent)
		MappingOne2One.__init__(self, "SCHEDA_EDIFICIO")
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setupUi(self)
		self.sectionsStacked.setCurrentIndex(0)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.ZZ_PROPRIETA_PREVALENTEID: AutomagicallyUpdater.ZZTable( "ZZ_PROPRIETA_PREVALENTE" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.PRINCIPALE, 
			self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ,
			self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.ZZ_PROPRIETA_PREVALENTEID, 
			self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.NUM_UNITA_IMMOBILIARI, 
			self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.PARTICELLE_CATASTALI, 
			self.UNITA_VOLUMETRICHE, 
			self.INTERVENTI, 
			self.STATO_UTILIZZO_EDIFICIOID,
			self.CARATTERISTICHE_STRUTTURALI, 
			self.CARATTERISTICHE_ARCHITETTONICHE_EDIFICIOID, 
			self.FOTO 
		]
		self.setupValuesUpdater(childrenList)

		self.connect(self.sectionsList, SIGNAL("itemSelectionChanged()"), self.currentSectionChanged)
		self.connect(self.PRINCIPALE.printBtn, SIGNAL("clicked()"), self.stampaScheda)

		# aggiorna il titolo della scheda con l'indirizzo del primo tab indirizzi
		indirizzo = self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA.firstTab
		self.connect(indirizzo, SIGNAL("indirizzoChanged"), self.aggiornaTitolo)

		# carica i dati della scheda
		self.setupLoader( schedaID )
		self.aggiornaTitolo()

	def currentSectionChanged(self):
		if self.sectionsList.currentRow() < 0:
			return
		self.sectionsStacked.setCurrentIndex(self.sectionsList.currentRow())

	def aggiornaTitolo(self):
		indirizzo = self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA.firstTab

		comune = indirizzo.ZZ_COMUNIISTATCOM.currentText()
		provincia = indirizzo.ZZ_PROVINCEISTATPROV.currentText()
		via = indirizzo.VIA.currentText()
		civico = indirizzo.NUMERI_CIVICI.rowToString()

		from WdgLocalizzazioneIndirizzi import WdgLocalizzazioneIndirizzi
		indirizzo_non_valido = WdgLocalizzazioneIndirizzi.INDIRIZZO_NON_VALIDO
		indirizzo_non_inserito = WdgLocalizzazioneIndirizzi.INDIRIZZO_NON_INSERITO

		if comune != '':
			via = u"%s, %s" % (via, civico) if via != '' and civico != '' else indirizzo_non_inserito
			titolo = u"%s - %s (%s)" % (via, comune, provincia)
		else:
			titolo = indirizzo_non_valido
		self.setWindowTitle( titolo )

	def getTitoloStampa(self):
		indirizzo = self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA.firstTab

		istatcom = self.getValue(indirizzo.ZZ_COMUNIISTATCOM)
		via = indirizzo.VIA.currentText()
		civico = indirizzo.NUMERI_CIVICI.rowToString()

		if istatcom != None and via != '' and civico != '':
			return u"%s - %s - %s" % ( istatcom, via, civico )
		return self._ID

	def stampaScheda(self, preview=True):
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		self.PRINCIPALE.printBtn.setEnabled( False )
		self.previewOnPrinting = preview

		# crea una webview per la stampa della scheda
		from PyQt4.QtWebKit import QWebView
		self.webView = QWebView(self)
		self.webView.setVisible(False)
		QObject.connect(self.webView, SIGNAL("loadFinished(bool)"), self.webViewLoadFinished)

		# genera la scheda in HTML
		self.webView.setHtml( self.toHtml() )

	def webViewLoadFinished(self, ok):
		if ok:
			lastDir = AutomagicallyUpdater._getLastUsedDir( 'pdf' )
			outFn = "%s.pdf" % self.getTitoloStampa()
			import os.path
			outFn = os.path.join( str(lastDir), outFn )

			printer = QPrinter()
			printer.setOutputFormat( QPrinter.PdfFormat )
			printer.setOutputFileName( outFn )

			if self.previewOnPrinting:
				printDlg = QPrintPreviewDialog(printer, self)
				QObject.connect(printDlg, SIGNAL("paintRequested(QPrinter *)"), self.webView.print_)

				QApplication.restoreOverrideCursor()
				if printDlg.exec_():
					AutomagicallyUpdater._setLastUsedDir( 'pdf', printer.outputFileName() )
				QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

			else: # stampa direttamente su pdf
				self.webView.print_(printer)

			del printer

		# rimuovi i file temporanei collegati alla generazione dell'html
		from Utils import TemporaryFile
		TemporaryFile.delAllFiles( TemporaryFile.KEY_SCHEDAEDIFICIO2HTML )
		del self.webView

		self.PRINCIPALE.printBtn.setEnabled( True )
		QApplication.restoreOverrideCursor()
		self.emit( SIGNAL("printFinished"), ok, self._ID )


	def creaStralcioCartografico( self, size, scale, ext="png", factor=1):

		def renderScaleLabel(painter, scale, factor=1):
			text = "1:%s" % (scale*factor)

			fontSize = 10*factor
			font = QFont( "helvetica", fontSize )
			painter.setFont( font )
			fontMetrics = QFontMetrics( font )

			margin = 20*factor
			bufferSize = 1
			backColor = Qt.white
			foreColor = Qt.black
    
			# first the buffer
			painter.setPen( backColor )
			fontWidth = fontMetrics.width( text )
			fontHeight = fontMetrics.height()
			for i in range(-bufferSize, bufferSize+1):
				for j in range(-bufferSize, bufferSize+1):
					painter.drawText( i + margin, j + margin, text )

			# then the text itself
			painter.setPen( foreColor );
			painter.drawText( margin, margin, text )

		# get a new temp file
		from Utils import TemporaryFile
		tmp = TemporaryFile.getNewFile( TemporaryFile.KEY_SCHEDAEDIFICIO2HTML, ext )
		if not tmp.open():
			TemporaryFile.delFile( TemporaryFile.KEY_SCHEDAEDIFICIO2HTML, ext )
			return QString(), None
		filename = tmp.fileName()
		tmp.close()

		from ManagerWindow import ManagerWindow
		mainCanvas = ManagerWindow.instance.iface.mapCanvas()
		prevRenderFlag = mainCanvas.renderFlag()
		mainCanvas.setRenderFlag( False )

		canvas = qgis.gui.QgsMapCanvas( ManagerWindow.instance.iface.mainWindow() )
		canvas.setCanvasColor( Qt.white )
		canvas.show()
		canvas.setFixedSize( size.width(), size.height() )
		canvas.setRenderFlag( False )

		settings = QSettings()
		canvas.enableAntiAliasing( settings.value( "/qgis/enable_anti_aliasing", QVariant(False) ).toBool() )
		canvas.useImageToRender( settings.value( "/qgis/use_qimage_to_render", QVariant(False) ).toBool() )

		renderer = ManagerWindow.instance.iface.mapCanvas().mapRenderer()
		canvas.mapRenderer().setDestinationSrs( renderer.destinationSrs() )
		canvas.mapRenderer().setMapUnits( renderer.mapUnits() )

		canvasLayers = []
		# add WMS layers
		for order, rlid in sorted( ManagerWindow.RLID_WMS.iteritems() ):
			layer = QgsMapLayerRegistry.instance().mapLayer( rlid )
			if layer != None and ManagerWindow.instance.iface.legendInterface().isLayerVisible( layer ):
				cl = qgis.gui.QgsMapCanvasLayer(layer)
				canvasLayers.insert(0, cl)

		# add other layers
		layers = [ManagerWindow.VLID_GEOM_ORIG, ManagerWindow.VLID_GEOM_MODIF, ManagerWindow.VLID_FOTO]
		for vlid in layers:
			layer = QgsMapLayerRegistry.instance().mapLayer( vlid )
			if layer != None:
				layer.removeSelection()
				cl = qgis.gui.QgsMapCanvasLayer(layer)
				canvasLayers.insert(0, cl)

		canvas.setLayerSet( canvasLayers )

		layerOrig = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_ORIG )
		if layerOrig != None:
			prevOrigState = ManagerWindow.instance.iface.legendInterface().isLayerVisible( layerOrig )
			ManagerWindow.instance.iface.legendInterface().setLayerVisible( layerOrig, True )

		layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
		if layerModif != None:
			prevModifState = ManagerWindow.instance.iface.legendInterface().isLayerVisible( layerModif )
			ManagerWindow.instance.iface.legendInterface().setLayerVisible( layerModif, True )
			mainCanvas.setRenderFlag( True )
			
			# select the geometries
			query = AutomagicallyUpdater.Query( "SELECT gmod.ROWID FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE AS gmod JOIN SCHEDA_UNITA_VOLUMETRICA AS suv ON gmod.ID_UV_NEW = suv.GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW WHERE SCHEDA_EDIFICIOID = ?", [ self._ID ] ).getQuery()
			if query.exec_():
				selIds = []
				while query.next():
					selIds.append( query.value(0).toInt()[0] )
				layerModif.setSelectedFeatures( selIds )

			canvas.zoomToSelected( layerModif )
		canvas.zoomScale( scale )

		# override the selection color
		prevColor = QgsRenderer.selectionColor()
		newColor = QColor( Qt.yellow )
		newColor.setAlpha(127)
		QgsRenderer.setSelectionColor( newColor )

		# save the map to a file
		renderFunc = lambda x: renderScaleLabel(x, scale)
		self.connect(canvas, SIGNAL("renderComplete(QPainter *)"), renderFunc)
		canvas.setRenderFlag( True )
		canvas.saveAsImage( filename, None, ext.upper() )
		extent = canvas.extent()
		self.disconnect(canvas, SIGNAL("renderComplete(QPainter *)"), renderFunc)
		canvas.deleteLater()
		del canvas

		# remove the wordfile create by canvas.saveAsImage()
		wordfile = QFile( filename[:-4] + filename[-4:].toUpper() + "w" )
		if wordfile.exists():
			wordfile.remove()

		# restore the original state and color
		if layerOrig != None:
			ManagerWindow.instance.iface.legendInterface().setLayerVisible( layerOrig, prevOrigState )
		if layerModif != None:
			ManagerWindow.instance.iface.legendInterface().setLayerVisible( layerModif, prevModifState )
		QgsRenderer.setSelectionColor( prevColor )
		mainCanvas.setRenderFlag( prevRenderFlag )

		return filename, extent

	def setMinimized(self, minimize=True):
		if minimize:
			self.setWindowState( self.windowState() | Qt.WindowMinimized )
		else:
			self.setWindowState( self.windowState() & ~Qt.WindowMinimized )
			self.raise_()

	def closeEvent(self, event):
		# rimuovi i file temporanei collegati alla scheda
		from Utils import TemporaryFile
		TemporaryFile.delAllFiles( TemporaryFile.KEY_SCHEDAEDIFICIO )

		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# effettua il salvataggio della scheda
			self.save()

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", e.toString())
			return

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()
			self.onClosing()
			self.emit( SIGNAL("closed()") )

		# carica il layer delle foto
		from ManagerWindow import ManagerWindow
		ManagerWindow.instance.aggiornaLayerFoto()

	def toHtml(self):
		import os.path
		currentPath = os.path.dirname(__file__)

		css = os.path.join( currentPath, "docs", "default.css" )

		dbPath = AutomagicallyUpdater._getPathToDb()
		logo = QFileInfo( dbPath ).dir().filePath( "omero_stampa_logo.jpg" )
		if not QFile.exists( logo ):
			logoOrig = os.path.join( currentPath, "docs", "omero_stampa_logo.jpg" )
			if not QFile.copy( logoOrig, logo ):
				logo = logoOrig

		comune = AutomagicallyUpdater.Query( "SELECT NOME FROM ZZ_COMUNI WHERE ISTATCOM = ?", [AutomagicallyUpdater._getIDComune()] ).getFirstResult()

		indirizzo = self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA.firstTab
		via = indirizzo.VIA.currentText()
		civico = indirizzo.NUMERI_CIVICI.rowToString()

		if via != '' and civico != '':
			via = u"%s, %s" % (via, civico)
		else:
			via = ''

		nome_edificio = self.getValue( self.PRINCIPALE.NOME_EDIFICIO )
		data = QDate.currentDate().toString( "dd/MM/yyyy" )

		return QString( u"""
<html>
<head>
	<title>Scheda di rilevamento</title>
	<link media="all" href="%s" type="text/css" rel="stylesheet">
</head>
<body>

<div id="header">
	<img id="logo" src="%s" alt="Logo">
	<p id="comune">Comune di %s</p>
	<p id="titolo">Scheda edificio</p>
	<div id="edificio">
		<p id="nomeedificio">%s</p>
		<p id="via">%s</p>
	</div>
	<p id="idscheda">Scheda: %s</p>
	<p id="data">scheda stampata il %s</p>
	<p id="info">(QuantumGIS - Omero - Regione Toscana - S.I.T.A.)</p>
</div>
%s %s %s %s %s %s %s %s 
</body>
</html>
""" % (css, logo, comune, nome_edificio if nome_edificio != None else '', via, self._ID, data, self.PRINCIPALE.toHtml(), self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.toHtml(), self.UNITA_VOLUMETRICHE.toHtml(), self.INTERVENTI.toHtml(), self.STATO_UTILIZZO_EDIFICIOID.toHtml(), self.CARATTERISTICHE_STRUTTURALI.toHtml(), self.CARATTERISTICHE_ARCHITETTONICHE_EDIFICIOID.toHtml(), self.FOTO.toHtml() )
)
