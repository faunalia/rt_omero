
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgStruttureOrizzontaliSolai_ui import Ui_Form
from AutomagicallyUpdater import *

class WdgStruttureOrizzontaliSolai(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "STRUTTURE_ORIZZONTALI_SOLAI")
		self.setupUi(self)

		self.SCHEDA_EDIFICIOID.hide()

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTEID: AutomagicallyUpdater.ZZTable( "ZZ_TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTE" ), 
			self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID: AutomagicallyUpdater.ZZTable( "ZZ_STATO_CONSERVAZIONE_STRUTTURALE" ),
			self.ZZ_QUALITA_INFORMAZIONEID: AutomagicallyUpdater.ZZTable( "ZZ_QUALITA_INFORMAZIONE" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.SCHEDA_EDIFICIOID,
			self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID, 
			self.ZZ_QUALITA_INFORMAZIONEID, 
			self.ZZ_TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTEID
		]
		self.setupValuesUpdater(childrenList)

	def toHtml(self, index):
		tipologia = map( str, self.ZZ_TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTEID.getValues(False) )
		return """
<table class="green border">
	<tr>
		<td class="title" colspan="4">Strutture orizzontali solai</td>
	</tr>
	<tr class="line">
		<td>Qualit&agrave; dell'informazione</td><td colspan="3" class="value">%s</td>
	</tr>
	<tr class="line">
		<td class="subtitle">Tipologia costruttiva</td><td colspan="3" class="value">%s</td>
	</tr>
	<tr>
		<td>Stato di conservazione</td><td colspan="3" class="value">%s</td>
	</tr>
</table>
""" % ( self.ZZ_QUALITA_INFORMAZIONEID.currentText(), "<br>".join(tipologia), self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID.currentText() )

