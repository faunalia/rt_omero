# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from MultiTabSection import MultiTabSection
from WdgInterventi import WdgInterventi
from AutomagicallyUpdater import *

class MultiTabInterventi(MultiTabSection):

	def __init__(self, parent=None):
		MultiTabSection.__init__(self, parent, WdgInterventi, "Intervento ", "INTERVENTO_EDIFICIO", None, "SCHEDA_EDIFICIOID")
		self.setFirstTab()

	def setFirstTab(self):
		self.firstTab = self.tabWidget.widget(0)
		self.firstTab.showOtherInfos(True)
		self.tabWidget.setTabText(0, "Generale")

