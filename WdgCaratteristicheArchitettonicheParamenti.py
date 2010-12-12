# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from WdgCaratteristicheArchitettonicheChild import WdgCaratteristicheArchitettonicheChild
from AutomagicallyUpdater import *

class WdgCaratteristicheArchitettonicheParamenti(WdgCaratteristicheArchitettonicheChild):

	def __init__(self, parent=None):
		multipleChoiseParams = ["ZZ_TIPO_PARAMENTI_ARCHITETTONICI_PARAMENTI", "ZZ_TIPO_PARAMENTI_ARCHITETTONICIID", "PARAMENTIID", "ZZ_TIPO_PARAMENTI_ARCHITETTONICI"]
		WdgCaratteristicheArchitettonicheChild.__init__(self, parent, "PARAMENTI", None, multipleChoiseParams)
		self.showOtherInfos(True)

		# modifica il nome degli oggetti
		self.ZZ_TIPO.setObjectName("ZZ_TIPO_PARAMENTI_ARCHITETTONICI_PARAMENTI")
		self.DESCRIZIONI_INCONGRUENZE.setObjectName("DESCRIZIONE_INCONGRUENZE")
		self.ALTRO.setObjectName("ALTRO_PARAMENTO")
