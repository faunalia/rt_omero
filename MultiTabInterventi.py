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

from MultiTabSection import MultiTabSection
from WdgInterventi import WdgInterventi

class MultiTabInterventi(MultiTabSection):

	def __init__(self, parent=None):
		MultiTabSection.__init__(self, parent, WdgInterventi, "Intervento ", "INTERVENTO_EDIFICIO", None, "SCHEDA_EDIFICIOID")
		self.setFirstTab()

	def setFirstTab(self):
		self.firstTab = self.tabWidget.widget(0)
		self.firstTab.showOtherInfos(True)
		self.tabWidget.setTabText(0, "Impianto")

