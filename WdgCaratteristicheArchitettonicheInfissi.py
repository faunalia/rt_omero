# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from WdgCaratteristicheArchitettonicheChild import WdgCaratteristicheArchitettonicheChild
from AutomagicallyUpdater import *

class WdgCaratteristicheArchitettonicheInfissi(WdgCaratteristicheArchitettonicheChild):

	def __init__(self, parent=None):
		multipleChoiseParams = ["ZZ_TIPO_INFISSI_INFISSI", "ZZ_TIPO_INFISSIID", "INFISSIID", "ZZ_TIPO_INFISSI"]
		WdgCaratteristicheArchitettonicheChild.__init__(self, parent, "INFISSI", None, multipleChoiseParams)
		self.showOtherInfos(True)

		# modifica il nome degli oggetti
		self.ZZ_TIPO.setObjectName("ZZ_TIPO_INFISSI_INFISSI")
		self.ALTRO.setObjectName("ALTRO_INFISSO")

