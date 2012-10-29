# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : Omero RT
Description          : Omero plugin
Date                 : August 15, 2010 
copyright            : (C) 2010 by Giuseppe Sucameli (Faunalia)
email                : sucameli@faunalia.it
 ***************************************************************************/

Omero plugin
Works done from Faunalia (http://www.faunalia.it) with funding from Regione 
Toscana - S.I.T.A. (http://www.regione.toscana.it/territorio/cartografia/index.html)

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

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
			(self.FINE_EPOCA_COSTRUTTIVA, AutomagicallyUpdater.OPTIONAL),
			self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID
		]
		self.setupValuesUpdater(childrenList)

		# update the color of the checkboxes associated to required widgets
		QObject.connect( self.INIZIO_EPOCA_COSTRUTTIVA_check, SIGNAL("toggled(bool)"), self.updateWidgetColor )
		self.updateWidgetColor()

	def updateWidgetColor(self):
		self._refreshWidgetColor(self.INIZIO_EPOCA_COSTRUTTIVA)
		self.INIZIO_EPOCA_COSTRUTTIVA_check.setStyleSheet( self.INIZIO_EPOCA_COSTRUTTIVA.styleSheet() )


	def setValue(self, widget, value):
		widget = self._getRealWidget(widget)
		value = self._getRealValue(value)
		# update the state of the checkboxes
		if widget == self.INIZIO_EPOCA_COSTRUTTIVA:
			self.INIZIO_EPOCA_COSTRUTTIVA_check.setChecked( value != None )
			if value == None:
				value = QDate.currentDate().year()
		if widget == self.FINE_EPOCA_COSTRUTTIVA:
			self.FINE_EPOCA_COSTRUTTIVA_check.setChecked( value != None )
			if value == None:
				value = QDate.currentDate().year()
		return AutomagicallyUpdater.setValue(widget, value)

	def getValue(self, widget):
		if self._getRealWidget(widget) != self.INIZIO_EPOCA_COSTRUTTIVA:
			return AutomagicallyUpdater.getValue(widget)

		# INIZIO_EPOCA_COSTRUTTIVA column is NOT NULL, store VALORE_NON_INSERITO
		value = AutomagicallyUpdater.getValue(widget)
		return value if value != None else AutomagicallyUpdater.VALORE_NON_INSERITO

