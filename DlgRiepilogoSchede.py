# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import qgis.gui
import qgis.core

from ui.dlgRiepilogoSchede_ui import Ui_Dialog
from AutomagicallyUpdater import *

class DlgRiepilogoSchede(QDialog, Ui_Dialog):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setupUi(self)

		# crea una webview per la stampa della scheda
		self.webView = QWebView(self)
		self.webView.setVisible(False)
		QObject.connect(self.webView, SIGNAL("loadFinished(bool)"), self.loadFinished)

		# su Win non funziona, probabile problema in QtSql 
		#AutomagicallyUpdater.loadTables( self.schedeList, AutomagicallyUpdater.Query( self.createQuerySchede() ) )
		# workaround, usa pyspatialite
		AutomagicallyUpdater.loadTables( self.schedeList, AutomagicallyUpdater.Query( self.createQuerySchede(), None, 1 ) )

		self.connect(self.apriBtn, SIGNAL("clicked()"), self.apriScheda)
		self.connect(self.eliminaBtn, SIGNAL("clicked()"), self.eliminaScheda)
		self.connect(self.stampaBtn, SIGNAL("clicked()"), self.stampaSchede)
		self.connect(self.centraBtn, SIGNAL("clicked()"), self.centraUV)
		self.connect(self.schedeList, SIGNAL("itemSelectionChanged()"), self.aggiornaPulsanti)

		self.aggiornaPulsanti()


	def createQuerySchede(self, lista=True):
		"""
		crea una query per recuperare l'intestazione (titolo) delle schede:
		se 'lista' è True (default) di tutte le schede definite,
		altrimenti solo di una (la query si aspetta come parametro ? l'ID della scheda)
		"""

		# recupera il primo indirizzo di ogni scheda edificio
		query_indirizzi = """
SELECT * FROM INDIRIZZO_VIA ORDER BY ROWID DESC
"""

		# recupera tutti i comuni nella forma "comune (provincia)"
		query_comuni = """
SELECT com.ISTATCOM, com.NOME || ' (' || prov.NOME || ')' AS NOME 
FROM ZZ_PROVINCE AS prov JOIN ZZ_COMUNI AS com ON prov.ISTATPROV = com.ZZ_PROVINCEISTATPROV
"""

		# recupera il primo civico di ogni scheda edificio
		# TODO integrare in query_indirizzo, in tal modo recupero solo il primo civico di ogni primo indirizzo di ogni scheda
		query_ncivici = """
SELECT N_CIVICO || MOD_CIVICO AS CIVICO, LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ, INDIRIZZO_VIAID_INDIRIZZO
FROM NUMERI_CIVICI ORDER BY ROWID DESC
"""

		from WdgLocalizzazioneIndirizzi import WdgLocalizzazioneIndirizzi
		comune_non_valido = WdgLocalizzazioneIndirizzi.COMUNE_NON_VALIDO
		via_civico_non_valido = WdgLocalizzazioneIndirizzi.VIA_CIVICO_NON_VALIDO

		if lista == True:
			# query che recupera IDscheda, "via, civico - comune (provincia)"
			query_localizzazione = """
	SELECT 
		sch.ID AS ID, 
		CASE com.NOME IS NULL 
			WHEN 0 THEN 
				CASE ind.VIA = '' OR ind.VIA IS NULL 
					WHEN 0 THEN 
						CASE length(ind.VIA) > 50 WHEN 1 THEN substr(ind.VIA, 0, 50) || '...' ELSE ind.VIA END
					ELSE '%s' 
				END 
				|| ', ' || 
				CASE civ.CIVICO = '' OR civ.CIVICO IS NULL WHEN 0 THEN civ.CIVICO ELSE '%s' END 
				|| ' - ' || com.NOME 
			ELSE '%s' 
		END AS INDIRIZZO 
	FROM 
		SCHEDA_EDIFICIO AS sch JOIN LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA loc_ind ON loc_ind.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ = sch.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ 
		JOIN (%s) AS ind ON ind.ID_INDIRIZZO = loc_ind.INDIRIZZO_VIAID_INDIRIZZO 
		LEFT OUTER JOIN (%s) AS com ON com.ISTATCOM = ind.ZZ_COMUNIISTATCOM 
		LEFT OUTER JOIN (%s) AS civ ON civ.INDIRIZZO_VIAID_INDIRIZZO = ind.ID_INDIRIZZO AND civ.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ = sch.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ 
	GROUP BY sch.ID
	ORDER BY com.NOME, ind.VIA ASC""" % (via_civico_non_valido, via_civico_non_valido, comune_non_valido, query_indirizzi, query_comuni, query_ncivici)

		else:
			# query che recupera "istat_comune - via - civico" se tali campi sono tutti presenti altrimenti IDscheda
			# richiede 1 parametro: l'IDscheda della scheda di cui si vuole recuperare tale informazione
			query_localizzazione = """
	SELECT 
		CASE com.NOME IS NULL OR ind.VIA = '' OR ind.VIA IS NULL OR civ.CIVICO = '' OR civ.CIVICO IS NULL 
			WHEN 1 THEN sch.ID 
			ELSE com.ISTATCOM || ' - ' || ind.VIA || ' - ' || civ.CIVICO 
		END AS INDIRIZZO
	FROM 
		SCHEDA_EDIFICIO AS sch JOIN LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA loc_ind ON loc_ind.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ = sch.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ 
		JOIN (%s) AS ind ON ind.ID_INDIRIZZO = loc_ind.INDIRIZZO_VIAID_INDIRIZZO 
		LEFT OUTER JOIN (%s) AS com ON com.ISTATCOM = ind.ZZ_COMUNIISTATCOM 
		LEFT OUTER JOIN (%s) AS civ ON civ.INDIRIZZO_VIAID_INDIRIZZO = ind.ID_INDIRIZZO AND civ.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ = sch.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ
	WHERE sch.ID = ?""" % (query_indirizzi, query_comuni, query_ncivici)

		return query_localizzazione


	def aggiornaPulsanti(self):
		enabled = AutomagicallyUpdater.getValue(self.schedeList) != None
		self.apriBtn.setEnabled( enabled )
		self.eliminaBtn.setEnabled( enabled )
		self.centraBtn.setEnabled( False )#enabled )
		self.stampaBtn.setEnabled( enabled )

	def recuperaUvID(self, schedaID):
		query = AutomagicallyUpdater.Query( "SELECT GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW FROM SCHEDA_UNITA_VOLUMETRICA WHERE SCHEDA_EDIFICIOID = ?", [ schedaID ] )
		return query.getFirstResult()

	def apriScheda(self):
		schedaID = AutomagicallyUpdater.getValue( self.schedeList )
		uvID = self.recuperaUvID( schedaID )
		if uvID == None:
			QMessageBox.warning(self, "Errore", "La scheda selezionata non ha alcuna UV associata! ")
			return

		from ManagerWindow import ManagerWindow
		if ManagerWindow.instance.apriScheda(uvID):
			self.close()

	def eliminaScheda(self):
		schedaID = AutomagicallyUpdater.getValue( self.schedeList )
		uvID = self.recuperaUvID( schedaID )
		if uvID == None:
			QMessageBox.warning(self, "Errore", "La scheda selezionata non ha alcuna UV associata! ")
			return

		from ManagerWindow import ManagerWindow
		if ManagerWindow.instance.eliminaScheda(uvID):
			self.close()

	def centraUV(self):
		schedaID = AutomagicallyUpdater.getValue( self.schedeList )
		uvID = self.recuperaUvID( schedaID )
		if uvID == None:
			QMessageBox.warning(self, "Errore", "La scheda selezionata non ha alcuna UV associata! ")
			return

	def stampaSchede(self):
		self.invalidPrint = []
		self.toPrint = []
		self.currentIndex = -1

		self.outFn = "%s.pdf"
		lastDir = AutomagicallyUpdater._getLastUsedDir( 'pdf' )

		if len(self.schedeList.selectedItems()) > 1:
			# permetti all'utente di selezionare la directory di output
			lastDir = QFileDialog.getExistingDirectory(self, "Salvataggio le schede", lastDir, QFileDialog.ShowDirsOnly )
			if lastDir.isEmpty():
				return
			AutomagicallyUpdater._setLastUsedDir( 'pdf', lastDir )

		import os.path
		self.outFn = os.path.join( str(lastDir), self.outFn )

		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		# recupera tutte le schede selezionate
		for item in self.schedeList.selectedItems():
			self.toPrint.append( item.data(Qt.UserRole).toString() )

		# avvia la stampa
		self.printNext()

	def printNext(self):
		self.currentIndex = self.currentIndex + 1

		if self.currentIndex >= len(self.toPrint):	# stampa completata
			QApplication.restoreOverrideCursor()
			return

		# recupera la scheda
		schedaID = self.toPrint[self.currentIndex]
		uvID = self.recuperaUvID( schedaID )
		if uvID == None:	# nessuna UV associata alla scheda
			self.invalidPrint.append( schedaID )
			return self.printNext()
		
		from ManagerWindow import ManagerWindow
		scheda = ManagerWindow.instance.recuperaScheda(uvID)
		if scheda == None:	# impossibile recuperare la scheda
			self.invalidPrint.append( schedaID )
			return self.printNext()

		# genera la scheda in HTML
		self.webView.setHtml( scheda.toHtml() )

	def loadFinished(self, ok):
		schedaID = self.toPrint[self.currentIndex]
		fn = AutomagicallyUpdater.Query( self.createQuerySchede(False), [schedaID], 1 ).getFirstResult()

		if not ok:
			self.invalidPrint.append( schedaID )
		else:
			printer = QPrinter()
			printer.setOutputFormat( QPrinter.PdfFormat )
			printer.setOutputFileName( self.outFn % fn )

			if len(self.toPrint) == 1:	# solo una scheda, mostra la preview
				printDlg = QPrintPreviewDialog(printer, self)
				QObject.connect(printDlg, SIGNAL("paintRequested(QPrinter *)"), self.webView.print_)
				QApplication.restoreOverrideCursor()

				if printDlg.exec_():
					AutomagicallyUpdater._setLastUsedDir( 'pdf', printer.outputFileName() )

				QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

			else:	# stampa direttamente su pdf
				self.webView.print_(printer)

			del printer
			# rimuovi i file temporanei collegati alla generazione dell'html
			from Utils import TemporaryFile
			TemporaryFile.delAllFiles( TemporaryFile.KEY_SCHEDAEDIFICIO2HTML )


		# stampa il successivo
		self.printNext()

