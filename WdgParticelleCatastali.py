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

	def _saveValue(self, name2valueDict, table, pk, ID=None):
		# converti i valori nulli per foglio e particella in stringhe vuote
		for c in self.columnFields:
			if name2valueDict.has_key( c ):
				value = name2valueDict[c]
				name2valueDict[c] = value if value != None else ''

		return Wdg2FieldsTable._saveValue(name2valueDict, table, pk, ID)

