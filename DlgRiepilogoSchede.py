# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import qgis.gui
import qgis.core

from ui.dlgRiepilogoSchede_ui import Ui_Dialog
from AutomagicallyUpdater import *

class DlgRiepilogoSchede(QDialog, MappingOne2One, Ui_Dialog):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		MappingOne2One.__init__(self)
		self.setupUi(self)

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

		# query che recupera IDscheda, "via, civico - comune (provincia)"
		query_localizzazione = """
SELECT 
	sch.ID AS ID, 
	CASE com.NOME IS NULL 
		WHEN 0 THEN 
			CASE ind.VIA = '' OR ind.VIA IS NULL WHEN 0 THEN ind.VIA ELSE '%s' END 
			|| ', ' || 
			CASE civ.CIVICO = '' OR civ.CIVICO IS NULL WHEN 0 THEN civ.CIVICO ELSE '%s' END 
			|| ' - ' || com.NOME 
		ELSE '%s' END AS INDIRIZZO 
FROM 
	SCHEDA_EDIFICIO AS sch JOIN LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA loc_ind ON loc_ind.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ = sch.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ 
	JOIN (%s) AS ind ON ind.ID_INDIRIZZO = loc_ind.INDIRIZZO_VIAID_INDIRIZZO 
	LEFT OUTER JOIN (%s) AS com ON com.ISTATCOM = ind.ZZ_COMUNIISTATCOM 
	LEFT OUTER JOIN (%s) AS civ ON civ.INDIRIZZO_VIAID_INDIRIZZO = ind.ID_INDIRIZZO AND civ.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ = sch.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ 
GROUP BY sch.ID
ORDER BY com.NOME, ind.VIA ASC""" % (via_civico_non_valido, via_civico_non_valido, comune_non_valido, query_indirizzi, query_comuni, query_ncivici)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			#self.schedeList: AutomagicallyUpdater.Query( query_localizzazione )	# non funziona, probabile problema in QtSql 
			self.schedeList: AutomagicallyUpdater.Query( query_localizzazione, None, 1 )	# workaround, usa pyspatialite 
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		self.connect(self.apriBtn, SIGNAL("clicked()"), self.apriScheda)
		self.connect(self.schedeList, SIGNAL("itemSelectionChanged()"), self.aggiornaPulsanti)

		self.aggiornaPulsanti()

	def aggiornaPulsanti(self):
		self.apriBtn.setEnabled( self.getValue(self.schedeList) != None )
		self.stampaBtn.setEnabled(False)

	def apriScheda(self):
		from ManagerWindow import ManagerWindow

		schedaID = self.getValue( self.schedeList )
		query = AutomagicallyUpdater.Query( "SELECT GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW FROM SCHEDA_UNITA_VOLUMETRICA WHERE SCHEDA_EDIFICIOID = ?", [ schedaID ] )
		uvID = query.getFirstResult()
		if uvID == None:
			QMessageBox.warning(self, "Errore", "La scheda selezionata non ha alcuna UV associata! ")
			return

		ManagerWindow.apriScheda(uvID)

		self.close()
