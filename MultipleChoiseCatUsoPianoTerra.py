# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import qgis.gui
import qgis.core

from MultipleChoise2Lists import MultipleChoise2Lists
from AutomagicallyUpdater import *

class MultipleChoiseCatUsoPianoTerra(MultipleChoise2Lists):

	def __init__(self, parent=None):
		MultipleChoise2Lists.__init__(self, parent, "CATEGORIA_USO_PIANO_TERRA_STATO_UTILIZZO_EDIFICIO", "ZZ_CATEGORIA_USO_PIANO_TERRAID", "STATO_UTILIZZO_EDIFICIOID", "ZZ_CATEGORIA_USO_PIANO_TERRA")

