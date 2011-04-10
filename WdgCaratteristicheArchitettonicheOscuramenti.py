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

from WdgCaratteristicheArchitettonicheChild import WdgCaratteristicheArchitettonicheChild

class WdgCaratteristicheArchitettonicheOscuramenti(WdgCaratteristicheArchitettonicheChild):

	def __init__(self, parent=None):
		multipleChoiseParams = ["ZZ_TIPO_OSCURAMENTI_OSCURAMENTI", "ZZ_TIPO_OSCURAMENTIID", "OSCURAMENTIID", "ZZ_TIPO_OSCURAMENTI"]
		WdgCaratteristicheArchitettonicheChild.__init__(self, parent, "OSCURAMENTI", None, multipleChoiseParams)
		self.showOtherInfos(True)

		# modifica il nome degli oggetti
		self.ZZ_TIPO.setObjectName("ZZ_TIPO_OSCURAMENTI_OSCURAMENTI")
		self.ALTRO.setObjectName("ALTRO_OSCURAMENTO")

	def getNomeCaratteristica(self):
		return "Oscuramenti"

