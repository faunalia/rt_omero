
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.grpEpocaCostruttiva_ui import Ui_GroupBox
from AutomagicallyUpdater import *

class GrpEpocaCostruttiva(QGroupBox, MappingPart, Ui_GroupBox):

	def __init__(self, parent=None):
		QGroupBox.__init__(self, parent)
		MappingOne2One.__init__(self, "SCHEDA_EDIFICIO")
		self.setupUi(self)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID: AutomagicallyUpdater.ZZTable( "ZZ_QUALITA_INFORMAZIONE" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.INIZIO_EPOCA_COSTRUTTIVA,
			self.FINE_EPOCA_COSTRUTTIVA, 
			self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID
		]
		self.setupValuesUpdater(childrenList)


