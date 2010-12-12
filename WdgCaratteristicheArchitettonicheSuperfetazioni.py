# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from WdgCaratteristicheArchitettonicheChild import WdgCaratteristicheArchitettonicheChild
from AutomagicallyUpdater import *

class WdgCaratteristicheArchitettonicheSuperfetazioni(WdgCaratteristicheArchitettonicheChild):

	def __init__(self, parent=None):
		multipleChoiseParams = ["ZZ_TIPO_SUPERFETAZIONI_SUPERFETAZIONI", "ZZ_TIPO_SUPERFETAZIONIID", "SUPERFETAZIONI_INCONGRUENZEID", "ZZ_TIPO_SUPERFETAZIONI"]
		WdgCaratteristicheArchitettonicheChild.__init__(self, parent, "SUPERFETAZIONI_INCONGRUENZE", None, multipleChoiseParams)
		self.showOtherInfos(False)

		# modifica il nome degli oggetti
		self.ZZ_TIPO.setObjectName("ZZ_TIPO_SUPERFETAZIONI_SUPERFETAZIONI")
		self.ALTRO.setObjectName("ALTRO_SUPERFETAZIONE_INCONGRUENZA")

