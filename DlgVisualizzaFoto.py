# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

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
			return self.apriFotoByRowid( ids[0] )

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


	def apriFotoByRowid(self, rowid):
		imgData = AutomagicallyUpdater.Query( "SELECT IMAGE FROM FOTO_GEOREF WHERE ROWID = ?", [rowid] ).getFirstResult()
		if imgData == None:
			return False

		tmp = Utils.TemporaryFile.getNewFile( 'DlgVisualizzaFoto.apriFoto' )
		if not tmp.open():
			Utils.TemporaryFile.delFile( tmp, 'DlgVisualizzaFoto.apriFoto' )
			return False

		outfile = open( tmp.fileName().toUtf8(), "wb" )
		outfile.write( str(imgData) )
		outfile.close()

		tmp.close()

		url = QUrl.fromLocalFile( tmp.fileName() )
		QDesktopServices.openUrl( url )
		return True

	def apriFotoByPicViewer(self):
		picViewer = self.sender()
		if picViewer == None or not isinstance(picViewer, Utils.PicViewer):
			return False
		if not self.view2id.has_key( picViewer ):
			return False
		return self.apriFotoByRowid( self.view2id[picViewer] )

