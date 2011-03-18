# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgSezLocalizzazione_ui import Ui_Form
from AutomagicallyUpdater import *

class SezLocalizzazione(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "LOCALIZZAZIONE_EDIFICIO")
		self.setupUi(self)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_POSIZIONE_EDIFICIO_AGGREGATOID: AutomagicallyUpdater.ZZTable( "ZZ_POSIZIONE_EDIFICIO_AGGREGATO" ),
			self.ZZ_PROPRIETA_PREVALENTEID: AutomagicallyUpdater.ZZTable( "ZZ_PROPRIETA_PREVALENTE" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			(self.EDIFICIO_ISOLATO, AutomagicallyUpdater.OPTIONAL), 
			self.ZZ_POSIZIONE_EDIFICIO_AGGREGATOID,  
			self.LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA, 
		]
		self.setupValuesUpdater(childrenList)

	def toHtml(self):
		catastali = self.PARTICELLE_CATASTALI.getValues(False)
		fogli = QStringList() << map(lambda x: x[0] if x[0] != None else "", catastali)
		particelle = QStringList() << map(lambda x: x[1] if x[1] != None else "", catastali)
		isolato = self.getValue(self.EDIFICIO_ISOLATO)
		return QString( u"""
<div id="sez2" class="block">
<p class="section">SEZIONE A2 - LOCALIZZAZIONE DELL'EDIFICIO</p>
<div class="border">
%s
<table class="blue">
	<tr class="line">
		<td class="subtitle">Riferimenti catastali</td>
		<td class="line">Foglio</td><td class="value">%s</td>
		<td class="line">Particelle</td><td class="value">%s</td>
	</tr>
	<tr class="line">
		<td>Edificio isolato</td><td class="value">%s</td>
		<td colspan="2" class="line">Posizione dell'edificio nell'aggregato strutturale</td><td class="value">%s</td>
	</tr>
	<tr>
		<td>Numero unit&agrave immobiliari</td><td class="value">%s</td>
		<td colspan="2" class="line">Propriet&agrave prevalente</td><td class="value">%s</td>
	</tr>
</table>
</div>
</div>
""" % ( self.LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA.toHtml(), fogli.join("<br>"), particelle.join("<br>"), "SI" if isolato else "NO", self.ZZ_POSIZIONE_EDIFICIO_AGGREGATOID.currentText(), self.getValue(self.NUM_UNITA_IMMOBILIARI), self.ZZ_PROPRIETA_PREVALENTEID.currentText() )
)
