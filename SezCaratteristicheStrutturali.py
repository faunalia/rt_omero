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

from ui.wdgSezCaratteristicheStrutturali_ui import Ui_Form
from AutomagicallyUpdater import *

class SezCaratteristicheStrutturali(QWidget, MappingPart, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingPart.__init__(self, "SCHEDA_EDIFICIO")
		self.setupUi(self)

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.STRUTTURE_PORTANTI_VERTICALIID,
			self.STRUTTURE_ORIZZONTALI_SOLAI
		]
		self.setupValuesUpdater(childrenList)

	def toHtml(self):
		return QString( u"""
<div id="sez6" class="block">
<p class="section">SEZIONE A6 - CARATTERISTICHE STRUTTURALI</p>
%s %s
</div>
""" % ( self.STRUTTURE_PORTANTI_VERTICALIID.toHtml(), self.STRUTTURE_ORIZZONTALI_SOLAI.toHtml() )
)
