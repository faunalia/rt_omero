
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.grpMantoCoperturaUnitaVolumetrica_ui import Ui_GroupBox
from AutomagicallyUpdater import *

class GrpMantoCoperturaUnitaVolumetrica(QGroupBox, MappingOne2One, Ui_GroupBox):

	def __init__(self, parent=None):
		QGroupBox.__init__(self, parent)
		MappingOne2One.__init__(self, "MANTO_COPERTURA_UNITA_VOLUMETRICA")
		self.setupUi(self)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_TIPO_MANTO_COPERTURAID: AutomagicallyUpdater.ZZTable( "ZZ_TIPO_MANTO_COPERTURA" ),
			self.ZZ_STATO_CONSERVAZIONE_MANTOID: AutomagicallyUpdater.ZZTable( "ZZ_STATO_CONSERVAZIONE_MANTO" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			(self.ALTRO_MANTO_COPERTURA, AutomagicallyUpdater.OPTIONAL),
			self.ZZ_TIPO_MANTO_COPERTURAID,
			(self.DESCRIZIONE_INCONGRUENZA, AutomagicallyUpdater.OPTIONAL), 
			self.ZZ_STATO_CONSERVAZIONE_MANTOID
		]
		self.setupValuesUpdater(childrenList)

		self.connect(self.ZZ_TIPO_MANTO_COPERTURAID, SIGNAL("currentIndexChanged(int)"), self.abilitaAltroManto)
		self.abilitaAltroManto()

	def abilitaAltroManto(self):
		enabler = self.ZZ_TIPO_MANTO_COPERTURAID.currentText().endsWith('Altro')
		self.ALTRO_MANTO_COPERTURA.setEnabled(enabler)

