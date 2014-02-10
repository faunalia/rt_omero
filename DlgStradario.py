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

from ui.dlgStradario_ui import Ui_Dialog
from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import *

class DlgStradario(QDialog, MappingOne2One, Ui_Dialog):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		MappingOne2One.__init__(self)
		self.setupUi(self)

		self.vieTable.setModel( EditVieTableModel() )

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.comuneCombo: AutomagicallyUpdater.Query( "SELECT com.ISTATCOM, com.NOME || ' (' || prov.NOME || ')' FROM ZZ_PROVINCE AS prov JOIN ZZ_COMUNI AS com ON prov.ISTATPROV = com.ZZ_PROVINCEISTATPROV ORDER BY com.NOME, prov.NOME ASC" ),
			self.vieTable: AutomagicallyUpdater.Query( "SELECT ind.ID_INDIRIZZO, ind.TIPO = 'EDITABILE' AS EDITABLE, prov.NOME AS PROVINCIA, com.NOME AS COMUNE, ind.VIA FROM INDIRIZZO_VIA AS ind JOIN ZZ_COMUNI AS com ON ind.ZZ_COMUNIISTATCOM = com.ISTATCOM JOIN ZZ_PROVINCE AS prov ON prov.ISTATPROV = com.ZZ_PROVINCEISTATPROV ORDER BY prov.NOME, com.NOME, ind.VIA ASC", None, 0 )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		self.vieTable.setColumnHidden(1, True)	# hide EDITABLE column

		# connetti i segnali agli slot
		self.connect(self.viaEdit, SIGNAL("textChanged (const QString &)"), self.aggiornaPulsanti)
		self.connect(self.addViaBtn, SIGNAL("clicked()"), self.aggiungiVia)
		self.connect(self.delViaBtn, SIGNAL("clicked()"), self.eliminaVia)

		self.connect(self.vieTable.selectionModel(), SIGNAL("selectionChanged(const QItemSelection &, const QItemSelection &)"), self.caricaVia)
		self.caricaVia()

	def aggiornaPulsanti(self):
		ID = self.getValue(self.vieTable)

		self.delViaBtn.setEnabled( ID != None and self.selectedRowIsEditabile() )

		enabler = self.getValue(self.comuneCombo) != None and not self.viaEdit.text().isEmpty()
		self.addViaBtn.setEnabled( enabler )

	def selectedRowIsEditabile(self):
		# non permettere di cancellare una via non editabile
		selIndexes = self.vieTable.selectedIndexes()
		if len(selIndexes) > 0:
			return self.vieTable.model().isEditable( selIndexes[0].row() )
		return False


	def caricaVia(self):
		IDindirizzo = self.getValue(self.vieTable)
		via = None
		IDcomune = None

		if IDindirizzo != None and self.selectedRowIsEditabile():
			# recupera la via selezionata
			query = AutomagicallyUpdater.Query( "SELECT ZZ_COMUNIISTATCOM, VIA FROM INDIRIZZO_VIA WHERE ID_INDIRIZZO = ?", [ IDindirizzo ] ).getQuery()
			if query.exec_() and query.next():
				IDcomune = str( query.value(0) )
				via = str( query.value(1) )

		self.setValue(self.comuneCombo, IDcomune)
		self.setValue(self.viaEdit, via)

		self.aggiornaPulsanti()

	def aggiornaVie(self):
		self.loadTables(self.vieTable)
		self.connect(self.vieTable.selectionModel(), SIGNAL("selectionChanged(const QItemSelection &, const QItemSelection &)"), self.caricaVia)
		self.caricaVia()


	def eliminaVia(self):
		IDindirizzo = self.getValue(self.vieTable)
		if IDindirizzo == None:	# nessuna via selezionata
			return

		if not self.selectedRowIsEditabile():
			return

		# non eliminare le vie vuote
		via = AutomagicallyUpdater.Query( "SELECT VIA FROM INDIRIZZO_VIA WHERE ID_INDIRIZZO = ?", [IDindirizzo] ).getFirstResult()
		if via == None or via.isEmpty():
			return

		# chiedi conferma all'utente
		numSchede = AutomagicallyUpdater.Query( "SELECT count(*) FROM LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA WHERE INDIRIZZO_VIAID_INDIRIZZO = ?", [IDindirizzo] ).getFirstResult()
		if QMessageBox.Ok != QMessageBox.warning( self, "Eliminazione indirizzo", u"L'indirizzo selezionato è associato a %s schede. Eliminare? L'operazione non è reversibile." % numSchede, QMessageBox.Ok|QMessageBox.Cancel ):
			return

		if self.testModificaVia( self.getValue(self.comuneCombo), '', IDindirizzo ):
			self.aggiornaVie()

	def aggiungiVia(self):
		IDcomune = self.getValue(self.comuneCombo)
		via = str(self.viaEdit.text()).upper()
		if IDcomune == None or via.isEmpty():
			return

		IDindirizzo = self.getValue(self.vieTable)
		if IDindirizzo == None:	# non inserire nuove vie
			return

		# verifica se il nuovo indirizzo esiste già
		nuovoID = AutomagicallyUpdater.Query( "SELECT ID_INDIRIZZO FROM INDIRIZZO_VIA WHERE ZZ_COMUNIISTATCOM = ? AND VIA = ?", [IDcomune, via] ).getFirstResult()
		if nuovoID != None and nuovoID != IDindirizzo:
			# ne esiste già, chiedi se bisogna unirli
			if QMessageBox.Ok != QMessageBox.warning( self, "RT Omero", u"L'indirizzo inserito esiste già. \nSi vuole modificare tutte le schede in modo che \npuntino al nuovo indirizzo?", QMessageBox.Ok|QMessageBox.Cancel ):
				return

		if self.testModificaVia( IDcomune, via, IDindirizzo ):
			self.aggiornaVie()

	def testModificaVia(self, comune, via, ID):
		via = str( via ).upper()
		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# verifica se il nuovo indirizzo esiste già
			nuovoID = AutomagicallyUpdater.Query( "SELECT ID_INDIRIZZO FROM INDIRIZZO_VIA WHERE ZZ_COMUNIISTATCOM = ? AND VIA = ?", [comune, via] ).getFirstResult()

			if nuovoID == None:
				# il nuovo non esiste, aggiorna il vecchio
				self._updateValue( { 'VIA' : via, 'ZZ_COMUNIISTATCOM' : comune }, 'INDIRIZZO_VIA', 'ID_INDIRIZZO', ID )

			elif nuovoID == ID:
				# nessuna modifica, non salvare
				return False

			else:
				# aggiorna i valori nella tabella di normalizzazione
				# se duplicati non aggiornarli (verranno rimossi nella query successiva)
				self._updateValue( { 'INDIRIZZO_VIAID_INDIRIZZO' : nuovoID }, 'LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA', 'INDIRIZZO_VIAID_INDIRIZZO', ID, "LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ NOT IN (SELECT LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ FROM LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA WHERE INDIRIZZO_VIAID_INDIRIZZO = ?)", [nuovoID] )
				# rimuovi quelli non aggiornati nella query precedente poiché sarebbero stati dei duplicati
				self._deleteValue( 'LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA', { 'INDIRIZZO_VIAID_INDIRIZZO' : ID } )

				# aggiorna i civici
				self._updateValue( { 'INDIRIZZO_VIAID_INDIRIZZO' : nuovoID }, 'NUMERI_CIVICI', 'INDIRIZZO_VIAID_INDIRIZZO', ID )
				# elimina il vecchio indirizzo
				self._deleteValue( 'INDIRIZZO_VIA', { 'ID_INDIRIZZO' : ID } )

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", str(e) )
			return False

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

		return True


# disable non-editable rows  
class EditVieTableModel(QSqlQueryModel):
	def __init__(self, parent=None):
		QSqlQueryModel.__init__(self, parent)

	def flags(self, index):
		flags = QSqlQueryModel.flags(self, index)
		if index.isValid() and not self.isEditable( index.row() ):
			flags &= ~Qt.ItemIsEnabled & ~Qt.ItemIsSelectable
		return flags

	#def data(self, index, role = Qt.DisplayRole):
	#	if not index.isValid() or role != Qt.BackgroundRole or self.isEditable( index.row() ):
	#		return QSqlQueryModel.data(self, index, role)
	#	return QVari---ant( QBrush(QColor(210, 210, 210)) )

	def isEditable(self, row):
		sqlRecord = self.record(row)
		return bool( sqlRecord.value(1) )

