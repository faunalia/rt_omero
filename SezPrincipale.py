# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgSezPrincipale_ui import Ui_Form
from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import *

class SezPrincipale(QWidget, MappingPart, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingPart.__init__(self, "SCHEDA_EDIFICIO")
		self.setupUi(self)

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.DATA_COMPILAZIONE_SCHEDA, 
			self.RILEVATOREID
		]
		self.setupValuesUpdater(childrenList)

		# carica il valore dell'ultimo rilevatore utilizzato
		self.setValue(self.RILEVATOREID, self._getIDRilevatore())

	def setValue(self, widget, value):
		value = self._getRealValue(value)
		if self._getRealWidget(widget) == self.RILEVATOREID and value != None:
			IDComune = QString(value).remove( QRegExp('\-.*$') )

			query = AutomagicallyUpdater.Query( "SELECT ID, COGNOME, NOME, (SELECT com.NOME || ' (' || prov.NOME || ')' FROM ZZ_PROVINCE AS prov JOIN ZZ_COMUNI AS com ON prov.ISTATPROV = com.ZZ_PROVINCEISTATPROV WHERE com.ISTATCOM = ?) AS \"COMUNE\" FROM RILEVATORE WHERE ID = ?", [ IDComune, value ] )
			self.loadTables(self.RILEVATOREID, query)
		
		AutomagicallyUpdater.setValue(widget, value)
		
