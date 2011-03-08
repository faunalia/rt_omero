# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from WdgCaratteristicheArchitettonicheChild import WdgCaratteristicheArchitettonicheChild
from AutomagicallyUpdater import *

class WdgCaratteristicheArchitettonicheOscuramenti(WdgCaratteristicheArchitettonicheChild):

	def __init__(self, parent=None):
		multipleChoiseParams = ["ZZ_TIPO_OSCURAMENTI_OSCURAMENTI", "ZZ_TIPO_OSCURAMENTIID", "OSCURAMENTIID", "ZZ_TIPO_OSCURAMENTI"]
		WdgCaratteristicheArchitettonicheChild.__init__(self, parent, "OSCURAMENTI", None, multipleChoiseParams)
		self.showOtherInfos(True)

		# modifica il nome degli oggetti
		self.ZZ_TIPO.setObjectName("ZZ_TIPO_OSCURAMENTI_OSCURAMENTI")
		self.ALTRO.setObjectName("ALTRO_OSCURAMENTO")

	def getNomeCaratteristica(self):
		return "Oscuramenti"

