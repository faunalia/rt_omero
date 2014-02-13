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
			self.ZZ_PROPRIETAID: AutomagicallyUpdater.ZZTable( "ZZ_PROPRIETA" )
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

	def toHtml(self):
		catastali = self.PARTICELLE_CATASTALI.getValues(False)
		fogli = map(lambda x: x[0] if x[0] != None else "", catastali)
		particelle =  map(lambda x: x[1] if x[1] != None else "", catastali)
		isolato = self.getValue(self.EDIFICIO_ISOLATO)
		
		
		print fogli, particelle, isolato
		
		
		return u"""
<div id="sez2" class="block">
<p class="section">SEZIONE A2 - LOCALIZZAZIONE DELL'EDIFICIO</p>
<div class="border">
%s
<table class="blue">
	<tr class="line">
		<td class="subtitle">Riferimenti catastali</td>
		<td class="line">Foglio</td><td class="value">%s</td>
		<td class="line">Particelle</td><td class="value">%s</td>
	</tr>
	<tr class="line">
		<td>Edificio isolato</td><td class="value">%s</td>
		<td colspan="2" class="line">Posizione dell'edificio nell'aggregato strutturale</td><td class="value">%s</td>
	</tr>
	<tr>
		<td>Numero unit&agrave immobiliari</td><td class="value">%s</td>
		<td colspan="2" class="line">Propriet&agrave</td><td class="value">%s</td>
	</tr>
</table>
</div>
</div>
""" % ( self.LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA.toHtml(), "<br>".join(fogli), "<br>".join(particelle), "SI" if isolato else "NO", self.ZZ_POSIZIONE_EDIFICIO_AGGREGATOID.currentText(), self.getValue(self.NUM_UNITA_IMMOBILIARI), self.ZZ_PROPRIETAID.currentText() )
