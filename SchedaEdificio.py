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

		self._printMode, _ = AutomagicallyUpdater.printBehavior()

		if self._printMode in (QPrinter.PdfFormat, QPrinter.NativeFormat):
			# create a webview to load the HTML
			from PyQt4.QtWebKit import QWebView
			self._webView = QWebView(self)
			self._webView.setVisible(False)
			QObject.connect(self._webView, SIGNAL("loadFinished(bool)"), self.webViewLoadFinished)

			# generate the HTML and load it into the webview
			html = self.toHtml()
			self._webView.setHtml( html )

		else:	# print to HTML files
			outputDir = AutomagicallyUpdater._getLastUsedDir( 'pdf' )

			if preview:
				QApplication.restoreOverrideCursor()
				outputDir = QFileDialog.getExistingDirectory(self, "Salvataggio scheda", outputDir, QFileDialog.ShowDirsOnly)
				QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
				if outputDir == "":
					return self.onPrintFinished( True )

				AutomagicallyUpdater._setLastUsedDir( 'pdf', outputDir )

			# create the dir that will contain the html file within the output dir
			outputDir = QDir( outputDir )
			outputPath = outputDir.filePath( self._ID )
			if not outputDir.exists( self._ID ) and not outputDir.mkdir( self._ID ):
				QMessageBox.warning( self, "RT Omero", u"Impossibile creare il percorso '%s'" % outputPath )
				return self.onPrintFinished( False )

			# generate the HTML using outputPath as directory for the images/resources
			html = self.toHtml( outputPath )
			htmlFile = unicode( QDir( outputPath ).filePath( "index.html" ) )
			with open( htmlFile, 'w' ) as fout:
				fout.write( html )

			self.onPrintFinished(True)

			#if preview:
			#	QDesktopServices.openUrl( QUrl.fromLocalFile( htmlFile ) )

	def webViewLoadFinished(self, ok):
		if not ok:
			return self.onPrintFinished( False )

		# get the instance of the printer
		from ManagerWindow import ManagerWindow
		printer = ManagerWindow.instance.getPrinter()
		printer.setDocName( self.getTitoloStampa() )

		if self._printMode == QPrinter.PdfFormat:
			# set the output format and filename
			lastDir = AutomagicallyUpdater._getLastUsedDir( 'pdf' )
			outFn = QDir( lastDir ).filePath( u"%s.pdf" % self.getTitoloStampa() )
			printer.setOutputFileName( outFn )

		if self._previewOnPrinting:
			printDlg = QPrintPreviewDialog(printer, self)
			QObject.connect(printDlg, SIGNAL("paintRequested(QPrinter *)"), self._webView.print_)

			QApplication.restoreOverrideCursor()
			ret = printDlg.exec_()
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

			if ret:
				if self._printMode == QPrinter.PdfFormat:
					AutomagicallyUpdater._setLastUsedDir( 'pdf', printer.outputFileName() )

			printDlg.deleteLater()
			del printDlg

		elif self._printMode == QPrinter.NativeFormat:
			printDlg = QPrintDialog(printer, self)

			QApplication.restoreOverrideCursor()
			ret = printDlg.exec_()
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

			if ret:
				self._webView.print_(printer)

		else: # print to PDF without asking to the user
			self._webView.print_(printer)

		return self.onPrintFinished( ok )

	def onPrintFinished(self, ok):
		# remove temporary files, i.e. images/resources used in the HTML
		from Utils import TemporaryFile
		TemporaryFile.delAllFiles( TemporaryFile.KEY_SCHEDAEDIFICIO2HTML )

		if self._printMode in (QPrinter.PdfFormat, QPrinter.NativeFormat):
			self._webView.deleteLater()
			del self._webView

		self.PRINCIPALE.printBtn.setEnabled( True )
		QApplication.restoreOverrideCursor()
		self.emit( SIGNAL("printFinished"), ok, self._ID )
		return ok


	def creaStralcioCartografico( self, size, scale, ext="png", factor=1, outpath=None):
		from ManagerWindow import ManagerWindow

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

		def createStralcioUsingCanvas(filename, size, scale, ext="png", factor=1):
			# get the reference to the main canvas and its renderer
			mainCanvas = ManagerWindow.instance.iface.mapCanvas()
			mainRenderer = mainCanvas.mapRenderer()

			# create a new map canvas and setup it
			canvas = qgis.gui.QgsMapCanvas( ManagerWindow.instance.iface.mainWindow() )
			canvas.setCanvasColor( Qt.white )
			canvas.setFixedSize( size.width(), size.height() )
			canvas.setRenderFlag( False )

			settings = QSettings()
			canvas.enableAntiAliasing( settings.value( "/qgis/enable_anti_aliasing", False, type=bool ) )
			canvas.useImageToRender( settings.value( "/qgis/use_qimage_to_render", False, type=bool ) )

			canvas.mapRenderer().setDestinationCrs( mainRenderer.destinationCrs() )
			canvas.mapRenderer().setMapUnits( mainRenderer.mapUnits() )

			try:
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

				# XXX: why? it's needed to update the extent of the other canvas
				canvas.show()
				mainCanvas.setRenderFlag( True )

				# select the geometries
				layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
				if layerModif != None:
					query = AutomagicallyUpdater.Query( "SELECT gmod.ROWID FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE AS gmod JOIN SCHEDA_UNITA_VOLUMETRICA AS suv ON gmod.ID_UV_NEW = suv.GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW WHERE SCHEDA_EDIFICIOID = ?", [ self._ID ] ).getQuery()
					if query.exec_():
						selIds = []
						while query.next():
							selIds.append( query.value(0) )
						layerModif.setSelectedFeatures( selIds )

					canvas.zoomToSelected( layerModif )

				# zoom to scale
				canvas.zoomScale( scale )

				# save the map to a file
				eventLoopHandler = [ QEventLoop(self) ]
				def savePainter(p, scale, evlHandler):
					renderScaleLabel(p, scale)
					evlHandler[0].quit()
					evlHandler[0].deleteLater()
					del evlHandler[0]

				onRenderFunc = lambda x: savePainter(x, scale, eventLoopHandler)
				QObject.connect(canvas, SIGNAL("renderComplete(QPainter *)"), onRenderFunc)
				canvas.setRenderFlag( True )

				if len(eventLoopHandler) > 0:
					eventLoopHandler[0].exec_( QEventLoop.ExcludeUserInputEvents )
		
				QObject.disconnect(canvas, SIGNAL("renderComplete(QPainter *)"), onRenderFunc)
				canvas.saveAsImage( filename, None, ext.upper() )
				extent = canvas.extent()

				# remove the wordfile create by canvas.saveAsImage()
				wordfile = QFile( filename[:-4] + filename[-4:].upper() + "w" )
				if wordfile.exists():
					wordfile.remove()

			finally:
				canvas.hide()
				canvas.deleteLater()
				del canvas

			return filename, extent

		def createStralcioUsingRenderer(filename, size, scale, ext="png", factor=1):
			# create the output image and pre-fill it
			image = QPixmap( size )
			image.fill( QColor(255, 255, 255, 255) )

			# get the reference to the main canvas and its renderer
			mainCanvas = ManagerWindow.instance.iface.mapCanvas()
			mainRenderer = mainCanvas.mapRenderer()

			# create a new renderer and setup it
			mapRenderer = qgis.core.QgsMapRenderer()
			mapRenderer.setOutputSize( size, image.logicalDpiX() )
			mapRenderer.setDestinationCrs( mainRenderer.destinationCrs() )
			mapRenderer.setMapUnits( mainRenderer.mapUnits() )
			mapRenderer.setProjectionsEnabled( mainRenderer.hasCrsTransformEnabled() )

			# add layers to renderer layer set
			layerIds = []
			# add WMS layers
			for order, rlid in sorted( ManagerWindow.RLID_WMS.iteritems() ):
				layer = QgsMapLayerRegistry.instance().mapLayer( rlid )
				if layer != None and ManagerWindow.instance.iface.legendInterface().isLayerVisible( layer ):
					lid = layer.id() if hasattr(layer, 'id') else layer.getLayerID()	# old API compatibility
					layerIds.insert(0, lid)

			# add other layers
			layers = [ManagerWindow.VLID_GEOM_ORIG, ManagerWindow.VLID_GEOM_MODIF, ManagerWindow.VLID_FOTO]
			for vlid in layers:
				layer = QgsMapLayerRegistry.instance().mapLayer( vlid )
				if layer != None:
					layer.removeSelection()
					lid = layer.id() if hasattr(layer, 'id') else layer.getLayerID()	# old API compatibility
					layerIds.insert(0, lid)

			mapRenderer.setLayerSet( layerIds )

			# select the geometries
			layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
			if layerModif != None:
				query = AutomagicallyUpdater.Query( "SELECT gmod.ROWID FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE AS gmod JOIN SCHEDA_UNITA_VOLUMETRICA AS suv ON gmod.ID_UV_NEW = suv.GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW WHERE SCHEDA_EDIFICIOID = ?", [ self._ID ] ).getQuery()
				if query.exec_():
					selIds = []
					while query.next():
						selIds.append( query.value(0) )
					layerModif.setSelectedFeatures( selIds )

				mapRenderer.setExtent( layerModif.boundingBoxOfSelected() )

			# zoom at the scale
			extent = mapRenderer.extent()
			extent.scale( float(scale) / mapRenderer.scale() )
			mapRenderer.setExtent( extent )

			# render now!
			painter = QPainter()
			painter.begin( image )

			#settings = QSettings()
			#antiAliasingEnabled = settings.value( "/qgis/enable_anti_aliasing", False ).toBool()
			#painter.setRenderHints( QPainter.RenderHints() | (QPainter.Antialiasing if antiAliasingEnabled else 0) )

			mapRenderer.render( painter )
			renderScaleLabel(painter, scale)

			painter.end()
			del painter

			mapRenderer.deleteLater()
			del mapRenderer

			# save the image to a file
			image.save( filename, ext.upper() )
			del image

			return filename, extent


		if outpath is None:
			# get a new temp file
			from Utils import TemporaryFile
			tmp = TemporaryFile.getNewFile( TemporaryFile.KEY_SCHEDAEDIFICIO2HTML, ext )
			if not tmp.open():
				TemporaryFile.delFile( TemporaryFile.KEY_SCHEDAEDIFICIO2HTML, ext )
				return "", None
			filename = unicode( tmp.fileName() )
			tmp.close()

		else:
			filename = u"%s/stralcio.%s" % (outpath, ext)

		# override the canvas render flag
		mainCanvas = ManagerWindow.instance.iface.mapCanvas()
		prevRenderFlag = mainCanvas.renderFlag()
		mainCanvas.setRenderFlag( False )

		# override the selection color
		#prevColor = QgsRenderer.selectionColor()
		#newColor = QColor( Qt.yellow )
		#newColor.setAlpha(127)
		#QgsRenderer.setSelectionColor( newColor )
		prevColor = qgis.core.QgsMapRenderer().rendererContext().selectionColor()
		newColor = QColor( Qt.yellow )
		newColor.setAlpha(127)
		qgis.core.QgsMapRenderer().rendererContext().setSelectionColor( newColor )

		# set layers visible
		legend = ManagerWindow.instance.iface.legendInterface()
		layerOrig = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_ORIG )
		if layerOrig != None:
			prevOrigState = ManagerWindow.instance.iface.legendInterface().isLayerVisible( layerOrig )
			ManagerWindow.instance.iface.legendInterface().setLayerVisible( layerOrig, True )

		layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
		if layerModif != None:
			prevModifState = ManagerWindow.instance.iface.legendInterface().isLayerVisible( layerModif )
			prevSelection = layerModif.selectedFeaturesIds()
			ManagerWindow.instance.iface.legendInterface().setLayerVisible( layerModif, True )

		try:
			if True:
				# XXX: why? the output image seems to be generated at a wrong scale using a new renderer
				filename, extent = createStralcioUsingCanvas(filename, size, scale, ext, factor)
			else:
				filename, extent = createStralcioUsingRenderer(filename, size, scale, ext, factor)
		finally:
			# restore the original layers' state and selection
			if layerOrig != None:
				legend.setLayerVisible( layerOrig, prevOrigState )
			if layerModif != None:
				legend.setLayerVisible( layerModif, prevModifState )
				layerModif.setSelectedFeatures( prevSelection )

			# restore the canvas original state and selection color
			#QgsRenderer.setSelectionColor( prevColor )
			qgis.core.QgsMapRenderer().rendererContext().setSelectionColor( prevColor )
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
			QMessageBox.critical(self, "Errore", e)
			return

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()
			self.onClosing()
			self.emit( SIGNAL("closed()") )

		# carica il layer delle foto
		from ManagerWindow import ManagerWindow
		ManagerWindow.instance.aggiornaLayerFoto()

	def toHtml(self, prefix=None):
		import os.path
		currentPath = os.path.dirname(__file__)

		# path to css file
		css_orig = os.path.join( currentPath, "docs", "default.css" )
		if prefix is None:
			css = css_orig
		else:
			# copy the css file to the output folder
			css = QDir( prefix ).filePath( "default.css" )
			if not QFile.exists( css ) and not QFile.copy( css_orig, css ):
				css = css_orig
		css = QUrl.fromLocalFile(css).toString()

		# path to the omero banner
		banner_orig = os.path.join( currentPath, "docs", "banner_omero.gif" )
		if prefix is None:
			banner = banner_orig
		else:
			# copy the omero banner file to the output folder
			banner = QDir( prefix ).filePath( "banner_omero.gif" )
			if not QFile.exists( banner ) and not QFile.copy( banner_orig, banner ):
				banner = banner_orig
		banner = QUrl.fromLocalFile(banner).toString()

		# path to the logo
		if prefix is None:
			logoDir = QDir( AutomagicallyUpdater._getPathToDb() )
		else:
			logoDir = QDir( prefix )

		logo = logoDir.filePath( "omero_stampa_logo.jpg" )
		if not QFile.exists( logo ):
			logo_orig = os.path.join( currentPath, "docs", "omero_stampa_logo.jpg" )
			if not QFile.copy( logo_orig, logo ):
				logo = logo_orig
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

		return u"""
<html>
<head>
	<title>Scheda di rilevamento</title>
	<link media="all" href="%s" type="text/css" rel="stylesheet">
</head>
<body>

<div id="header">
	<div id="omero">
		<img src="%s" alt="Omero">
	</div>
	<div id="logo">
		<img src="%s" alt="Logo">
	</div>
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
%s %s %s %s %s %s %s 
<div id="sez8" class="block">
<p class="section">SEZIONE A8 - FOTOGRAFIE</p>
%s %s
</div>
</body>
</html>
""" % (css, banner, logo, comune, nome_edificio if nome_edificio != None else '', via, self._ID, data, self.PRINCIPALE.toHtml(), self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.toHtml(), self.UNITA_VOLUMETRICHE.toHtml(), self.INTERVENTI.toHtml(), self.STATO_UTILIZZO_EDIFICIOID.toHtml(), self.CARATTERISTICHE_STRUTTURALI.toHtml(), self.CARATTERISTICHE_ARCHITETTONICHE_EDIFICIOID.toHtml(), self.stralcioToHtml(prefix), self.FOTO.toHtml(prefix))

	def stralcioToHtml(self, prefix=None):
		xmin = ymin = xmax = ymax = ""

		# dimensioni e scala originali
		realwidth = 700
		realscale = 1000

		# TRICK! aumenta la risoluzione dell'immagine
		# riduce la scala e ingrandisce le dimensioni dell'immagine in output
		factor = 1

		# size and scale will be passed to the map renderer
		renderwidth = realwidth * factor
		renderscale = realscale / factor

		# create the image
		filename, extent = self.creaStralcioCartografico( QSize(renderwidth, renderwidth), renderscale, "png", factor, outpath=prefix )
		filename = QUrl.fromLocalFile(filename).toString()
		if extent != None:
			xmin = extent.xMinimum()
			ymin = extent.yMinimum()
			xmax = extent.xMaximum()
			ymax = extent.yMaximum()

		# size of the image displayed in the HTML page
		printwidth = realwidth*1.25

		return u"""
<table class="border">
	<tr>
		<td colspan="4">Stralcio cartografico dell'edificio</td>
	</tr>
	<tr>
		<td colspan="4" class="mapContainer"><img class="map border" style="width: %spx; height: %spx;" src="%s" alt="stralcio cartografico"></td>
	</tr>
	<tr>
		<td>xmin</td><td class="value">%s</td>
		<td>ymin</td><td class="value">%s</td>
	</tr>
	<tr>
		<td>xmax</td><td class="value">%s</td>
		<td>ymax</td><td class="value">%s</td>
	</tr>
</table>
""" % (printwidth, printwidth, filename, xmin, ymin, xmax, ymax)
