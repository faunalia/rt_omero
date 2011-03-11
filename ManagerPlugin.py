# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

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
	
		# Add toolbar button and menu item
		self.iface.addToolBarIcon(self.action)
		if hasattr( self.iface, 'addPluginToDatabaseMenu' ):
			self.iface.addPluginToDatabaseMenu("&Omero RT", self.action)
		else:
			self.iface.addPluginToMenu("&Omero RT", self.action)
	
	def unload(self):
		# Remove the plugin menu item and icon
		if hasattr( self.iface, 'removePluginDatabaseMenu' ):
			self.iface.removePluginDatabaseMenu("&Omero RT", self.action)
		else:
			self.iface.removePluginMenu("&Omero RT", self.action)
		self.iface.removeToolBarIcon(self.action)

		if self.dlg != None:
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
		self.dlg = None
