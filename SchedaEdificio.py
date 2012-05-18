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
			self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.ZZ_PROPRIETAID: AutomagicallyUpdater.ZZTable( "ZZ_PROPRIETA" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.PRINCIPALE, 
			self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ,
			self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.ZZ_PROPRIETAID, 
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
		self._previewOnPrinting = preview

		# crea una webview per la stampa della scheda
		from PyQt4.QtWebKit import QWebView
		self._webView = QWebView(self)
		self._webView.setVisible(False)
		QObject.connect(self._webView, SIGNAL("loadFinished(bool)"), self.webViewLoadFinished)

		# genera la scheda in HTML
		html = self.toHtml()
		#print ">>>\n\n", html, "\n\n<<<"
		self._webView.setHtml( html )

	def webViewLoadFinished(self, ok):
		if ok:
			lastDir = AutomagicallyUpdater._getLastUsedDir( 'pdf' )
			outFn = u"%s.pdf" % self.getTitoloStampa()
			import os.path
			outFn = os.path.join( str(lastDir), outFn )

			from ManagerWindow import ManagerWindow
			printer = ManagerWindow.instance.getPrinter()
			printer.setOutputFormat( QPrinter.PdfFormat )
			#printer.setPaperSize( QPrinter.A4 )
			#printer.setOrientation( QPrinter.Portrait )
			printer.setOutputFileName( outFn )
			printer.setCreator( "Omero RT plugin (Quantum GIS)" )

			if self._previewOnPrinting:
				printDlg = QPrintPreviewDialog(printer, self)
				QObject.connect(printDlg, SIGNAL("paintRequested(QPrinter *)"), self._webView.print_)

				QApplication.restoreOverrideCursor()
				if printDlg.exec_():
					AutomagicallyUpdater._setLastUsedDir( 'pdf', printer.outputFileName() )
				QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

				printDlg.deleteLater()
				del printDlg

			else: # stampa direttamente su pdf
				self._webView.print_(printer)

		# rimuovi i file temporanei collegati alla generazione dell'html
		from Utils import TemporaryFile
		TemporaryFile.delAllFiles( TemporaryFile.KEY_SCHEDAEDIFICIO2HTML )

		self._webView.deleteLater()
		del self._webView

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

		# get the reference to the main canvas and its renderer
		from ManagerWindow import ManagerWindow
		mainCanvas = ManagerWindow.instance.iface.mapCanvas()
		prevRenderFlag = mainCanvas.renderFlag()
		mainCanvas.setRenderFlag( False )
		mainRenderer = ManagerWindow.instance.iface.mapCanvas().mapRenderer()

		# create the output image and pre-fill it
		image = QImage( size, QImage.Format_ARGB32_Premultiplied )
		image.fill( QColor(255, 255, 255, 0).value() )

		# create a new renderer and setup it
		mapRenderer = qgis.core.QgsMapRenderer()
		mapRenderer.setOutputSize( size, image.logicalDpiX() )
		mapRenderer.setDestinationSrs( mainRenderer.destinationSrs() )
		mapRenderer.setMapUnits( mainRenderer.mapUnits() )
		mapRenderer.setProjectionsEnabled( mainRenderer.hasCrsTransformEnabled() )

		# override the selection color
		prevColor = QgsRenderer.selectionColor()
		newColor = QColor( Qt.yellow )
		newColor.setAlpha(127)
		QgsRenderer.setSelectionColor( newColor )

		# add layers to renderer layer set
		layerIds = []
		# add WMS layers
		for order, rlid in sorted( ManagerWindow.RLID_WMS.iteritems() ):
			layer = QgsMapLayerRegistry.instance().mapLayer( rlid )
			if layer != None and ManagerWindow.instance.iface.legendInterface().isLayerVisible( layer ):
				layerIds.insert(0, getattr(layer, 'id', layer.getLayerID)() )

		# add other layers
		layers = [ManagerWindow.VLID_GEOM_ORIG, ManagerWindow.VLID_GEOM_MODIF, ManagerWindow.VLID_FOTO]
		for vlid in layers:
			layer = QgsMapLayerRegistry.instance().mapLayer( vlid )
			if layer != None:
				layer.removeSelection()
				layerIds.insert(0, getattr(layer, 'id', layer.getLayerID)() )

		mapRenderer.setLayerSet( layerIds )

		# select the geometries
		layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
		if layerModif != None:
			query = AutomagicallyUpdater.Query( "SELECT gmod.ROWID FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE AS gmod JOIN SCHEDA_UNITA_VOLUMETRICA AS suv ON gmod.ID_UV_NEW = suv.GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW WHERE SCHEDA_EDIFICIOID = ?", [ self._ID ] ).getQuery()
			if query.exec_():
				selIds = []
				while query.next():
					selIds.append( query.value(0).toInt()[0] )
				layerModif.setSelectedFeatures( selIds )

			mapRenderer.setExtent( layerModif.boundingBoxOfSelected() )

		# zoom at the scale
		extent = mapRenderer.extent()
		extent.scale( scale / mapRenderer.scale() )
		mapRenderer.setExtent( extent )

		settings = QSettings()
		antiAliasingEnabled = settings.value( "/qgis/enable_anti_aliasing", QVariant(False) ).toBool()

		painter = QPainter( image )
		painter.setRenderHints( QPainter.RenderHints() | (QPainter.Antialiasing if antiAliasingEnabled else 0) )

		mapRenderer.render( painter )
		renderScaleLabel(painter, scale)

		mapRenderer.deleteLater()
		del mapRenderer
		del painter

		# save the image to a file
		image.save( filename, ext.upper() )
		del image

		# restore the canvas original state and selection color
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
		css = QUrl.fromLocalFile(css).toString()

		dbPath = AutomagicallyUpdater._getPathToDb()
		logo = QFileInfo( dbPath ).dir().filePath( "omero_stampa_logo.jpg" )
		if not QFile.exists( logo ):
			logoOrig = os.path.join( currentPath, "docs", "omero_stampa_logo.jpg" )
			if not QFile.copy( logoOrig, logo ):
				logo = logoOrig
		logo = QUrl.fromLocalFile(logo).toString()

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
