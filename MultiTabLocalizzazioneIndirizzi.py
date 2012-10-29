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

from MultiTabSection import MultiTabSection
from WdgLocalizzazioneIndirizzi import WdgLocalizzazioneIndirizzi
from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import *

class MultiTabLocalizzazioneIndirizzi(MultiTabSection):

	def __init__(self, parent=None):
		MultiTabSection.__init__(self, parent, WdgLocalizzazioneIndirizzi, "Indirizzo ", "LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA", "INDIRIZZO_VIAID_INDIRIZZO", "LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ")
		self.setFirstTab()

	def setFirstTab(self):
		self.firstTab = self.tabWidget.widget(0)
		self.tabWidget.setTabText(0, "Indirizzo")

		if self.firstTab.getComune() == None:
			settings = QSettings()
			IDComune = settings.value( "/omero_RT/lastIDComune", QVariant("") ).toString()
			self.firstTab.setComune(IDComune)


	def addTab(self):
		if self.tabWidget.count() > 0: 
			self.tabWidget.setTabText(0, "Indirizzo 1")

		newIndex = MultiTabSection.addTab(self)
		if newIndex <= 0:
			return newIndex

		widget = self.tabWidget.widget(newIndex)
		prevWidget = self.tabWidget.widget(newIndex-1)

		IDComune = prevWidget.getComune()
		widget.setComune(IDComune)
		return newIndex

	def btnDeleteTabClicked(self):
		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()
			self.deleteTab()

		except Exception, e:
			if isinstance(e, ConnectionManager.AbortedException):
				QMessageBox.critical(self, "Errore", e.toString())
				return False
			raise

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

	def deleteTab(self):
		MultiTabSection.deleteTab(self)

		if self.tabWidget.count() <= 1: 
			self.tabWidget.setTabText(0, "Indirizzo")

	def save(self):
		# salva i valori
		if not MappingOne2Many.save(self):
			return False

		# rimuovi i vecchi ID dalle tabella di normalizzazione
		self._deleteValue(self._tableName, { self._parentPkColumn : self._ID })

		# inserisci i nuovi ID nella tabella di normalizzazione evitando i doppioni
		newIDs = []
		for parent, widget in self._recursiveChildrenRefs():
			if isinstance(widget, MappingOne2One):
				if widget._ID in newIDs:
					continue
				newIDs.append( widget._ID )

				values = {
					self._parentPkColumn : self._ID, 
					self._pkColumn : widget._ID
				}
				self._insertValue( values, self._tableName, None )

		return True

	def delete(self):
		# elimina i valori delle tabelle collegate
		for parent, widget in self._recursiveChildrenRefs():
			if not isinstance(widget, MappingOne2One):
				continue
			if not widget.delete():
				return False
		return True
