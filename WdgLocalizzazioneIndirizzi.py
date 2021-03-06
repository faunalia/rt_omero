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

import re

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui.wdgLocalizzazioneIndirizzi_ui import Ui_Form
from AutomagicallyUpdater import *
from Utils import Porting

class WdgLocalizzazioneIndirizzi(QWidget, MappingOne2One, Ui_Form):

	INDIRIZZO_NON_VALIDO = 'INDIRIZZO NON VALIDO'
	INDIRIZZO_NON_INSERITO = '<indirizzo non inserito>'

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "INDIRIZZO_VIA")
		self.setupUi(self)

		# mostra le vie che corrispondono all'input dell'utente
		self.VIA.completer().setCompletionMode(QCompleter.PopupCompletion)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_PROVINCEISTATPROV: AutomagicallyUpdater.ZZTable( "ZZ_PROVINCE", "ISTATPROV", "NOME" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.ZZ_COMUNIISTATCOM, 
			self.VIA
		]
		self.setupValuesUpdater(childrenList)

		self.connect(self.ZZ_PROVINCEISTATPROV, SIGNAL("currentIndexChanged(int)"), self.caricaComuni)
		self.connect(self.ZZ_COMUNIISTATCOM, SIGNAL("currentIndexChanged(int)"), self.caricaVie)
		#self.connect(self.VIA, SIGNAL("editTextChanged(const QString &)"), self.caricaCivici)
		self.connect(self.NUMERI_CIVICI, SIGNAL( "dataChanged()" ), self.aggiornaTitoloScheda)

		self.caricaComuni()
		self.caricaVie()


	def caricaComuni(self):
		self.ZZ_COMUNIISTATCOM.clear()
		self.ZZ_COMUNIISTATCOM.setCurrentIndex(-1)

		provincia = self.getValue(self.ZZ_PROVINCEISTATPROV)
		self.ZZ_COMUNIISTATCOM.setEnabled( provincia != None )

		# aggiorna la visualizzazione
		self.setValue(self.ZZ_COMUNIISTATCOM, None)

		if provincia == None:
			return

		# carica i comuni della provincia selezionata
		self.loadTables( self.ZZ_COMUNIISTATCOM, AutomagicallyUpdater.Query( "SELECT ISTATCOM, NOME FROM ZZ_COMUNI WHERE ZZ_PROVINCEISTATPROV = ? ORDER BY NOME ASC", [provincia] ) )

	def caricaVie(self):
		# aggiorna il comune visualizzato nel titolo della scheda
		self.aggiornaTitoloScheda()

		self.VIA.clear()
		self.VIA.setCurrentIndex(-1)

		comune = self.getValue(self.ZZ_COMUNIISTATCOM)
		self.VIA.setEnabled( comune != None )

		# aggiorna la visualizzazione
		self.setValue(self.VIA, None)

		if comune == None:
			return

		# carica le vie del comune selezionato
		self.loadTables( self.VIA, AutomagicallyUpdater.Query( "SELECT ID_INDIRIZZO, VIA FROM INDIRIZZO_VIA WHERE ZZ_COMUNIISTATCOM = ? ORDER BY VIA ASC", [comune] ) )


	def caricaCivici(self):
		self.NUMERI_CIVICI.clear()

		via = self.getValue(self.VIA)
		self.NUMERI_CIVICI.setEnabled( via != None )

		# aggiorna la visualizzazione
		self.setValue(self.NUMERI_CIVICI, None)

		if via == None:
			return

		# carica i civici dell'indirizzo selezionato
		self.NUMERI_CIVICI.loadValues( AutomagicallyUpdater.Query( "SELECT IDNUMEROCIVICO, N_CIVICO, MOD_CIVICO FROM NUMERI_CIVICI WHERE INDIRIZZO_VIAID_INDIRIZZO = ? AND LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ = ?", [via, self._parentRef._ID] ) )

	def aggiornaTitoloScheda(self):
		self.emit( SIGNAL("indirizzoChanged") )


	def getValue(self, widget):
		if self._getRealWidget(widget) != self.VIA:
			return AutomagicallyUpdater.getValue(widget)

		# gestisti a parte il caso del widget VIA così da effettuare un test CaseInsensitive
		value = AutomagicallyUpdater.getValue(widget)
		if value != None:
			index = self.VIA.findData( value )
			if index >= 0:
				return value
			value = re.sub("\s\s+", " ", value.strip())

		index = self.VIA.findText( value if value != None else "", Qt.MatchFixedString )
		if index >= 0:
			ID = self._getRealValue( Porting.str( self.VIA.itemData(index) ) )
			if ID != None:
				return ID

		return self._getRealValue( value )

	def setValue(self, widget, value):
		value = self._getRealValue(value)
		if self._getRealWidget(widget) != self.ZZ_COMUNIISTATCOM or value == None:
			return AutomagicallyUpdater.setValue(widget, value)

		# impostando il comune bisogna aggiornare anche la provincia
		query = AutomagicallyUpdater.Query("SELECT ZZ_PROVINCEISTATPROV FROM ZZ_COMUNI WHERE ISTATCOM = ?", [value])

		self.disconnect(self.ZZ_PROVINCEISTATPROV, SIGNAL("currentIndexChanged(int)"), self.caricaComuni)
		self.setValue(self.ZZ_PROVINCEISTATPROV, query)
		self.caricaComuni()
		self.connect(self.ZZ_PROVINCEISTATPROV, SIGNAL("currentIndexChanged(int)"), self.caricaComuni)
		
		AutomagicallyUpdater.setValue(self.ZZ_COMUNIISTATCOM, value)


	def getComune(self):
		return self.getValue(self.ZZ_COMUNIISTATCOM)

	def setComune(self, comune):
		self.setValue(self.ZZ_COMUNIISTATCOM, comune)


	def setupLoader(self, ID=None):
		MappingOne2One.setupLoader(self, ID)
		IDLocalizzazione = self._parentRef._ID
		self.NUMERI_CIVICI.setupLoader([IDLocalizzazione, ID])

	def delete(self):
		if self._ID == None:
			return

		# elimina dalla tabella di normalizzazione
		filters = {
			self._parentRef._parentPkColumn : self._parentRef._ID, 
			self._parentRef._pkColumn : self._ID
		}
		self._deleteValue(self._parentRef._tableName, filters)

		# non eliminare le vie non editabili
		tipo = AutomagicallyUpdater.Query( "SELECT TIPO FROM %s WHERE %s = ?" % (self._tableName, self._pkColumn), [self._ID] ).getFirstResult()
		if tipo != "EDITABILE":
			return

		# elimina solo se non sono presenti altri riferimenti a questo oggetto
		count = AutomagicallyUpdater.Query( "SELECT count(*) FROM %s WHERE %s = ?" % (self._parentRef._tableName, self._parentRef._pkColumn), [self._ID] ).getFirstResult()
		if count == None or int(count) > 0:
			return

		#elimina i numeri civici
		self.NUMERI_CIVICI.delete()

		# elimina l'indirizzo dalla tabella
		MappingOne2One.delete(self)


	def save(self):
		ID = None

		values = {}
		for parent, widget in self._recursiveChildrenRefs():
			if not isinstance(widget, (MappingOne2Many, MappingMany2Many)):
				value = parent.getValue(widget)

				if widget == self.VIA:
					# non salvare duplicati: controlla che la via non esista già
					if value != None:
						index = self.VIA.findData( value )
						if index >= 0:	# è una via esistente
							ID = value
							break
					else:
						value = ""

					if self._ID != None:	# la via è stata modificata
						tipo = AutomagicallyUpdater.Query( "SELECT TIPO FROM %s WHERE %s = ?" % (self._tableName, self._pkColumn), [self._ID] ).getFirstResult()
						if tipo != "EDITABILE":	# l'indirizzo modificato non è editabile, creane un nuovo
							self._ID = None

						else:
							# se nessun altro punta a questo indirizzo, è possibile modificarlo
							# altrimenti sarà necessario crearne uno nuovo
							count = AutomagicallyUpdater.Query( "SELECT count(*) FROM %s WHERE %s = ?" % (self._parentRef._tableName, self._parentRef._pkColumn), [self._ID] ).getFirstResult()
							if count != None and int(count) > 1:	# salva un nuovo indirizzo
								self._ID = None

					ID = AutomagicallyUpdater.Query( "SELECT %s FROM %s WHERE %s = ? AND %s = ?" % (self._pkColumn, self._tableName, self.ZZ_COMUNIISTATCOM.objectName(), self.VIA.objectName()), [self.getValue(self.ZZ_COMUNIISTATCOM), value]).getFirstResult()
					if ID != None:
						break

				values[widget.objectName()] = value

		if ID == None:	# salva un nuovo edificio
			ID = self._saveValue(values, self._tableName, self._pkColumn, self._ID)
			if ID == None:
				return False

		elif self._ID != ID: 
			# se nessun altro edificio punta a questo indirizzo vuoto ed editabile, eliminalo
			count = AutomagicallyUpdater.Query( "SELECT count(*) FROM %s WHERE %s = ?" % (self._parentRef._tableName, self._parentRef._pkColumn), [self._ID] ).getFirstResult()
			if count != None and int(count) <= 1:	# elimina l'indirizzo se editabile e vuoto
				self._deleteValue(self._tableName, {self._pkColumn: self._ID, "VIA": "", "TIPO": "EDITABILE"})

		self._ID = ID

		IDLocalizzazione = self._parentRef._ID
		self.NUMERI_CIVICI._ID = [IDLocalizzazione, self._ID]
		self.NUMERI_CIVICI.save()

		return True


	def toHtml(self, index):
		civici = self.NUMERI_CIVICI.getValues(False)
		civici = map(lambda x: (x[0] if x[0] != None else "") + (x[1] if x[1] != None else ""), civici)
		return u"""
<table class="blue">
	<tr class="line">
		<td>Provincia</td><td class="value">%s</td>
		<td class="line">Comune</td><td class="value">%s</td>
	</tr>
	<tr class="line">
		<td>Via/Piazza</td><td class="value">%s</td>
		<td class="line">Num. Civici</td><td class="value">%s</td>
	</tr>
</table>
""" % ( self.ZZ_COMUNIISTATCOM.currentText(), self.ZZ_PROVINCEISTATPROV.currentText(), self.VIA.currentText(), ", ".join(civici) )

