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

from ui.wdgSezPrincipale_ui import Ui_Form
from AutomagicallyUpdater import *

class SezPrincipale(QWidget, MappingPart, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingPart.__init__(self, "SCHEDA_EDIFICIO")
		self.setupUi(self)

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.DATA_COMPILAZIONE_SCHEDA, 
			self.RILEVATOREID, 
			(self.NOME_EDIFICIO, AutomagicallyUpdater.OPTIONAL), 
			(self.NOTA_STORICA, AutomagicallyUpdater.OPTIONAL)
		]
		self.setupValuesUpdater(childrenList)

		# carica il valore dell'ultimo rilevatore utilizzato
		self.setValue(self.RILEVATOREID, self._getIDRilevatore())

	def setValue(self, widget, value):
		value = self._getRealValue(value)
		if self._getRealWidget(widget) == self.RILEVATOREID and value != None:
			IDComune = QString(value).remove( QRegExp('\-.*$') )

			query = AutomagicallyUpdater.Query( "SELECT ID, COGNOME, NOME, (SELECT com.NOME || ' (' || prov.NOME || ')' FROM ZZ_PROVINCE AS prov JOIN ZZ_COMUNI AS com ON prov.ISTATPROV = com.ZZ_PROVINCEISTATPROV WHERE com.ISTATCOM = ?) AS \"COMUNE\" FROM RILEVATORE WHERE ID = ?", [ IDComune, value ], 0 )
			self.loadTables(self.RILEVATOREID, query)
		
		AutomagicallyUpdater.setValue(widget, value)

	def setupLoader(self, ID=None):
		MappingPart.setupLoader(self, ID)
		self.setValue(self.schedaID, ID)		

	def refreshId(self, ID=None):
		MappingPart.refreshId(self, ID)
		self.setValue(self.schedaID, ID)

	def toHtml(self):
		comIstat = QString(self._ID).remove( QRegExp('\-.*$') )
		numScheda = QString(self._ID).mid( len(comIstat)+1 ).remove( QRegExp('\_.*$') )

		rilevatoreID = self.getValue(self.RILEVATOREID)
		ril = self.RILEVATOREID.model().record(0)
		cognome = ril.value(1).toString()
		nome = ril.value(2).toString()

		notaStorica = self.getValue(self.NOTA_STORICA)
		if notaStorica == None or len(notaStorica) <= 0:
			newLineClass = ''
			notaStorica = ''
		else:
			newLineClass = ' class="line"'
			notaStorica = u"""
<table class="blue">
	<tr>
		<td>Nota storiografica</td><td class="value">%s</td>
	</tr>
</table>
""" % QString(notaStorica).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('\n', '<br>')


		return QString( u"""
<div id="sez1" class="block">
<p class="section"><span class="scheda">SCHEDA A EDIFICIO </span>SEZIONE A1 - IDENTIFICAZIONE</p>
<div class="border">
<table class="blue">
	<tr class="line">
		<!--<td>ID Scheda</td><td class="value">%s<br><span class="tooltip">COD. ISTAT COMUNE</span></td><td class="value" width="5px">-</td><td class="value">%s<br><span class="tooltip">NUM. SCHEDA</span></td><td class="value" width="5px">_</td><td class="value">%s<br><span class="tooltip">ID_RIL</span></td>-->
		<td>ID Scheda</td><td class="value center">%s<span style="padding: 0 5px;">-</span>%s<span style="padding: 0 5px;">_</span>%s<br><span class="tooltip">COD. ISTAT COMUNE<span style="padding: 0 10px;">-</span>NUM. SCHEDA<span style="padding: 0 10px;">_</span>ID_RIL</span></td>
		<td class="line">Data</td><td class="value">%s<br><span class="tooltip">GG MM AAAA</span></td>
	</tr>
</table>
<table class="blue">
	<tr%s>
		<td>Rilevatori</td><td class="value">%s<br><span class="tooltip">NOME</span></td><td class="value">%s<br><span class="tooltip">COGNOME</span></td>
		<td class="line">ID_RIL</td><td class="value">%s</td>
	</tr>
</table>%s</div>
</div>
""" % (self._ID, comIstat, numScheda, rilevatoreID, self.getValue(self.DATA_COMPILAZIONE_SCHEDA), newLineClass, nome, cognome, rilevatoreID, notaStorica)
)
