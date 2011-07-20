# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : Omero RT
Description          : Omero plugin
Date                 : August 15, 2010 
copyright            : (C) 2010 by Giuseppe Sucameli (Faunalia)
email                : brush.tyler@gmail.com
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
 This script initializes the plugin, making it known to QGIS.
"""

def name():
	return "RT Omero"

def description():
	return "Omero plugin per la Regione Toscana"

def icon():
	return "icons/rt_omero.png"

def version():
	return "Version 1.0.4"

def qgisMinimumVersion():
	return "1.7.0"

def classFactory(iface):
	from ManagerPlugin import ManagerPlugin
	return ManagerPlugin(iface)
