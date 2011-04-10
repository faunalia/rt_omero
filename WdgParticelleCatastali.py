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

from Wdg2FieldsTable import Wdg2FieldsTable

class WdgParticelleCatastali(Wdg2FieldsTable):

	def __init__(self, parent=None):
		columns = ( ("FOGLIO", "Foglio"), ("PARTICELLA", "Particella") )
		Wdg2FieldsTable.__init__(self, parent, "RIFERIMENTI_CATASTALI_SCHEDA_EDIFICIO", "SCHEDA_EDIFICIOID", "RIFERIMENTI_CATASTALIIDREF_CATAST", "RIFERIMENTI_CATASTALI", "IDREF_CATAST", columns)

