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

from ui.wdgMantoCoperturaUnitaVolumetrica_ui import Ui_Form
from AutomagicallyUpdater import *

class WdgMantoCoperturaUnitaVolumetrica(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
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
		enabler = self.ZZ_TIPO_MANTO_COPERTURAID.currentText().endswith('Altro')
		self.ALTRO_MANTO_COPERTURA.setEnabled(enabler)

	def setValue(self, widget, value):
		widget = self._getRealWidget(widget)
		value = self._getRealValue(value)
		if widget == self.DESCRIZIONE_INCONGRUENZA:
			print value
			self.PRESENZA_INCONGRUENZE.setChecked( value != None and value != "" )
		return AutomagicallyUpdater.setValue(widget, value)

	def toHtml(self):
		incongruenza = self.getValue(self.DESCRIZIONE_INCONGRUENZA)
		return u"""
	<tr class="line">
		<td>Manto di copertura</td><td class="value">%s</td>
		<td class="line">Stato di conservazione</td><td class="value">%s</td>
	</tr>
	<tr class="line">
		<td>Presenza di elementi incogruenti</td><td class="value">%s</td><td colspan="2" class="value">%s</td>
	</tr>
""" % ( self.ZZ_TIPO_MANTO_COPERTURAID.currentText() if not self.ALTRO_MANTO_COPERTURA.isEnabled() else self.getValue(self.ALTRO_MANTO_COPERTURA), self.ZZ_STATO_CONSERVAZIONE_MANTOID.currentText(), "SI" if incongruenza != None else "NO", incongruenza if incongruenza != None else "" )
