# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from Wdg2FieldsTable import Wdg2FieldsTable
from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import *

class WdgParticelleCatastali(Wdg2FieldsTable):

	def __init__(self, parent=None):
		columns = ( ("FOGLIO", "Foglio"), ("PARTICELLA", "Particella") )
		Wdg2FieldsTable.__init__(self, parent, "RIFERIMENTI_CATASTALI_SCHEDA_EDIFICIO", "SCHEDA_EDIFICIOID", "RIFERIMENTI_CATASTALIIDREF_CATAST", "RIFERIMENTI_CATASTALI", "IDREF_CATAST", columns)

