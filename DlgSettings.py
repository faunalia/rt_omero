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

from ui.dlgSettings_ui import Ui_Dialog

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from AutomagicallyUpdater import AutomagicallyUpdater

class DlgSettings(QDialog, Ui_Dialog):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setupUi(self)
		
		self.restorePrintBehavior()
		self.initPrintPdfResolution()
		
		self.restoreWMSRepoUrl()


	def initPrintPdfResolution(self):
		self.printPdfResGroup.setEnabled( self.printPdfRadio.isChecked() )

		import platform
		if platform.system() != "Windows":
			self.printPdfHighResRadio.setChecked( True )
			self.printPdfResGroup.hide()
			self.resize( QSize(100,100) )


	def restorePrintBehavior(self):
		mode, res = AutomagicallyUpdater.printBehavior()

		self.printPdfRadio.setChecked( mode == QPrinter.PdfFormat )
		self.printDefaultRadio.setChecked( mode == QPrinter.NativeFormat )
		self.printHtmlRadio.setChecked( mode == -1 )

		self.printPdfHighResRadio.setChecked( res == QPrinter.HighResolution )
		self.printPdfLowResRadio.setChecked( res == QPrinter.ScreenResolution )

	def updatePrintBehavior(self):
		if self.printDefaultRadio.isChecked(): mode = QPrinter.NativeFormat
		elif self.printHtmlRadio.isChecked(): mode = -1
		else: mode = QPrinter.PdfFormat

		if self.printPdfLowResRadio.isChecked(): res = QPrinter.ScreenResolution
		else: res = QPrinter.HighResolution

		AutomagicallyUpdater.setPrintBehavior( mode, res )
	
	
	def restoreWMSRepoUrl(self):
		self.wmsRepoUrlEdit.setText( AutomagicallyUpdater.getWMSRepositoryUrl() )

	def updateWMSRepoUrl(self):
		AutomagicallyUpdater.setWMSRepositoryUrl( self.wmsRepoUrlEdit.text() )


	def accept(self):
		self.updatePrintBehavior()
		self.updateWMSRepoUrl()
		QDialog.accept(self)

