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

from ui.dlgRiepilogoSchede_ui import Ui_Dialog
from AutomagicallyUpdater import *

class DlgRiepilogoSchede(QDialog, Ui_Dialog):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setupUi(self)

		self.loadListaSchede()

		self.connect(self.apriBtn, SIGNAL("clicked()"), self.apriScheda)
		self.connect(self.eliminaBtn, SIGNAL("clicked()"), self.eliminaScheda)
		self.connect(self.stampaBtn, SIGNAL("clicked()"), self.stampaSchede)
		self.connect(self.centraBtn, SIGNAL("clicked()"), self.centraScheda)
		self.connect(self.schedeList, SIGNAL("itemSelectionChanged()"), self.aggiornaPulsanti)

		self.aggiornaPulsanti()

	def loadListaSchede(self):
		# su Win non funziona, probabile problema in QtSql 
		#AutomagicallyUpdater.loadTables( self.schedeList, AutomagicallyUpdater.Query( self.createQuerySchede() ) )
		# workaround, usa pyspatialite
		AutomagicallyUpdater.loadTables( self.schedeList, AutomagicallyUpdater.Query( self.createQuerySchede(), None, 1 ) )


	def createQuerySchede(self):
		""" crea una query per recuperare l'intestazione (titolo) delle schede """

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
		indirizzo_non_valido = WdgLocalizzazioneIndirizzi.INDIRIZZO_NON_VALIDO
		indirizzo_non_inserito = WdgLocalizzazioneIndirizzi.INDIRIZZO_NON_INSERITO

		# query che recupera IDscheda, "via, civico - comune (provincia)"
		query_localizzazione = """
SELECT 
	sch.ID AS ID, 
	CASE com.NOME IS NULL 
		WHEN 0 THEN 
			CASE ind.VIA = '' OR ind.VIA IS NULL OR civ.CIVICO = '' OR civ.CIVICO IS NULL
				WHEN 0 THEN 
					CASE length(ind.VIA) > 50 WHEN 1 THEN substr(ind.VIA, 0, 50) || '...' ELSE ind.VIA END
					|| ', ' || civ.CIVICO
				ELSE '%s'
			END 
			|| ' - ' || com.NOME 
		ELSE '%s' 
	END AS INDIRIZZO 
FROM 
	SCHEDA_EDIFICIO AS sch JOIN LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA loc_ind ON loc_ind.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ = sch.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ 
	JOIN (%s) AS ind ON ind.ID_INDIRIZZO = loc_ind.INDIRIZZO_VIAID_INDIRIZZO 
	LEFT OUTER JOIN (%s) AS com ON com.ISTATCOM = ind.ZZ_COMUNIISTATCOM 
	LEFT OUTER JOIN (%s) AS civ ON civ.INDIRIZZO_VIAID_INDIRIZZO = ind.ID_INDIRIZZO AND civ.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ = sch.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ 
GROUP BY sch.ID
ORDER BY com.NOME, ind.VIA ASC""" % (indirizzo_non_inserito, indirizzo_non_valido, query_indirizzi, query_comuni, query_ncivici)

		return query_localizzazione


	def aggiornaPulsanti(self):
		enabled = AutomagicallyUpdater.getValue(self.schedeList) != None
		self.apriBtn.setEnabled( enabled )
		self.eliminaBtn.setEnabled( enabled )
		self.centraBtn.setEnabled( enabled )
		self.stampaBtn.setEnabled( enabled )

	def recuperaUvID(self, schedaID):
		query = AutomagicallyUpdater.Query( "SELECT GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW FROM SCHEDA_UNITA_VOLUMETRICA WHERE SCHEDA_EDIFICIOID = ?", [ schedaID ] )
		return query.getFirstResult()

	def centraScheda(self):
		schedaID = AutomagicallyUpdater.getValue( self.schedeList )
		uvID = self.recuperaUvID( schedaID )
		if uvID == None:
			QMessageBox.warning(self, u"Errore", u"La scheda selezionata non ha alcuna UV associata!")
			return

		from ManagerWindow import ManagerWindow
		if not ManagerWindow.instance.selezionaScheda(uvID):
			return
		return uvID


	def apriScheda(self):
		uvID = self.centraScheda()
		if uvID == None:
			return

		from ManagerWindow import ManagerWindow
		if ManagerWindow.instance.apriScheda(uvID):
			self.close()

	def eliminaScheda(self):
		uvID = self.centraScheda()
		if uvID == None:
			return

		from ManagerWindow import ManagerWindow
		if ManagerWindow.instance.eliminaScheda(uvID):
			self.loadListaSchede()


	def stampaSchede(self):
		self.invalidPrint = []
		self.toPrint = []
		self.currentIndex = -1

		if len(self.schedeList.selectedItems()) > 1:
			# permetti all'utente di selezionare la directory di output
			lastDir = AutomagicallyUpdater._getLastUsedDir( 'pdf' )
			lastDir = QFileDialog.getExistingDirectory(self, u"Salvataggio le schede", lastDir, QFileDialog.ShowDirsOnly )
			if lastDir.isEmpty():
				return
			AutomagicallyUpdater._setLastUsedDir( 'pdf', lastDir )

		# recupera tutte le schede selezionate
		for item in self.schedeList.selectedItems():
			self.toPrint.append( item.data(Qt.UserRole).toString() )

		# avvia la stampa
		self.printNext()

	def printNext(self):
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		self.currentIndex = self.currentIndex + 1

		if self.currentIndex >= len(self.toPrint):	# stampa completata
			del self.toPrint
			del self.invalidPrint
			QApplication.restoreOverrideCursor()
			return

		# recupera la scheda
		schedaID = self.toPrint[self.currentIndex]
		uvID = self.recuperaUvID( schedaID )
		if uvID == None:	# nessuna UV associata alla scheda
			self.invalidPrint.append( schedaID )
			return self.printNext()
		
		from ManagerWindow import ManagerWindow
		self.currentScheda = ManagerWindow.instance.recuperaScheda(uvID)
		if self.currentScheda == None:	# impossibile recuperare la scheda
			self.invalidPrint.append( schedaID )
			return self.printNext()

		self.connect(self.currentScheda, SIGNAL("printFinished"), self.printFinished)
		previewOnPrinting = len(self.toPrint) == 1

		QApplication.restoreOverrideCursor()
		self.currentScheda.stampaScheda( previewOnPrinting )

	def printFinished(self, ok, schedaID):
		if not ok:
			self.invalidPrint.append( schedaID )

		# elimina la scheda
		self.currentScheda.close()
		del self.currentScheda

		# stampa il successivo
		self.printNext()

