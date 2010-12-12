# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgInterventi_ui import Ui_Form
from AutomagicallyUpdater import *

class WdgInterventi(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "INTERVENTO_EDIFICIO")
		self.setupUi(self)
		self.showOtherInfos(False)

		self.SCHEDA_EDIFICIOID.hide()

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_QUALITA_INFORMAZIONEID: AutomagicallyUpdater.ZZTable( "ZZ_QUALITA_INFORMAZIONE" ),
			self.ZZ_TIPO_INTERVENTOID: AutomagicallyUpdater.ZZTable( "ZZ_TIPO_INTERVENTO" ),
			self.ZZ_NORMATIVA_SISMICAID: AutomagicallyUpdater.ZZTable( "ZZ_NORMATIVA_SISMICA" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.SCHEDA_EDIFICIOID, 
			(self.ANNO_PROGETTAZIONE, AutomagicallyUpdater.OPTIONAL),
			self.ZZ_QUALITA_INFORMAZIONEID,
			(self.DESCRIZ_INTERV, AutomagicallyUpdater.OPTIONAL),
			(self.DIA_N_PERMESSO, AutomagicallyUpdater.OPTIONAL),
			(self.DIA_DATA_PERMESSO, AutomagicallyUpdater.OPTIONAL),
			self.ZZ_TIPO_INTERVENTOID,
			self.INTERVENTO_IN_CORSO, 
			(self.ZZ_NORMATIVA_SISMICAID, AutomagicallyUpdater.OPTIONAL)
		]
		self.setupValuesUpdater(childrenList)

	def showOtherInfos(self, show=True):
		self.EPOCA_COSTRUTTIVA.setVisible(show)

