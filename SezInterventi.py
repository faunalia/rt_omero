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


