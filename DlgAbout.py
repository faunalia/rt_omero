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

from ui.dlgAbout_ui import Ui_DlgAbout

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import QGis
import ConfigParser
import os.path

from AutomagicallyUpdater import *

class DlgAbout(QDialog, Ui_DlgAbout):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setupUi(self)
		self.showVersions()
		self.connect(self.buttonBox, SIGNAL("helpRequested()"), self.help)

	def help(self):
		path = os.path.join( os.path.dirname(__file__), 'docs', 'manuale_uso.pdf' )
		QDesktopServices.openUrl( QUrl.fromLocalFile(path) )

	def showVersions(self):
		# read metadata from metadata.txt
		config = ConfigParser.ConfigParser()
		config.read( os.path.join( os.path.dirname(__file__), 'metadata.txt' ) )		
		
		text = self.txt.toHtml()

		plugin_ver = config.get("general", "version")
		text = text.replace( "$PLUGIN_VER$", plugin_ver )
		text = text.replace( "$QGIS_VER$", QGis.QGIS_VERSION )
		text = text.replace( "$DB_PATH$" , AutomagicallyUpdater._getPathToDb() )

		query = AutomagicallyUpdater.Query( "SELECT DATABASE, DB_VERSION_MAIOR || '.' || DB_VERSION_MINOR, TARGET FROM ZZ_DISCLAIMER" )
		query = query.getQuery()
		if query.exec_() and query.next():
			text = text.replace( "$DB_TYPE$", query.value(0) )
			text = text.replace( "$DB_VER$", query.value(1) )
			text = text.replace( "$DB_TARGET$", query.value(2) )

		self.txt.setHtml(text)
