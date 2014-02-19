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

from ui.multipleChoise2Lists_ui import Ui_MultipleChoise
from AutomagicallyUpdater import *
from Utils import Porting

class MultipleChoise2Lists(QWidget, MappingMany2Many, Ui_MultipleChoise):

	def __init__(self, parent=None, table=None, pk=None, parentPk=None, tableWithValues=None):
		QWidget.__init__(self, parent)
		MappingMany2Many.__init__(self, table, pk, parentPk, tableWithValues)
		self.setupUi(self)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.nonSelezionateList: AutomagicallyUpdater.ZZTable( self._tableWithValues, None, None, 0 ), 
			self.selezionateList: AutomagicallyUpdater.ZZTable( self._tableWithValues, None, None, 0 )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTablesAndInit()

		self.storedValues = []

		self.connect(self.btnAdd, SIGNAL("clicked()"), self.aggiungiSelezionata)
		self.connect(self.btnDel, SIGNAL("clicked()"), self.eliminaSelezionata)

		self.connect(self.nonSelezionateList.selectionModel(), SIGNAL("selectionChanged(const QItemSelection &, const QItemSelection &)"), self.aggiornaPulsanti)
		self.connect(self.selezionateList.selectionModel(), SIGNAL("selectionChanged(const QItemSelection &, const QItemSelection &)"), self.aggiornaPulsanti)

		self.aggiornaPulsanti()

	def onClosing(self):
		for val in self.storedValues:
			self.storedValues.remove(val)
			del val
		del self.storedValues
		MappingMany2Many.onClosing(self)		


	def selectionChanged(self):
		self.emit( SIGNAL("selectionChanged()") )

	def isSelected(self, text, matchFlags):
		row=0
		model = self.selezionateList.model()
		while model.hasIndex(row,0):
			if not self.selezionateList.isRowHidden(row):
				itemtext = Porting.str( model.record(row).value(1) )
				if matchFlags == Qt.MatchStartsWith:
					if itemtext.startswith( text ):
						return True
				elif matchFlags == Qt.MatchEndsWith:
					if itemtext.endswith( text ):
						return True
				else:
					raise RuntimeError( "Error in MultipleChoise2List: matchFlags %s NOT IMPLEMENTED YET!" % matchFlags )
			row = row + 1
		return False

	def aggiornaPulsanti(self):
		enabler = AutomagicallyUpdater.getValue(self.nonSelezionateList) != None
		self.btnAdd.setEnabled( enabler )

		enabler = AutomagicallyUpdater.getValue(self.selezionateList) != None
		self.btnDel.setEnabled( enabler )


	def getValues(self, getIDs=True):
		values = []
		row=0
		model = self.selezionateList.model()
		while model.hasIndex(row,0):
			if not self.selezionateList.isRowHidden(row):
				values.append( Porting.str( model.record(row).value(0 if getIDs else 1) ) )
			row = row + 1

		return values

	def setValues(self, values):
		if values == None:
			values = []
		if not hasattr(values, '__iter__'):
			values = [values]
		checkValues = [unicode(v) for v in values]
		
		row=0
		model = self.selezionateList.model()
		while model.hasIndex(row,0):
			hide = unicode(model.record(row).value(0)) in checkValues
			self.selezionateList.setRowHidden(row, not hide)
			self.nonSelezionateList.setRowHidden(row, hide)
			row = row + 1

		self.storedValues = values
		self.selectionChanged()

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
		self.selectionChanged()

	def eliminaSelezionata(self):
		self.moveItem(self.selezionateList, self.nonSelezionateList)
		self.selectionChanged()

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
				ID = Porting.str( model.record(row).value(0) )
				ID = ID if ID != "None" else None
				if not ID in oldIDs:
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

