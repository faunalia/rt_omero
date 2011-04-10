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

from ui.dlgSelezionaDB_ui import Ui_DlgSelezionaDB as Ui_Dlg
from AutomagicallyUpdater import *

class DlgSelezionaDB(QDialog, Ui_Dlg):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setupUi(self)
		self.connect(self.buttonBox, SIGNAL("helpRequested()"), self.help)
		self.connect(self.btnDbDemo, SIGNAL("clicked()"), self.copiaDemoDB)
		self.connect(self.btnDbWork, SIGNAL("clicked()"), self.copiaWorkDB)

	def help(self):
		import os.path
		path = os.path.join( os.path.dirname(__file__), 'docs', 'manuale_uso.pdf' )
		QDesktopServices.openUrl( QUrl.fromLocalFile(path) )


	@classmethod
	def selezionaDB(self, parent=None):
		path = AutomagicallyUpdater._getPathToDb()
		dbpath = QFileDialog.getOpenFileName(parent, u"Seleziona il DB di lavoro da utilizzare", path if path != None else "", "Sqlite DB (*.sqlite *.db3);;Tutti i file (*)" )
		if dbpath.isEmpty():
			return
		AutomagicallyUpdater._setPathToDb( dbpath )
		return dbpath


	def copiaWorkDB(self):
		if self.selezionaDB( self ) == None:
			return
		return self.accept()

	def copiaDemoDB(self):
		path = AutomagicallyUpdater._getPathToDb()
		# copia il database di test nella directory indicata dall'utente
		dbpath = QFileDialog.getSaveFileName(self, u"Salva il DB dimostrativo", path if path != None else "", "Sqlite DB (*.sqlite *.db3);;Tutti i file (*)" )
		if dbpath.isEmpty():
			return

		import os.path, zipfile
		demoZip = os.path.join(os.path.dirname(__file__), "docs", "demo.zip")

		try:
			zf = zipfile.ZipFile( unicode(demoZip) )
			if len( zf.namelist() ) <= 0:
				raise zipfile.BadZipfile( "no files in the archive" )
			
			outfile = open( unicode(dbpath), 'wb' )
			try:
				outfile.write( zf.read( zf.namelist()[0] ) )
			finally:
				outfile.close()

		except (IOError, zipfile.BadZipfile), e:
			QMessageBox.critical( self, u"Errore", u"Impossibile estrarre l'archivio contenente il DB dimostrativo.\n\nError message: %s" % unicode(str(e), 'utf8') )
			return self.reject()

		AutomagicallyUpdater._setPathToDb( dbpath )
		return self.accept()

