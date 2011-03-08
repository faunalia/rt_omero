# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from WdgCaratteristicheArchitettonicheChild import WdgCaratteristicheArchitettonicheChild
from AutomagicallyUpdater import *

class WdgCaratteristicheArchitettonicheGronda(WdgCaratteristicheArchitettonicheChild):

	def __init__(self, parent=None):
		multipleChoiseParams = ["ZZ_TIPO_GRONDA_GRONDA", "ZZ_TIPO_GRONDAID", "GRONDAID", "ZZ_TIPO_GRONDA"]
		WdgCaratteristicheArchitettonicheChild.__init__(self, parent, "GRONDA", None, multipleChoiseParams)
		self.showOtherInfos(True)

		# modifica il nome degli oggetti
		self.ZZ_TIPO.setObjectName("ZZ_TIPO_GRONDA_GRONDA")
		self.ALTRO.setObjectName("ALTRO_GRONDA")

	def getNomeCaratteristica(self):
		return "Gronda"

