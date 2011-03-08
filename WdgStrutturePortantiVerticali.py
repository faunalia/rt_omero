
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgStrutturePortantiVerticali_ui import Ui_Form
from AutomagicallyUpdater import *

class WdgStrutturePortantiVerticali(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "STRUTTURE_PORTANTI_VERTICALI")
		self.setupUi(self)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_TIPOLOGIA_COSTRUTTIVAID: AutomagicallyUpdater.ZZTable( "ZZ_TIPOLOGIA_COSTRUTTIVA" ), 
			self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID: AutomagicallyUpdater.ZZTable( "ZZ_STATO_CONSERVAZIONE_STRUTTURALE" ),
			self.ZZ_QUALITA_INFORMAZIONEID: AutomagicallyUpdater.ZZTable( "ZZ_QUALITA_INFORMAZIONE" ),
			self.ZZ_APPARECCHIATURA_MURARIAID: AutomagicallyUpdater.ZZTable( "ZZ_APPARECCHIATURA_MURARIA" ),
			self.ZZ_INCATENAMENTIID: AutomagicallyUpdater.ZZTable( "ZZ_INCATENAMENTI" ),
			self.ZZ_TAMPONATURE_DISTRIBUZIONEID: AutomagicallyUpdater.ZZTable( "ZZ_TAMPONATURE_DISTRIBUZIONE" ),
			self.ZZ_TAMPONATURE_TIPOLOGIAID: AutomagicallyUpdater.ZZTable( "ZZ_TAMPONATURE_TIPOLOGIA" ),
			self.ZZ_TAMPONATURE_PRESENZA_PIANO_DEBOLEID: AutomagicallyUpdater.ZZTable( "ZZ_TAMPONATURE_PRESENZA_PIANO_DEBOLE" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID, 
			self.ZZ_QUALITA_INFORMAZIONEID,
			(self.ZZ_APPARECCHIATURA_MURARIAID, AutomagicallyUpdater.OPTIONAL),
			(self.ZZ_INCATENAMENTIID, AutomagicallyUpdater.OPTIONAL),
			(self.ZZ_TAMPONATURE_DISTRIBUZIONEID, AutomagicallyUpdater.OPTIONAL),
			(self.ZZ_TAMPONATURE_TIPOLOGIAID, AutomagicallyUpdater.OPTIONAL),
			self.ZZ_TAMPONATURE_PRESENZA_PIANO_DEBOLEID, 
			self.ZZ_TIPOLOGIA_COSTRUTTIVAID
		]
		self.setupValuesUpdater(childrenList)

		self.connect(self.ZZ_TIPOLOGIA_COSTRUTTIVAID, SIGNAL("selectionChanged()"), self.abilitaCombo)
		self.abilitaCombo()

	def abilitaCombo(self):
		enabler = self.ZZ_TIPOLOGIA_COSTRUTTIVAID.isSelected("01", Qt.MatchStartsWith)
		self.ZZ_APPARECCHIATURA_MURARIAID.setEnabled(enabler)
		self.ZZ_INCATENAMENTIID.setEnabled(enabler)

	def toHtml(self):
		tipologia = map( str, self.ZZ_TIPOLOGIA_COSTRUTTIVAID.getValues(False) )
		return """
<table class="green border">
	<tr>
		<td class="title" colspan="4">Strutture portanti verticali</td>
	</tr>
	<tr class="line">
		<td>Qualit&agrave; dell'informazione</td><td colspan="3" class="value">%s</td>
	</tr>
	<tr class="line">
		<td class="subtitle">Tipologia costruttiva</td><td colspan="3" class="value">%s</td>
	</tr>
	<tr class="line">
		<td>Stato di conservazione strutturale</td><td colspan="3" class="value">%s</td>
	</tr>
	<tr class="line">
		<td class="subtitle">Apparecchiatura muraria</td><td class="value">%s</td>
		<td class="subtitle line">Incatenamenti</td><td class="value">%s</td>
	</tr>
	<tr class="line">
		<td class="subtitle" colspan="6">Tamponature</td>
	</tr>
	<tr class="line">
		<td>Distribuzione</td><td class="value">%s</td>
		<td class="line">Tipologia</td><td class="value">%s</td>
	</tr>
	<tr class="line">
		<td>Piano debole</td><td colspan="3" class="value">%s</td>
	</tr>
</table>
""" % ( self.ZZ_QUALITA_INFORMAZIONEID.currentText(), "<br>".join(tipologia), self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID.currentText(), self.ZZ_APPARECCHIATURA_MURARIAID.currentText(), self.ZZ_INCATENAMENTIID.currentText(), self.ZZ_TAMPONATURE_DISTRIBUZIONEID.currentText(), self.ZZ_TAMPONATURE_TIPOLOGIAID.currentText(), self.ZZ_TAMPONATURE_PRESENZA_PIANO_DEBOLEID.currentText() )
