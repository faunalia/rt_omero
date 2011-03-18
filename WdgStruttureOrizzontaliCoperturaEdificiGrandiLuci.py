# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgStruttureOrizzontaliCoperturaEdificiGrandiLuci_ui import Ui_Form
from AutomagicallyUpdater import *

class WdgStruttureOrizzontaliCoperturaEdificiGrandiLuci(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_GRANDI_LUCI")
		self.setupUi(self)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_TIPOLOGIA_COSTRUTTIVA_COPERTURA_EDIFICI_GRANDI_LUCIID: AutomagicallyUpdater.ZZTable( "ZZ_TIPOLOGIA_COSTRUTTIVA_COPERTURA_EDIFICI_GRANDI_LUCI" ),
			self.ZZ_COMPORTAMENTO_STRUTTURALE_COPERTURAID: AutomagicallyUpdater.ZZTable( "ZZ_COMPORTAMENTO_STRUTTURALE_COPERTURA" ),
			self.ZZ_STATO_CONSERVAZIONE_COPERTURA_EDIFICI_ORDINARIID: AutomagicallyUpdater.Table( "ZZ_STATO_CONSERVAZIONE_COPERTURA_EDIFICI_ORDINARI" ),
			self.ZZ_MATERIALE_COPERTURA_EDIFICI_GRANDI_LUCIID: AutomagicallyUpdater.ZZTable( "ZZ_MATERIALE_COPERTURA_EDIFICI_GRANDI_LUCI" ),
			self.ZZ_QUALITA_INFORMAZIONEID: AutomagicallyUpdater.ZZTable( "ZZ_QUALITA_INFORMAZIONE" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.ZZ_TIPOLOGIA_COSTRUTTIVA_COPERTURA_EDIFICI_GRANDI_LUCIID, 
			(self.ZZ_COMPORTAMENTO_STRUTTURALE_COPERTURAID, AutomagicallyUpdater.OPTIONAL),
			(self.ZZ_STATO_CONSERVAZIONE_COPERTURA_EDIFICI_ORDINARIID, AutomagicallyUpdater.OPTIONAL),
			self.ZZ_MATERIALE_COPERTURA_EDIFICI_GRANDI_LUCIID,
			self.ZZ_QUALITA_INFORMAZIONEID
		]
		self.setupValuesUpdater(childrenList)

	def toHtml(self):
		return QString( u"""
<table class="green border">
	<tr>
		<td class="title" colspan="4">Strutture orizzontali - Copertura > Edifici con grandi luci (capannoni, palestre, piscine, etc.)</td>
	</tr>
	<tr class="line">
		<td>Qualit&agrave; dell'informazione</td><td colspan="3" class="value">%s</td>
	</tr>
	<tr class="line">
		<td class="subtitle">Tipologia costruttiva</td><td class="value">%s</td>
		<td class="subtitle line">Materiale</td><td class="value">%s</td>
	</tr>
	<tr>
		<td>Comportamento strutturale</td><td class="value">%s</td>
		<td class="line">Stato di conservazione</td><td class="value">%s</td>
	</tr>
</table>
""" % ( self.ZZ_QUALITA_INFORMAZIONEID.currentText(), self.ZZ_TIPOLOGIA_COSTRUTTIVA_COPERTURA_EDIFICI_GRANDI_LUCIID.currentText(), self.ZZ_MATERIALE_COPERTURA_EDIFICI_GRANDI_LUCIID.currentText(), self.ZZ_COMPORTAMENTO_STRUTTURALE_COPERTURAID.currentText(), self.ZZ_STATO_CONSERVAZIONE_COPERTURA_EDIFICI_ORDINARIID.currentText() )
)
