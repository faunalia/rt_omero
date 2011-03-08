
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from WdgCaratteristicheArchitettonicheChild import WdgCaratteristicheArchitettonicheChild
from AutomagicallyUpdater import *

class WdgCaratteristicheArchitettonicheElemDecorativi(WdgCaratteristicheArchitettonicheChild):

	def __init__(self, parent=None):
		multipleChoiseParams = ["ZZ_TIPO_ELEMENTI_DECORATIVI_ELEMENTI_DECORATIVI", "ZZ_TIPO_ELEMENTI_DECORATIVIID", "ELEMENTI_DECORATIVIID", "ZZ_TIPO_ELEMENTI_DECORATIVI"]
		WdgCaratteristicheArchitettonicheChild.__init__(self, parent, "ELEMENTI_DECORATIVI", None, multipleChoiseParams)
		self.showOtherInfos(True)

		# modifica il nome degli oggetti
		self.ZZ_TIPO.setObjectName("ZZ_TIPO_ELEMENTI_DECORATIVI_ELEMENTI_DECORATIVI")
		self.ALTRO.setObjectName("ALTRO_ELEMENTO_DECORATIVO")

	def getNomeCaratteristica(self):
		return "Elem. arch. decorativi"

