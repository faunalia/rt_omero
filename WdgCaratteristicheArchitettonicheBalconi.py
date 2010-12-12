# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from WdgCaratteristicheArchitettonicheChild import WdgCaratteristicheArchitettonicheChild
from AutomagicallyUpdater import *

class WdgCaratteristicheArchitettonicheBalconi(WdgCaratteristicheArchitettonicheChild):

	def __init__(self, parent=None):
		multipleChoiseParams = ["ZZ_TIPO_BALCONI_BALCONI", "ZZ_TIPO_BALCONIID", "BALCONIID", "ZZ_TIPO_BALCONI"]
		WdgCaratteristicheArchitettonicheChild.__init__(self, parent, "BALCONI", None, multipleChoiseParams)
		self.showOtherInfos(True)

		# modifica il nome degli oggetti
		self.ZZ_TIPO.setObjectName("ZZ_TIPO_BALCONI_BALCONI")
		self.ALTRO.setObjectName("ALTRO_BALCONE")

