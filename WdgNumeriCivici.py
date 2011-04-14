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

from Wdg2FieldsTable import Wdg2FieldsTable
from AutomagicallyUpdater import *

class WdgNumeriCivici(Wdg2FieldsTable):

	def __init__(self, parent=None):
		columns = [ ["N_CIVICO", "Civici"], ["MOD_CIVICO", "Esponente"] ]
		Wdg2FieldsTable.__init__(self, parent, None, "LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ", "INDIRIZZO_VIAID_INDIRIZZO", "NUMERI_CIVICI", "IDNUMEROCIVICO", columns)

		self.table.setItemDelegateForColumn(0, Wdg2FieldsTable.SpinBoxDelegate(self.table))


	def loadValues(self, action=None):
		if action == None:
			if self._ID == None:
				return
			action = AutomagicallyUpdater.Query( "SELECT %s, %s, %s FROM %s WHERE %s = ? AND %s = ?" % (self._tableWithValuesPkColumn, self.columnFields[0], self.columnFields[1], self._tableWithValues, self._pkColumn, self._parentPkColumn), self._ID )

		return Wdg2FieldsTable.loadValues(self, action)

	def _saveValue(self, name2valueDict, table, pk, ID=None):
		name2valueDict[self._pkColumn] = self._ID[0]
		name2valueDict[self._parentPkColumn] = self._ID[1]

		# converti i valori nulli per civico e esponente in stringhe vuote
		for c in self.columnFields:
			if name2valueDict.has_key( c ):
				value = name2valueDict[c]
				name2valueDict[c] = value if value != None else ''

		return Wdg2FieldsTable._saveValue(name2valueDict, table, pk, ID)

	def _insertValue(self, name2valueDict, table, pk):
		# table è None quando viene chiamato da Wdg2FieldTable per salvare i valori della tabella di normalizzazione
		if table == None:
			return True

		return Wdg2FieldsTable._insertValue(name2valueDict, table, pk)


	def delete(self):
		if self._ID == None:
			return
		# rimuovi tutti quelli riferiti dalla tabella padre
		filters = {
			self._pkColumn : self._ID[0],
			self._parentPkColumn : self._ID[1]
		}
		self._deleteValue(self._tableWithValues, filters)

	def _deleteValue(self, table, name2valueDict=None, filterStr=None, filterParams=None):
		# table è None quando viene chiamato da Wdg2FieldTable per salvare i valori della tabella di normalizzazione
		if table == None:
			return

		return Wdg2FieldsTable._deleteValue(table, name2valueDict, filterStr, filterParams)

