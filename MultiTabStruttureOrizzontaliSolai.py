# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from MultiTabSection import MultiTabSection
from WdgStruttureOrizzontaliSolai import WdgStruttureOrizzontaliSolai
from AutomagicallyUpdater import *

class MultiTabStruttureOrizzontaliSolai(MultiTabSection):

	def __init__(self, parent=None):
		MultiTabSection.__init__(self, parent, WdgStruttureOrizzontaliSolai, "#", "STRUTTURE_ORIZZONTALI_SOLAI", None, "SCHEDA_EDIFICIOID")
