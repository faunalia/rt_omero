# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
from qgis.core import *

from MultiTabSection import MultiTabSection
from WdgSezUnitaVolumetriche import WdgSezUnitaVolumetriche
from AutomagicallyUpdater import *

import Utils
from ManagerWindow import ManagerWindow

class SezUnitaVolumetriche(MultiTabSection):

	def __init__(self, parent=None):
		MultiTabSection.__init__(self, parent, WdgSezUnitaVolumetriche, "UV", "SCHEDA_UNITA_VOLUMETRICA", None, "SCHEDA_EDIFICIOID")
		self.connect(self.tabWidget, SIGNAL( "currentChanged(int)" ), self.currentTabChanged)

		self.pluginManager = ManagerWindow.instance
		self.iface = self.pluginManager.iface
		self.firstTab = self.tabWidget.widget(0)

		self.pointEmitter = Utils.FeatureFinder()
		QObject.connect(self.pointEmitter, SIGNAL("pointEmitted"), self.clickedOnCanvas)

		self.firstTab.setCurrentUV(self.pluginManager.uvScheda)
		self.currentTabChanged(0)

	def assegnaGeomNuova(self, feat):
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		index = self.addTab()
		currentTab = self.tabWidget.widget(index)

		ID = self.pluginManager.copiaGeometria(feat)
		currentTab.setCurrentUV(ID)
		self.pluginManager.scheda.show()
		self.tabWidget.setCurrentIndex(index)

		QApplication.restoreOverrideCursor()

	def assegnaGeomEsistente(self, feat=None):
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		index = self.addTab()
		currentTab = self.tabWidget.widget(index)

		codice = feat.attributeMap()[0].toString()
		currentTab.setCurrentUV(codice)
		self.pluginManager.scheda.show()
		self.tabWidget.setCurrentIndex(index)

		QApplication.restoreOverrideCursor()

	def startCapture(self):
		self.iface.mainWindow().statusBar().showMessage( QString( u"Seleziona l'unità volumetrica da associare alla scheda" ) )
		self.pluginManager.scheda.hide()
		return self.pointEmitter.startCapture()

	def stopCapture(self):
		self.pointEmitter.stopCapture()
		self.iface.mainWindow().statusBar().clearMessage()

	def clickedOnCanvas(self, point=None, button=None):
		self.stopCapture()

		if button != Qt.LeftButton:
			self.pluginManager.scheda.show()
			return

		layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
		if layerModif == None:
			return

		feat = self.pointEmitter.findAtPoint(layerModif, point)
		if feat != None:
			# controlla se tale geometria ha qualche scheda associata
			codice = feat.attributeMap()[0].toString()
			query = AutomagicallyUpdater.Query( "SELECT count(*) FROM SCHEDA_UNITA_VOLUMETRICA WHERE GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW = ?", [codice] )
			if int( query.getFirstResult() ) > 0:
				# NO, c'è già una scheda associata
				QMessageBox.warning( self, "RT Omero", "La geometria selezionata appartiene ad un edificio gia' esistente" )
				return self.startCapture()
			else:
				# OK, non esiste alcuna scheda associata a tale geometria
				# associa la UV a tale geometria
				return self.assegnaGeomEsistente(feat)

		layerOrig = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_ORIG )
		if layerOrig == None:
			return

		# copia la geometria dal layer delle geometrie originali, quindi 
		# associa la UV alla nuova geometria creata
		feat = self.pointEmitter.findAtPoint(layerOrig, point)
		self.assegnaGeomNuova(feat)

	def currentTabChanged(self, index):
		self.tabWidget.widget(index).selectUV()

	def btnAddTabClicked(self):
		return self.startCapture()

	def btnDeleteTabClicked(self):
		refreshCanvas = False

		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()
			refreshCanvas = self.deleteTab()

		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", e.toString())
			return False

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

		if refreshCanvas:
			# aggiorna il layer con le geometrie modificate
			self.pluginManager.aggiornaLayerModif()

	def setupLoader(self, ID=None):
		MultiTabSection.setupLoader(self, ID)

		# seleziona il tab contenente l'UV selezionata in canvas
		for index in range(self.tabWidget.count()):
			uvWidget = self.tabWidget.widget(index)
			if uvWidget.uvID == self.pluginManager.uvScheda:
				self.tabWidget.setCurrentIndex(index)
				return

	def toHtml(self):
		return QString( u"""
<div id="sez3" class="block">
<p class="section">SEZIONE A3 - IDENTIFICAZIONE DELLE UNITA' VOLUMETRICHE</p>
%s
</div>
""" % MultiTabSection.toHtml(self)
)
