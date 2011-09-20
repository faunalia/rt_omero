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

from qgis.core import QgsMapLayerRegistry

from MultiTabSection import MultiTabSection
from WdgSezUnitaVolumetriche import WdgSezUnitaVolumetriche
from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import *

import Utils
from ManagerWindow import ManagerWindow

class SezUnitaVolumetriche(MultiTabSection):

	def __init__(self, parent=None):
		MultiTabSection.__init__(self, parent, WdgSezUnitaVolumetriche, "UV", "SCHEDA_UNITA_VOLUMETRICA", None, "SCHEDA_EDIFICIOID")
		self.connect(self.tabWidget, SIGNAL( "currentChanged(int)" ), self.currentTabChanged)

		self.firstTab = self.tabWidget.widget(0)

		self.firstTab.setUV(ManagerWindow.instance.uvScheda)
		self.currentTabChanged(0)

		self.pointEmitter = Utils.FeatureFinder()
		self.pointEmitter.registerStatusMsg( u"Seleziona l'unità volumetrica da associare alla scheda" )
		QObject.connect(self.pointEmitter, SIGNAL("pointEmitted"), self.clickedOnCanvas)

	def onClosing(self):
		del self.firstTab
		self.pointEmitter.deleteLater()
		del self.pointEmitter
		MultiTabSection.onClosing(self)

	def assegnaGeomNuova(self, feat):
		ID = ManagerWindow.instance.copiaGeometria(feat)
		self.assegnaGeomEsistenteByUvID( ID )

	def assegnaGeomEsistente(self, feat=None):
		codice = feat.attributeMap()[0].toString()
		self.assegnaGeomEsistenteByUvID( codice )

	def assegnaGeomEsistenteByUvID(self, uvID=None):
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		index = self.addTab()
		currentTab = self.tabWidget.widget(index)
		currentTab.setUV( uvID )	# aggiorna le info di DEBUG sulla UV

		# imposta la geometria come abbinata a scheda
		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()
			AutomagicallyUpdater._updateValue( { "ABBINATO_A_SCHEDA" : '1' }, "GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE", "ID_UV_NEW", uvID )
		except ConnectionManager.AbortedException, e:
			QMessageBox.critical(self, "Errore", e.toString())
			return

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

		self.stopCapture()
		self.tabWidget.setCurrentIndex(index)

		QApplication.restoreOverrideCursor()


	def startCapture(self):
		# minimizza la scheda
		ManagerWindow.instance.scheda.setMinimized( True )
		return self.pointEmitter.startCapture()

	def stopCapture(self):
		self.pointEmitter.stopCapture()
		# mostra la scheda
		ManagerWindow.instance.scheda.setMinimized( False )


	def clickedOnCanvas(self, point=None, button=None):
		action = u"Associa unità volumetrica"

		if not ManagerWindow.checkActionScale( action, ManagerWindow.SCALE_IDENTIFY ) or point == None:
			return self.startCapture()

		if button != Qt.LeftButton:
			return self.stopCapture()

		layerModif = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_MODIF )
		if layerModif == None:
			return

		feat = self.pointEmitter.findAtPoint(layerModif, point)
		if feat != None:
			if not ManagerWindow.checkActionSpatialFromFeature( action, feat, True ):
				return self.startCapture()

			# controlla se tale geometria ha qualche scheda associata
			codice = feat.attributeMap()[0].toString()
			abbinato = AutomagicallyUpdater.Query( "SELECT ABBINATO_A_SCHEDA FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE WHERE ID_UV_NEW = ?", [codice] ).getFirstResult() == '1'
			if abbinato:
				# NO, c'è già una scheda associata
				QMessageBox.warning( self, "RT Omero", u"La geometria selezionata appartiene ad un edificio già esistente" )
				return self.startCapture()
			else:
				# OK, non esiste alcuna scheda associata a tale geometria
				# associa la UV a tale geometria
				return self.assegnaGeomEsistente(feat)

		layerOrig = QgsMapLayerRegistry.instance().mapLayer( ManagerWindow.VLID_GEOM_ORIG )
		if layerOrig == None:
			return

		feat = self.pointEmitter.findAtPoint(layerOrig, point)		
		if feat != None:
			if not ManagerWindow.checkActionSpatialFromFeature( action, feat, False ):
				return

			# copia la geometria dal layer delle geometrie originali, quindi 
			# associa la UV alla nuova geometria creata
			return self.assegnaGeomNuova(feat)

		return self.startCapture()


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
			ManagerWindow.instance.aggiornaLayerModif()

	def setupLoader(self, ID=None):
		MultiTabSection.setupLoader(self, ID)

		# seleziona il tab contenente l'UV selezionata in canvas
		for index in range(self.tabWidget.count()):
			uvWidget = self.tabWidget.widget(index)
			if uvWidget.uvID == ManagerWindow.instance.uvScheda:
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
