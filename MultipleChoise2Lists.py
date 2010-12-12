# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import qgis.gui
import qgis.core

from ui.multipleChoise2Lists_ui import Ui_MultipleChoise
from AutomagicallyUpdater import *

class MultipleChoise2Lists(QWidget, MappingMany2Many, Ui_MultipleChoise):

	def __init__(self, parent=None, table=None, pk=None, parentPk=None, tableWithValues=None):
		QWidget.__init__(self, parent)
		MappingMany2Many.__init__(self, table, pk, parentPk, tableWithValues)
		self.setupUi(self)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.nonSelezionateList: AutomagicallyUpdater.ZZTable( self._tableWithValues ), 
			self.selezionateList: AutomagicallyUpdater.ZZTable( self._tableWithValues )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTablesAndInit()

		self.storedValues = []

		self.connect(self.btnAdd, SIGNAL("clicked()"), self.aggiungiSelezionata)
		self.connect(self.btnDel, SIGNAL("clicked()"), self.eliminaSelezionata)

		self.connect(self.nonSelezionateList.selectionModel(), SIGNAL("selectionChanged(const QItemSelection &, const QItemSelection &)"), self.aggiornaPulsanti)
		self.connect(self.selezionateList.selectionModel(), SIGNAL("selectionChanged(const QItemSelection &, const QItemSelection &)"), self.aggiornaPulsanti)

		self.aggiornaPulsanti()

	def aggiornaPulsanti(self):
		enabler = AutomagicallyUpdater.getValue(self.nonSelezionateList) != None
		self.btnAdd.setEnabled( enabler )

		enabler = AutomagicallyUpdater.getValue(self.selezionateList) != None
		self.btnDel.setEnabled( enabler )


	def getValues(self):
		values = []
		row=0
		model = self.selezionateList.model()
		while model.hasIndex(row,0):
			if not self.selezionateList.isRowHidden(row):
				values.append( model.record(row).value(0).toString() )
			row = row + 1

		return values

	def setValues(self, values):
		if values == None:
			values = []
		if not hasattr(values, '__iter__'):
			values = [values]

		row=0
		model = self.selezionateList.model()
		while model.hasIndex(row,0):
			hide = model.record(row).value(0) in values
			self.selezionateList.setRowHidden(row, not hide)
			self.nonSelezionateList.setRowHidden(row, hide)
			row = row + 1

		self.storedValues = values
		self.emit( SIGNAL( "selectedValuesChanged()" ) )

	def loadTablesAndInit(self):
		MappingMany2Many.loadTables(self)

		# nascondi tutte le righe di selezionateList
		row=0
		model = self.selezionateList.model()
		while model.hasIndex(row,0):
			self.selezionateList.setRowHidden(row, True)
			row = row + 1

	def aggiungiSelezionata(self):
		self.moveItem(self.nonSelezionateList, self.selezionateList)
		self.emit( SIGNAL( "selectedValuesChanged()" ) )

	def eliminaSelezionata(self):
		self.moveItem(self.selezionateList, self.nonSelezionateList)
		self.emit( SIGNAL( "selectedValuesChanged()" ) )

	def moveItem(self, fromList, toList):
		selIndexes = fromList.selectedIndexes()
		if len(selIndexes) <= 0:
			return

		value = MappingMany2Many.getValue(fromList)
		if value == None:
			return

		row = selIndexes[0].row()
		toList.setRowHidden(row, False)
		fromList.setRowHidden(row, True)

		self.aggiornaPulsanti()

	def save(self):
		if self._ID == None:
			return False

		oldIDs = self.storedValues
		newIDs = []

		row = 0
		model = self.selezionateList.model()
		while model.hasIndex(row,0):
			if not self.selezionateList.isRowHidden(row):
				ID = model.record(row).value(0).toString()

				values = {
					self._pkColumn : ID, 
					self._parentPkColumn : self._ID
				}
				self._insertValue(values, self._tableName, None)
				newIDs.append(ID)

			row = row + 1

		# rimuovi dal db quelli eliminati
		for ID in oldIDs:
			if ID in newIDs:
				continue

			filters = {
				self._pkColumn : ID, 
				self._parentPkColumn : self._ID
			}
			self._deleteValue(self._tableName, filters)

		self.storedValues = newIDs
		return True

	def delete(self):
		self._deleteValue( self._tableName, { self._parentPkColumn : self._ID } )
