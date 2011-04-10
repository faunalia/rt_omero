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

from ui.wdg2FieldsTable_ui import Ui_Form
from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import *

class Wdg2FieldsTable(QWidget, MappingMany2Many, Ui_Form):

	def __init__(self, parent=None, table=None, pk=None, parentPk=None, tableWithValues=None, tableWithValuesPk=None, fields=None):
		QWidget.__init__(self, parent)
		MappingMany2Many.__init__(self, table, pk, parentPk, tableWithValues)
		self._tableWithValuesPkColumn = tableWithValuesPk

		self.columnFields = map(lambda x: x[0], fields)
		self.columnNames = map(lambda x: x[1], fields)

		self.setupUi(self)

		self.table.horizontalHeaderItem(0).setText(self.columnNames[0])
		self.table.horizontalHeaderItem(1).setText(self.columnNames[1])

		self.connect(self.btnAdd, SIGNAL("clicked()"), self.addNewChild)
		self.connect(self.btnDel, SIGNAL("clicked()"), self.rimuoviVoce)
		self.connect(self.table, SIGNAL("itemSelectionChanged()"), self.aggiornaPulsanti)
		self.connect(self.table, SIGNAL("itemChanged(QTableWidgetItem *)"), self.dataChanged )
		self.aggiornaPulsanti()

	def onClosing(self):
		for col in self.columnFields:
			self.columnFields.remove(col)
			del col
		del self.columnFields
		for col in self.columnNames:
			self.columnNames.remove(col)
			del col
		del self.columnNames
		MappingMany2Many.onClosing(self)

	def dataChanged(self):
		self.emit( SIGNAL("dataChanged()") )

	def aggiornaPulsanti(self):
		enabler = len(self.table.selectedRanges()) > 0
		self.btnDel.setEnabled( enabler )

	def rimuoviVoce(self, row=None):
		if row == None:
			selItems = self.table.selectedRanges()
			if len(selItems) <= 0:
				return

			row = selItems[0].topRow()

		if self._ID != None:
			# rimuovi dal db
			item = self.table.item(row, 0)
			if item != None:
				ID = item.data( Qt.UserRole ).toString()
				if ID != None:
					ConnectionManager.startTransaction()
					# elimina il valore
					self._deleteValue( self._tableWithValues, { self._tableWithValuesPkColumn : ID } )
					# elimina la riga dalla tabella di normalizzazione
					values = {
						self._pkColumn : self._ID,
						self._parentPkColumn : ID
					}
					self._deleteValue( self._tableName, values )
					ConnectionManager.endTransaction()

		# rimuovi dalla vista
		self.table.removeRow(row)
		self.dataChanged()

	def rowToString(self, row=0):
		string = QString()

		if self.table.rowCount() <= 0:
			return string

		row = 0

		item1 = self.table.item(row, 0)
		item2 = self.table.item(row, 1)
		if item1 != None:
			string += item1.text()
		if item2 != None:
			string += item2.text()

		return string

	def getValues(self, getIDs=True):
		values = []
		for row in range(self.table.rowCount()):
			item1 = self.table.item(row, 0)
			item2 = self.table.item(row, 1)
			if item1 == None:
				continue

			values.append( item1.data(Qt.UserRole).toString() if getIDs else (item1.text(), item2.text() if item2 != None else None) )
		return values

	def clear(self):
		for i in range(self.table.rowCount()):
			self.table.removeRow(0)
		self.dataChanged()

	def addNewChild(self, ID=None, first=None, second=None):
		# assicurati che le modifiche vengano committate
		self.table.setCurrentItem(None)

		newRow = self.table.rowCount()
		self.table.insertRow(newRow)

		if ID != None:
			if first != None:
				item1 = QTableWidgetItem(first)
				item1.setData( Qt.UserRole, QVariant(ID) )
				self.table.setItem(newRow, 0, item1)

			if second != None:
				item2 = QTableWidgetItem(second)
				self.table.setItem(newRow, 1, item2)

		self.dataChanged()
		return True

	def loadValues(self, action=None):
		if action == None:
			if self._ID == None:
				return
			fields = QStringList()
			for c in self.columnFields:
				fields << "t1.%s" % c
			action = AutomagicallyUpdater.Query( "SELECT t1.%s, %s FROM %s AS t1 JOIN %s AS t2 ON t1.%s = t2.%s WHERE t2.%s = ?" % (self._tableWithValuesPkColumn, fields.join(", "), self._tableWithValues, self._tableName, self._tableWithValuesPkColumn, self._parentPkColumn, self._pkColumn), [self._ID] )

		query = action.getQuery()
		if query == None:
			return None
		if not query.exec_():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self.table )
			return

		self.clear()

		while query.next():
			ID = query.value(0).toString()
			first = query.value(1).toString()
			second = query.value(2).toString()
			self.addNewChild(ID, first, second)


	def save(self):
		if self._ID == None:
			return False

		# rimuovi i vecchi ID dalla tabella di normalizzazione
		values = {
			self._pkColumn : self._ID,
		}
		self._deleteValue(self._tableName, values, None)

		# assicurati che le modifiche vengano committate
		self.table.setCurrentItem(None)

		for row in range(self.table.rowCount()):
			item1 = self.table.item(row, 0)
			item2 = self.table.item(row, 1)
			if item1 == None:
				continue

			ID = item1.data( Qt.UserRole ).toString()
			ID = self._getRealValue(ID)

			# salva la riga
			values = {
				self.columnFields[0] : item1.text(), 
				self.columnFields[1] : item2.text() if item2 != None else None
			}
			ID = self._saveValue(values, self._tableWithValues, self._tableWithValuesPkColumn, ID)
			if ID == None:
				return False

			item1.setData( Qt.UserRole, QVariant(ID) if ID != None else QVariant() )

			# inserisci i nuovi ID nella tabella di normalizzazione
			values = {
				self._pkColumn : self._ID,
				self._parentPkColumn : ID
			}
			self._insertValue(values, self._tableName, None)

		return True

	def delete(self):
		if self._ID == None:
			return

		# rimuovi tutti quelli riferiti dalla tabella padre
		for row in range(self.table.rowCount()):
			item1 = self.table.item(row, 0)
			if item1 == None:
				continue

			ID = item1.data( Qt.UserRole ).toString()
			ID = self._getRealValue(ID)
			self._deleteValue( self._tableWithValues, { self._tableWithValuesPkColumn : ID } )

		# rimuovi tutti quelli presenti nella tabella di normalizzazione
		self._deleteValue( self._tableName, { self._pkColumn : self._ID } )


	class SpinBoxDelegate(QStyledItemDelegate):
		def createEditor(self, parent, option, index):
			if index.column() == 0:
				editor = QSpinBox(parent)
				editor.setRange(1, 99999)
				return editor
			else:
				return QStyledItemDelegate.createEditor(parent, option, index)

		def setEditorData(self, editor, index):
			if index.column() == 0:
				value = index.data().toInt()
				value = value[0] if value[1] == True else 1
					
				editor.setValue(value)
			else:
				QStyledItemDelegate.setEditorData(editor, index)

		def setModelData(self, editor, model, index):
			if index.column() == 0:
				value = editor.value()
				model.setData(index, value)
			else:
				QStyledItemDelegate.setModelData(editor, model, index)

