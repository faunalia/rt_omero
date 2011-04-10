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

from MultipleChoise2Lists import MultipleChoise2Lists

class MultipleChoiseTipologiaCostruttivaOrizzontale(MultipleChoise2Lists):

	def __init__(self, parent=None):
		MultipleChoise2Lists.__init__(self, parent, "TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTE_STRUTTURE_ORIZZONTALI_SOLAI", None, "STRUTTURE_ORIZZONTALI_SOLAIID", "ZZ_TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTE")

