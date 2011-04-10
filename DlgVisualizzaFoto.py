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

from ui.dlgVisualizzaFoto_ui import Ui_Dialog
from AutomagicallyUpdater import *
import Utils

class DlgVisualizzaFoto(QDialog, Ui_Dialog):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setupUi(self)
		self.view2id = {}

	def exec_(self, ids):
		if len(ids) <= 0:
			return False
		if len(ids) == 1:
			return self.apriFotoByRowid( ids[0], None )

		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		layout = QHBoxLayout( self.listaFoto )
		layout.setContentsMargins( 0, 0, 0, 0 )

		for rowid in ids:
			imgData = AutomagicallyUpdater.Query( "SELECT IMAGE FROM FOTO_GEOREF WHERE ROWID = ?", [rowid] ).getFirstResult()
			if imgData != None:
				picViewer = Utils.PicViewer(self)
				picViewer.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
				picViewer.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
				picViewer.setMinimumSize( QSize(160, 120) )
				picViewer.setMaximumSize( QSize(160, 120) )

				self.view2id [ picViewer ] = rowid
				self.connect(picViewer, SIGNAL( "openPicRequested" ), self.apriFotoByPicViewer)
				layout.addWidget( picViewer )

				AutomagicallyUpdater.setValue( picViewer, imgData )
				picViewer.clearCache()

		QApplication.restoreOverrideCursor()
		return QDialog.exec_(self)


	def apriFotoByRowid(self, rowid, tempKey=Utils.TemporaryFile.KEY_VISUALIZZAFOTO):
		query = AutomagicallyUpdater.Query( "SELECT IMAGE, FILENAME FROM FOTO_GEOREF WHERE ROWID = ?", [rowid] ).getQuery()
		if not query.exec_() or not query.next():
			return
		imgData = query.value(0).toByteArray()
		ext = QFileInfo( query.value(1).toString() ).suffix()

		filename = Utils.TemporaryFile.salvaDati(imgData, tempKey, ext)
		if filename == None:
			return False
		url = QUrl.fromLocalFile( filename )
		QDesktopServices.openUrl( url )
		return True

	def apriFotoByPicViewer(self):
		picViewer = self.sender()
		if picViewer == None or not isinstance(picViewer, Utils.PicViewer):
			return False
		if not self.view2id.has_key( picViewer ):
			return False
		return self.apriFotoByRowid( self.view2id[picViewer] )


	def closeEvent(self, event):
		for view in self.view2id.keys():
			del self.view2id[ view ]
			del view
		del self.view2id

		Utils.TemporaryFile.delAllFiles( Utils.TemporaryFile.KEY_VISUALIZZAFOTO )
		return QDialog.closeEvent(self, event)

