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

from AutomagicallyUpdater import *

class MultipleChoiseCheckList(QWidget, MappingMany2Many):

	def __init__(self, parent=None, table=None, pk=None, parentPk=None, tableWithValues=None):
		QWidget.__init__(self, parent)
		MappingMany2Many.__init__(self, table, pk, parentPk, tableWithValues)
		self.setupUi()

		if self._tableWithValues != None:
			# carica i widget multivalore con i valori delle relative tabelle
			tablesDict = {
				self.list: AutomagicallyUpdater.ZZTable( self._tableWithValues )
			}
			self.setupTablesUpdater(tablesDict)
		self.loadTablesAndInit()

		self.storedValues = []

		self.connect(self.list, SIGNAL("itemChanged(QListWidgetItem *)"), self.selectionChanged)

	def onClosing(self):
		for val in self.storedValues:
			self.storedValues.remove(val)
			del val
		del self.storedValues
		MappingMany2Many.onClosing(self)


	def selectionChanged(self):
		self.emit( SIGNAL("selectionChanged()") )

	def isSelected(self, text, matchFlags):
		itemsFound = self.list.findItems(text, matchFlags)
		return len(itemsFound) > 0 and itemsFound[0].checkState() == Qt.Checked

	def getValues(self, getIDs=True):
		values = []
		for row in range(self.list.count()):
			item = self.list.item(row)
			if item.checkState() == Qt.Checked:
				values.append( str( item.data(Qt.UserRole) ) if getIDs else item.text() )

		return values

	def setValues(self, values):
		if values == None:
			values = []
		if not hasattr(values, '__iter__'):
			values = [values]

		for row in range(self.list.count()):
			item = self.list.item(row)
			enabler = item.data(Qt.UserRole) in values
			item.setCheckState( Qt.Checked if enabler else Qt.Unchecked )

		self.storedValues = values

	def loadTablesAndInit(self):
		MappingMany2Many.loadTables(self)

		# visualizza la checkbox di ogni voce nella lista
		for row in range(self.list.count()):
			item = self.list.item(row)
			item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled )
			item.setCheckState(Qt.Unchecked)

	def save(self):
		if self._ID == None:
			return False

		oldIDs = self.storedValues
		newIDs = []

		for row in range(self.list.count()):
			item = self.list.item(row)
			if item.checkState() == Qt.Checked:
				ID = str( item.data(Qt.UserRole) )
				if not ID in oldIDs:
					values = {
						self._pkColumn : ID, 
						self._parentPkColumn : self._ID
					}
					self._insertValue(values, self._tableName, None)

				newIDs.append(ID)

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


	def setupUi(self):
		gridLayout = QGridLayout(self)
		self.list = QListWidget(self)
		self.list.setObjectName("multipleChoiseCheckList")
		gridLayout.addWidget(self.list, 0, 0, 1, 1)

