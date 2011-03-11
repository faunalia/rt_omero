# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgSezCaratteristicheStrutturali_ui import Ui_Form
from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import *

class SezCaratteristicheStrutturali(QWidget, MappingPart, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingPart.__init__(self, "SCHEDA_EDIFICIO")
		self.setupUi(self)

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.STRUTTURE_PORTANTI_VERTICALIID,
			self.STRUTTURE_ORIZZONTALI_SOLAI
		]
		self.setupValuesUpdater(childrenList)

	def toHtml(self):
		return """
<div id="sez6" class="block">
<p class="section">SEZIONE A6 - CARATTERISTICHE STRUTTURALI</p>
%s %s
</div>
""" % ( self.STRUTTURE_PORTANTI_VERTICALIID.toHtml(), self.STRUTTURE_ORIZZONTALI_SOLAI.toHtml() )
