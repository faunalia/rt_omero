# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgSezCaratteristicheArchitettoniche_ui import Ui_Form
from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import *

class SezCaratteristicheArchitettoniche(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "CARATTERISTICHE_ARCHITETTONICHE_EDIFICIO")
		self.setupUi(self)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_PROSPETTO_PREVALENTEID: AutomagicallyUpdater.ZZTable( "ZZ_PROSPETTO_PREVALENTE" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.ZZ_PROSPETTO_PREVALENTEID,
			self.PARAMENTIID,
			self.BALCONIID,
			self.OSCURAMENTIID,
			self.INFISSIID,
			self.GRONDAID,
			self.ELEMENTI_DECORATIVIID,
			self.SUPERFETAZIONI_INCONGRUENZEID
		]
		self.setupValuesUpdater(childrenList)

