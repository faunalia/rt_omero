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

from ui.wdgCaratteristicheArchitettonicheChild_ui import Ui_Form
from MultipleChoiseCheckList import MultipleChoiseCheckList
from AutomagicallyUpdater import *

class WdgCaratteristicheArchitettonicheChild(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None, table=None, pk=None, zzTipoParams=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, table, pk)
		self.setupUi(self)

		if zzTipoParams != None:
			self.setupMultiCheckList(*zzTipoParams)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_STATO_CONSERVAZIONE_ARCHITETTONICOID: AutomagicallyUpdater.ZZTable( "ZZ_STATO_CONSERVAZIONE_ARCHITETTONICO" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			(self.ALTRO, AutomagicallyUpdater.OPTIONAL), 
			self.ZZ_STATO_CONSERVAZIONE_ARCHITETTONICOID, 
			self.ZZ_TIPO
		]
		self.setupValuesUpdater(childrenList)

		self.showOtherInfos(True)

		self.connect(self.ZZ_TIPO, SIGNAL("selectionChanged()"), self.abilitaAltroTipo)
		self.abilitaAltroTipo()

	def abilitaAltroTipo(self):
		enabler = self.ZZ_TIPO.isSelected("Altro", Qt.MatchEndsWith)
		self.ALTRO.setEnabled(enabler)


	def showOtherInfos(self, show=True):
		self.incongruenzeInfo.setVisible(show)
		self.otherInfos = show
		if show:
			self.addChildRef(self.PRESENZA_INCONGRUENZE)
			self.addChildRef(self.DESCRIZIONI_INCONGRUENZE, AutomagicallyUpdater.OPTIONAL)
		else:
			self.delChildRef(self.PRESENZA_INCONGRUENZE)
			self.delChildRef(self.DESCRIZIONI_INCONGRUENZE)
			

	def setupMultiCheckList(self, table=None, pk=None, parentPk=None, tableWithValues=None):
		oldZZ_TIPO = self.ZZ_TIPO
		parent = oldZZ_TIPO.parent()
		self.ZZ_TIPO = MultipleChoiseCheckList(parent, table, pk, parentPk, tableWithValues)
		gridLayout = parent.layout()
		index = gridLayout.indexOf(oldZZ_TIPO)
		info = gridLayout.getItemPosition(index)
		gridLayout.addWidget(self.ZZ_TIPO, *info)
		#gridLayout.removeWidget(oldZZ_TIPO)

	def getNomeCaratteristica(self):
		pass

	def toHtml(self):
		valori = QStringList() << self.ZZ_TIPO.getValues(False)
		if self.ALTRO.isEnabled():
			for v in valori:
				if v.endsWith("Altro"):
					valori.remove(v)
					break
			valori << self.getValue(self.ALTRO)

		incongruenze = self.getValue(self.DESCRIZIONI_INCONGRUENZE)

		return QString( u"""
<table class="yellow border">
	<tr class="line">
		<td class="subtitle">%s</td><td class="value">%s</td>
		<td class="line">Stato di conservazione</td><td class="value">%s</td>
	</tr>
	<tr %s>
		<td>Presenza di elementi incogruenti</td><td class="value">%s</td><td class="value">%s</td>
	</tr>
</table>
""" % ( self.getNomeCaratteristica(), valori.join("<br>"), self.ZZ_STATO_CONSERVAZIONE_ARCHITETTONICOID.currentText(), 'class="hidden"' if not self.otherInfos else '', "SI" if self.getValue(self.PRESENZA_INCONGRUENZE) else "NO", incongruenze if incongruenze != None else '' )
)
