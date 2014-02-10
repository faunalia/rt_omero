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

from ui.wdgStruttureOrizzontaliSolai_ui import Ui_Form
from AutomagicallyUpdater import *

class WdgStruttureOrizzontaliSolai(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "STRUTTURE_ORIZZONTALI_SOLAI")
		self.setupUi(self)

		self.SCHEDA_EDIFICIOID.hide()

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTEID: AutomagicallyUpdater.ZZTable( "ZZ_TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTE" ), 
			self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID: AutomagicallyUpdater.ZZTable( "ZZ_STATO_CONSERVAZIONE_STRUTTURALE" ),
			self.ZZ_QUALITA_INFORMAZIONEID: AutomagicallyUpdater.ZZTable( "ZZ_QUALITA_INFORMAZIONE" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.SCHEDA_EDIFICIOID,
			self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID, 
			self.ZZ_QUALITA_INFORMAZIONEID, 
			self.ZZ_TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTEID
		]
		self.setupValuesUpdater(childrenList)

	def toHtml(self, index):
		tipologia = self.ZZ_TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTEID.getValues(False)
		return u"""
<table class="green border">
	<tr>
		<td class="title" colspan="4">Strutture orizzontali solai</td>
	</tr>
	<tr class="line">
		<td>Qualit&agrave; dell'informazione</td><td colspan="3" class="value">%s</td>
	</tr>
	<tr class="line">
		<td class="subtitle">Tipologia costruttiva</td><td colspan="3" class="value">%s</td>
	</tr>
	<tr>
		<td>Stato di conservazione</td><td colspan="3" class="value">%s</td>
	</tr>
</table>
""" % ( self.ZZ_QUALITA_INFORMAZIONEID.currentText(), "<br>".join(tipologia), self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID.currentText() )
