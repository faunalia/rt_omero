# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgSezLocalizzazione_ui import Ui_Form
from AutomagicallyUpdater import *

class SezLocalizzazione(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "LOCALIZZAZIONE_EDIFICIO")
		self.setupUi(self)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_POSIZIONE_EDIFICIO_AGGREGATOID: AutomagicallyUpdater.ZZTable( "ZZ_POSIZIONE_EDIFICIO_AGGREGATO" ),
			self.ZZ_PROPRIETA_PREVALENTEID: AutomagicallyUpdater.ZZTable( "ZZ_PROPRIETA_PREVALENTE" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			(self.EDIFICIO_ISOLATO, AutomagicallyUpdater.OPTIONAL), 
			self.ZZ_POSIZIONE_EDIFICIO_AGGREGATOID,  
			self.LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA, 
		]
		self.setupValuesUpdater(childrenList)

