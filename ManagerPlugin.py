# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import resources

class ManagerPlugin:

	def __init__(self, iface):
		# Save reference to the QGIS interface
		self.iface = iface
		self.dlg = None
	
	def initGui(self):
		# Create action that will start plugin configuration
		self.action = QAction(QIcon(":/icons/rt_omero.png"), "RT Omero", self.iface.mainWindow())
		QObject.connect(self.action, SIGNAL("triggered()"), self.run)

		self.createEmptyDbAction = QAction(QIcon(""), "Crea DB vuoto", self.iface.mainWindow())
		QObject.connect(self.createEmptyDbAction, SIGNAL("triggered()"), self.createEmptyDb)
	
		# Add toolbar button and menu item
		if hasattr( self.iface, 'addDatabaseToolBarIcon' ):
			self.iface.addDatabaseToolBarIcon(self.action)
		else:
			self.iface.addToolBarIcon(self.action)
		if hasattr( self.iface, 'addPluginToDatabaseMenu' ):
			self.iface.addPluginToDatabaseMenu("&Omero RT", self.action)
			self.iface.addPluginToDatabaseMenu("&Omero RT", self.createEmptyDbAction)
		else:
			self.iface.addPluginToMenu("&Omero RT", self.action)
			self.iface.addPluginToMenu("&Omero RT", self.createEmptyDbAction)

		QObject.connect(self.iface, SIGNAL("projectRead()"), self.loadProject)
	
	def unload(self):
		QObject.disconnect(self.iface, SIGNAL("projectRead()"), self.loadProject)

		# Remove the plugin menu item and icon
		if hasattr( self.iface, 'removePluginDatabaseMenu' ):
			self.iface.removePluginDatabaseMenu("&Omero RT", self.action)
			self.iface.removePluginDatabaseMenu("&Omero RT", self.createEmptyDbAction)
		else:
			self.iface.removePluginMenu("&Omero RT", self.action)
			self.iface.removePluginMenu("&Omero RT", self.createEmptyDbAction)

		if hasattr( self.iface, 'removeDatabaseToolBarIcon' ):
			self.iface.removeDatabaseToolBarIcon(self.action)
		else:
			self.iface.removeToolBarIcon(self.action)

		if self.dlg:
			self.dlg.close()
	
	def run(self):
		try:
			import pyspatialite
		except ImportError, e:
			QMessageBox.information(self.iface.mainWindow(), "Attenzione", QString( u"Modulo 'pyspatialite' non trovato. Senza di esso non è possibile eseguire RT Omero." ) )
			return

		if self.dlg == None:
			from ManagerWindow import ManagerWindow
			self.dlg = ManagerWindow(self.iface.mainWindow(), self.iface)
			QObject.connect(self.dlg, SIGNAL("closed()"), self.onDlgClosed)
		self.dlg.exec_()

	def onDlgClosed(self):
		if self.dlg:
			self.dlg.deleteLater()
		self.dlg = None

	def loadProject(self):
		if self.dlg != None:
			return

		from ManagerWindow import ManagerWindow
		self.dlg = ManagerWindow(self.iface.mainWindow(), self.iface)
		QObject.connect(self.dlg, SIGNAL("closed()"), self.onDlgClosed)
		if not self.dlg.reloadLayersFromProject():
			self.dlg.close()


	def createEmptyDb(self):
		from DlgCreaDbVuoto import DlgCreaDbVuoto
		DlgCreaDbVuoto().exec_()

