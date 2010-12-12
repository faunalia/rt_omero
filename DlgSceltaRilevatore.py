# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import qgis.gui
import qgis.core

from ui.dlgSceltaRilevatore_ui import Ui_Dialog
from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import *

class DlgSceltaRilevatore(QDialog, MappingOne2One, Ui_Dialog):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		MappingOne2One.__init__(self)
		self.setupUi(self)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.comuneCombo: AutomagicallyUpdater.Query( "SELECT com.ISTATCOM, com.NOME || ' (' || prov.NOME || ')' FROM ZZ_PROVINCE AS prov JOIN ZZ_COMUNI AS com ON prov.ISTATPROV = com.ZZ_PROVINCEISTATPROV ORDER BY com.NOME, prov.NOME ASC" ),
			self.rilevatoriTable: AutomagicallyUpdater.Query( "SELECT ID, COGNOME, NOME FROM RILEVATORE WHERE ID LIKE ? ORDER BY COGNOME, NOME ASC", [ None ] )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# connetti i segnali agli slot
		self.connect(self.nomeEdit, SIGNAL("textChanged (const QString &)"), self.aggiornaPulsanti)
		self.connect(self.cognomeEdit, SIGNAL("textChanged (const QString &)"), self.aggiornaPulsanti)
		self.connect(self.addRilevatoreBtn, SIGNAL("clicked()"), self.aggiungiRilevatore)
		self.connect(self.delRilevatoreBtn, SIGNAL("clicked()"), self.eliminaRilevatore)
		self.connect(self.comuneCombo, SIGNAL("currentIndexChanged(int)"), self.aggiornaRilevatori)
		self.connect(self.rilevatoriTable.selectionModel(), SIGNAL("selectionChanged(const QItemSelection &, const QItemSelection &)"), self.aggiornaPulsanti)

		self.aggiornaPulsanti()

	def aggiornaPulsanti(self):
		enabler = self.getValue(self.comuneCombo) != None
		self.nuovoRilevatoreGroup.setEnabled( enabler )

		enabler = not (self.nomeEdit.text().isEmpty() or self.nomeEdit.text().isEmpty())
		self.addRilevatoreBtn.setEnabled( enabler )

		enabler = self.getValue(self.rilevatoriTable) != None
		self.delRilevatoreBtn.setEnabled( enabler )

		self.buttonBox.button(QDialogButtonBox.Ok).setEnabled( self.isCompleted() )

	def isCompleted(self):
		return len(self.rilevatoriTable.selectedIndexes()) > 0 and self.comuneCombo.currentIndex() >= 0


	def aggiornaRilevatori(self):
		IDComune = self.getValue(self.comuneCombo)

		params = [ IDComune+'%' ] if IDComune != None else None
		self._widget2action[self.rilevatoriTable].setParams( params )
		self.loadTables(self.rilevatoriTable)

		self.aggiornaPulsanti()


	def eliminaRilevatore(self):
		ID = self.getValue(self.rilevatoriTable)
		if ID == None:
			return

		# elimina il rilevatore
		if None == self._deleteValue( 'RILEVATORE', { 'ID' : ID } ):
			return
		self.loadTables(self.rilevatoriTable)

	def aggiungiRilevatore(self):
		if self.nomeEdit.text().isEmpty() or self.cognomeEdit.text().isEmpty():
			return

		if None == self._insertRilevatore(self.nomeEdit.text(), self.cognomeEdit.text(), self.getValue(self.comuneCombo)):
			return
		self.loadTables(self.rilevatoriTable)

		# pulisci i campi
		self.nomeEdit.clear()
		self.cognomeEdit.clear()


	def exec_(self):
		settings = QSettings()
		self.setValue(self.comuneCombo, self._getIDComune())
		self.setValue(self.rilevatoriTable, self._getIDRilevatore())
		return QDialog.exec_(self)

	def accept(self):
		settings = QSettings()
		settings.setValue( "/omero_RT/lastIDComune", QVariant( self.getValue(self.comuneCombo) ) )
		settings.setValue( "/omero_RT/lastIDRilevatore", QVariant( self.getValue(self.rilevatoriTable) ) )
		return QDialog.accept(self)

