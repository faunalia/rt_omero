# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from MultiTabInterventi import MultiTabInterventi
from AutomagicallyUpdater import *

class SezInterventi(QWidget, MappingPart):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingPart.__init__(self, "SCHEDA_EDIFICIO")
		self.setupUi()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.INTERVENTO_EDIFICIO.firstTab.EPOCA_COSTRUTTIVA,
			self.INTERVENTO_EDIFICIO
		]
		self.setupValuesUpdater(childrenList)

	def setupUi(self):
		gridLayout = QGridLayout(self)
		self.INTERVENTO_EDIFICIO = MultiTabInterventi(self)
		gridLayout.addWidget(self.INTERVENTO_EDIFICIO, 0, 0, 1, 1)

	def toHtml(self):
		epoca = self.INTERVENTO_EDIFICIO.firstTab.EPOCA_COSTRUTTIVA
		return """
<p class="section">SEZIONE A4 - DATAZIONE INTERVENTI DELL'EDIFICIO</p>
<table class="white border">
	<tr class="line">
		<td colspan="6" class="subtitle">Epoca di impianto</td>
	</tr>
	<tr>
		<td class="subtitle">Inizio della costruzione</td><td class="value">%s</td>
		<td class="subtitle line">Fine della costruzione</td><td class="value">%s</td>
		<td class="line">Qualit&agrave; dell'informazione</td><td class="value">%s</td>
	</tr>
</table>
%s
""" % ( self.getValue(epoca.INIZIO_EPOCA_COSTRUTTIVA), self.getValue(epoca.FINE_EPOCA_COSTRUTTIVA), epoca.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID.currentText(), self.INTERVENTO_EDIFICIO.toHtml() )

