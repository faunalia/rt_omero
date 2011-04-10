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
			self.FINE_EPOCA_COSTRUTTIVA, 
			self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID
		]
		self.setupValuesUpdater(childrenList)


