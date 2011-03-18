# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import qgis.gui
import qgis.core

from ui.mainSchedaEdificio_ui import Ui_SchedaEdificio
from AutomagicallyUpdater import *

class SchedaEdificio(QMainWindow, MappingOne2One, Ui_SchedaEdificio):

	def __init__(self, parent=None, schedaID=None):
		QMainWindow.__init__(self, parent)
		MappingOne2One.__init__(self, "SCHEDA_EDIFICIO")
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setupUi(self)
		self.sectionsStacked.setCurrentIndex(0)

		# salva il titolo predefinito della finestra
		self.defaultTitle = self.windowTitle()

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

		# aggiorna il titolo della scheda con l'indirizzo del primo tab indirizzi
		indirizzo = self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA.firstTab
		self.connect(indirizzo, SIGNAL("indirizzoChanged(const QString &)"), self.impostaTitolo)

		self.connect(self.PRINCIPALE.printBtn, SIGNAL("clicked()"), self.stampaScheda)

		# carica i dati della scheda
		self.setupLoader( schedaID )

	def currentSectionChanged(self):
		if self.sectionsList.currentRow() < 0:
			return
		self.sectionsStacked.setCurrentIndex(self.sectionsList.currentRow())

	def impostaTitolo(self, title=QString()):
		if not title.isEmpty():
			self.setWindowTitle( title )
		else:
			self.setWindowTitle( self.defaultTitle )


	def getTitoloStampa(self):
		indirizzo = self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA.firstTab

		istatcom = self.getValue(indirizzo.ZZ_COMUNIISTATCOM)
		via = indirizzo.VIA.currentText()
		civico = indirizzo.NUMERI_CIVICI.rowToString(0)

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


	def closeEvent(self, event):
		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# effettua il salvataggio della scheda
			self.save()

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", e.toString())
			return

		finally:
			# rimuovi i file temporanei collegati alla scheda
			from Utils import TemporaryFile
			TemporaryFile.delAllFiles( TemporaryFile.KEY_SCHEDAEDIFICIO )

			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

	def toHtml(self):
		import os.path
		currentPath = os.path.dirname(__file__)
		css = os.path.join( currentPath, "docs", "default.css" )
		giunta = os.path.join( currentPath, "docs", "RTgiunta_logo.jpg" )
		return QString( u"""
<html>
<head>
	<title>Scheda di rilevamento</title>
	<link media="all" href="%s" type="text/css" rel="stylesheet">
</head>
<body>

<div id="header">
	<img id="rt_giunta" src="%s" alt="RT Giunta regionale">
	<p><span id="ter_amb">Direzione Generale Politiche Territoriali e Ambientali</span><br>
		<span id="sigta">Sistema Informativo per il Governo del Territorio e dell'Ambiente</span>
	</p>
	<p id="mude">Indagine sperimentale per la implementazione del DB Topografico attraverso rilievi sul campo sugli edifici e aggiornamento tramite il MUDE</p>
</div>
%s %s %s %s %s %s %s %s 
</body>
</html>
""" % (css, giunta, self.PRINCIPALE.toHtml(), self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.toHtml(), self.UNITA_VOLUMETRICHE.toHtml(), self.INTERVENTI.toHtml(), self.STATO_UTILIZZO_EDIFICIOID.toHtml(), self.CARATTERISTICHE_STRUTTURALI.toHtml(), self.CARATTERISTICHE_ARCHITETTONICHE_EDIFICIOID.toHtml(), self.FOTO.toHtml() )
)
