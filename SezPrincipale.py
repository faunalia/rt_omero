# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgSezPrincipale_ui import Ui_Form
from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import *

class SezPrincipale(QWidget, MappingPart, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingPart.__init__(self, "SCHEDA_EDIFICIO")
		self.setupUi(self)

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.DATA_COMPILAZIONE_SCHEDA, 
			self.RILEVATOREID
		]
		self.setupValuesUpdater(childrenList)

		# carica il valore dell'ultimo rilevatore utilizzato
		self.setValue(self.RILEVATOREID, self._getIDRilevatore())

	def setValue(self, widget, value):
		value = self._getRealValue(value)
		if self._getRealWidget(widget) == self.RILEVATOREID and value != None:
			IDComune = QString(value).remove( QRegExp('\-.*$') )

			query = AutomagicallyUpdater.Query( "SELECT ID, COGNOME, NOME, (SELECT com.NOME || ' (' || prov.NOME || ')' FROM ZZ_PROVINCE AS prov JOIN ZZ_COMUNI AS com ON prov.ISTATPROV = com.ZZ_PROVINCEISTATPROV WHERE com.ISTATCOM = ?) AS \"COMUNE\" FROM RILEVATORE WHERE ID = ?", [ IDComune, value ] )
			self.loadTables(self.RILEVATOREID, query)
		
		AutomagicallyUpdater.setValue(widget, value)
		

	def toHtml(self):
		comIstat = QString(self._ID).remove( QRegExp('\-.*$') )
		numScheda = QString(self._ID).mid( len(comIstat)+1 ).remove( QRegExp('\_.*$') )

		rilevatoreID = self.getValue(self.RILEVATOREID)
		ril = self.RILEVATOREID.model().record(0)
		cognome = ril.value(1).toString()
		nome = ril.value(2).toString()

		return """
<div id="sez1" class="block">
<p class="section"><span class="scheda">SCHEDA A EDIFICIO </span>SEZIONE A1 - IDENTIFICAZIONE</p>
<div class="border">
<table class="blue">
	<tr class="line">
		<!--<td>ID Scheda</td><td class="value center">%s<br><span class="tooltip">COD. ISTAT COMUNE <span class="space">-</span> NUM. SCHEDA <span class="space">_</span> ID RILEVATORE</span></td>-->
		<td>ID Scheda</td><td class="value">%s<br><span class="tooltip">COD. ISTAT COMUNE</span></td><td class="value" width="5px">-</td><td class="value">%s<br><span class="tooltip">NUM. SCHEDA</span></td><td class="value" width="5px">_</td><td class="value">%s<br><span class="tooltip">ID_RIL</span></td>
		<td class="line">Data</td><td class="value">%s<br><span class="tooltip">GG MM AAAA</span></td>
	</tr>
</table>
<table class="blue">
	<tr>
		<td>Rilevatori</td><td class="value">%s<br><span class="tooltip">NOME</span></td><td class="value">%s<br><span class="tooltip">COGNOME</span></td>
		<td class="line">ID_RIL</td><td class="value">%s</td>
	</tr>
</table>
</div>
</div>
""" % (self._ID, comIstat, numScheda, rilevatoreID, self.getValue(self.DATA_COMPILAZIONE_SCHEDA), nome, cognome, rilevatoreID)
