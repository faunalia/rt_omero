# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : Omero RT
Description          : Omero plugin
Date                 : June 15, 2013 
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

from ui.dlgUnisci2Db_ui import Ui_Dialog
from AutomagicallyUpdater import *
from ConnectionManager import PySLDatabase, SqlException

from qgis.core import *
from qgis.gui import QgsMessageViewer
from ManagerWindow import ManagerWindow

import os.path, sys
currentPath = os.path.dirname(__file__)

class DlgUnisci2Db(QDialog, Ui_Dialog):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setupUi(self)

		# setup the progress dialog
		self.progressDlg = QProgressDialog(self)
		self.progressDlg.setWindowModality(Qt.WindowModal)
		self.progressDlg.setMinimumDuration(0)
		self.progressDlg.setAutoClose(False)
		self.connect(self.progressDlg, SIGNAL("canceled()"), self.onCancel)

		# get all "input db" groups
		i=1
		self._groups = []
		while hasattr(self, 'indb%dEdit'%i):
			infilename = getattr(self, 'indb%dEdit'%i)
			browsebtn = getattr(self, 'inBrowse%dBtn'%i)
			self.connect(browsebtn, SIGNAL("clicked()"), self.browseFile)

			grp = (
				infilename,
				browsebtn
			)
			self._groups += [grp]

			i += 1

	def browseFile(self):
		senderbtn = self.sender()

		lastUsedDir = AutomagicallyUpdater._getLastUsedDir("importdb")
		infile = QFileDialog.getOpenFileName(self, u"Seleziona un database di input", lastUsedDir, "SQLite database (*.db3 *.sqlite *db);;Tutti i file (*)")
		if not infile:
			return
		AutomagicallyUpdater._setLastUsedDir("importdb", infile)

		for fnedit, browsebtn in self._groups:
			if senderbtn != browsebtn:
				continue

			fnedit.setText(infile)
			break


	def getOutputPath(self):
		lastUsedDir = QFileInfo(AutomagicallyUpdater._getPathToDb()).path()
		output = QFileDialog.getSaveFileName(self, u"Salva un database", lastUsedDir, "SQLite database (*.db3 *.sqlite);;Tutti i file (*)")
		if not output:
			return

		if output[-4:] != ".db3" and output[-7:] != ".sqlite" and output[-3:] != ".db":
			output += ".db3"
		return output

	def accept(self):
		self.outputPath = self.getOutputPath()
		if not self.outputPath:
			return
			
		for infn, btn in self._groups:
			if not infn.text() or infn.text() == self.outputPath:
				return

		self.buttonBox.button( QDialogButtonBox.Ok ).setEnabled(False)
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		self.resetProgress(None, "Unione dei database in corso..." )
		self.progressDlg.forceShow()

		indb1path = self._groups[0][0].text()
		indb2path = self._groups[1][0].text()
		
		# run the work on a different thread
		self.mythread = Merge2DbsThread(indb1path, indb2path, self.outputPath, self)
		self.connect(self.mythread, SIGNAL("messageSent"), self.onMessage)
		self.connect(self.mythread, SIGNAL("exceptionRaised"), self.reRaiseExceptions)	# error handler
		self.connect(self.mythread, SIGNAL("resetProgress"), self.resetProgress)
		self.connect(self.mythread, SIGNAL("updateProgress"), self.updateProgress)
		self.connect(self.mythread, SIGNAL("creationDone"), self.workDone)
		self.connect(self.mythread, SIGNAL("finished()"), self.stop)
		#self.mythread.run()	###DEBUG
		self.mythread.start()

	def workDone(self, ok, log):
		if ok:
			title = u"<h3>Unione dei database completata. <br>Nuovo database: <em>'%s'</em>.</h3>" % self.outputPath
		else:
			title = "<h3>Errore durante l'unione dei database selezionati.</h3>"

		# display the log
		if log != "":
			vw = QgsMessageViewer(self)
			vw.setTitle("RT Omero")
			vw.setMessageAsHtml( u"%s\n%s" % (title, log) )
			vw.exec_()
		else:
			self.onMessage(0 if ok else 2, title)

		if ok:
			QDialog.accept(self)

	def stop(self):
		self.mythread.deleteLater()
		QApplication.restoreOverrideCursor()
		self.buttonBox.button( QDialogButtonBox.Ok ).setEnabled(True)
		self.progressDlg.hide()

	def onCancel(self):
		self.mythread.terminate()
		self.stop()

	def reRaiseExceptions(self, exc_info):
		""" error handler: re-raise the exception """
		raise exc_info[1], None, exc_info[2]

	def onMessage(self, level, msg):
		msgbox = QMessageBox.information
		if level == 1:
			msgbox = QMessageBox.warning
		elif level == 2:
			msgbox = QMessageBox.critical
		msgbox(self, "RT Omero", msg)

	def resetProgress(self, maximum=None, label=None):
		self.progressDlg.reset()
		if label is not None:
			self.progressDlg.setLabelText( label )
		if maximum is not None:
			self.progressDlg.setMaximum( maximum )
		else:
			self.progressDlg.setRange(0, 0)

	def updateProgress(self, val=None):
		self.progressDlg.setValue( val if val is not None else self.progressDlg.value()+1 )


#class Merge2DbsThread(QObject):	###DEBUG
class Merge2DbsThread(QThread):

	def __init__(self, inpath1, inpath2, outpath, parent=None):
		#QObject.__init__(self, parent)	###DEBUG
		QThread.__init__(self, parent)
		self.inpath1 = inpath1
		self.inpath2 = inpath2
		self.outpath = outpath

	def run(self):
		# Let's catch all the exceptions to avoid crashes! 
		# QGis tries to display a dialog with the traceback for uncaugth exceptions 
		# but GUI can't be drawn out of the main thread
		try:
			self.exec_()
		except:
			self.emit(SIGNAL("exceptionRaised"), sys.exc_info() )

	def exec_(self):
		# if the file exists remove it
		finfo = QFileInfo(self.outpath)
		if finfo.exists() and not QFile.remove(self.outpath):
			self.emit(SIGNAL("messageSent"), 1, u"Impossibile scrivere nella directory selezionata.")
			return
			
		# make a copy of the second input db
		QFile.copy(self.inpath2, self.outpath)
		
		# if the file not exists display an error
		finfo = QFileInfo(self.outpath)
		if not finfo.exists():
			self.emit(SIGNAL("messageSent"), 1, u"Impossibile scrivere nella directory selezionata.")
			return

		from merge2dbs import merge
		try:
			merge(self.inpath1, self.outpath)
		except IOError:
			self.emit(SIGNAL("messageSent"), 2, u"Errore connettendosi al database: \n%s" % e.args[0])
			return

		self.emit(SIGNAL("creationDone"), True, "")
		return
