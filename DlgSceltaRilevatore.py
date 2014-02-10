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

from ui.dlgSceltaRilevatore_ui import Ui_Dialog
from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import *
from ManagerWindow import ManagerWindow

class DlgSceltaRilevatore(QDialog, MappingOne2One, Ui_Dialog):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		MappingOne2One.__init__(self)
		self.setupUi(self)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.comuneCombo: AutomagicallyUpdater.Query( "SELECT com.ISTATCOM, com.NOME || ' (' || prov.NOME || ')' FROM ZZ_PROVINCE AS prov JOIN ZZ_COMUNI AS com ON prov.ISTATPROV = com.ZZ_PROVINCEISTATPROV ORDER BY com.NOME, prov.NOME ASC" ),
			self.rilevatoriTable: AutomagicallyUpdater.Query( "SELECT ID, COGNOME, NOME FROM RILEVATORE WHERE ID LIKE ? ORDER BY COGNOME, NOME ASC", [ None ], 0 )
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

		enabler = not self.nomeEdit.text().isEmpty() and not self.cognomeEdit.text().isEmpty()
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
		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()
			if not self._deleteValue( 'RILEVATORE', { 'ID' : ID } ):
				return

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", e)
			return False

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

		self.loadTables( self.rilevatoriTable )

	def aggiungiRilevatore(self):
		if self.nomeEdit.text().isEmpty() or self.cognomeEdit.text().isEmpty():
			return

		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()
			self._insertRilevatore(self.nomeEdit.text(), self.cognomeEdit.text(), self.getValue(self.comuneCombo))

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", e)
			return False

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

		self.loadTables(self.rilevatoriTable)

		# pulisci i campi
		self.nomeEdit.clear()
		self.cognomeEdit.clear()


	def exec_(self):
		settings = QSettings()
		self.setValue(self.comuneCombo, self._getIDComune())
		self.setValue(self.rilevatoriTable, self._getIDRilevatore())

		offline = self.offlineMode()
		self.offlineBtn.setChecked( offline )
		self.onlineBtn.setChecked( not offline )

		return QDialog.exec_(self)

	def accept(self):
		if self.offlineBtn.isChecked() and not self.offlineMode():
			if not self.selectCacheFolder():
				return
			
		settings = QSettings()
		settings.setValue( "/omero_RT/lastIDComune", self.getValue(self.comuneCombo) )
		settings.setValue( "/omero_RT/lastIDRilevatore", self.getValue(self.rilevatoriTable) )

		self.setOfflineMode( self.offlineBtn.isChecked() or not self.onlineBtn.isChecked() )
		return QDialog.accept(self)


	def selectCacheFolder(self):
		subdir = ".omero-cache"

		cache_path = self.getPathToCache()
		if cache_path.isEmpty():
			cache_path = self._getPathToDb()
		else:			
			cache_dir = QDir(cache_path)
			if cache_dir.dirName() == subdir:
				cache_dir.cd( ".." )
				cache_path = cache_dir.absolutePath()

		if ManagerWindow.instance.startedYet:
			caption = u"Seleziona la directory dove salvare la cache"
		else:
			caption = u"Seleziona la directory da dove recuperare la cache"

		cache_path = QFileDialog.getExistingDirectory(self, caption, cache_path )
		if cache_path.isEmpty():
			return False

		cache_dir = QDir( cache_path )

		if ManagerWindow.instance.startedYet:
			if cache_dir.dirName() != subdir:
				cache_dir.mkdir( subdir )
				if not cache_dir.cd( subdir ):
					QMessageBox.critical(self, "RT Omero", "Impossibile scrivere nella directory selezionata.")
					return False

		else:
			if cache_dir.dirName() != subdir and not cache_dir.cd( subdir ):
				QMessageBox.information(self, "RT Omero", "Sottocartella \".omero_cache\" non trovata, parto offline senza strati wms")

		self.setPathToCache( cache_dir.absolutePath() )
		return True

