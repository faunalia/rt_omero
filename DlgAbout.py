# -*- coding: utf-8 -*-

from ui.dlgAbout_ui import Ui_DlgAbout

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import QGis

from rt_omero import version
from AutomagicallyUpdater import *

class DlgAbout(QDialog, Ui_DlgAbout):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setupUi(self)
		self.showVersions()
		self.connect(self.buttonBox, SIGNAL("helpRequested()"), self.help)

	def help(self):
		import os.path
		path = os.path.join( __file__, 'docs', 'index.html' )
		QDesktopServices.openUrl( QUrl.fromLocalFile(path) )

	def showVersions(self):
		text = self.txt.toHtml()

		plugin_ver = version()[8:]
		text = text.replace( "$PLUGIN_VER$", plugin_ver )

		text = text.replace( "$QGIS_VER$", QGis.QGIS_VERSION )
		text = text.replace( "$QGIS_REV$", QGis.QGIS_SVN_VERSION )

		text = text.replace( "$DB_PATH$" , AutomagicallyUpdater._getPathToDb() )

		query = AutomagicallyUpdater.Query( "SELECT DB_VERSION_MAIOR || '.' || DB_VERSION_MINOR, DB_LAST_DATE_USAGE FROM ZZ_DISCLAIMER" )
		query = query.getQuery()
		if query.exec_() and query.next():
			text = text.replace( "$DB_VER$", query.value(0).toString() )
			text = text.replace( "$DB_REV$", query.value(1).toString() )

		self.txt.setHtml(text)
