
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from MultiTabSection import MultiTabSection
from WdgFoto import WdgFoto
from AutomagicallyUpdater import *

class WdgElencoFoto(MultiTabSection):

	def __init__(self, parent=None):
		self._hasTabs = False
		MultiTabSection.__init__(self, parent, WdgFoto, "Foto", "FOTO_GEOREF_FOTO_EDIFICIO", "FOTO_GEOREFID", "FOTO_EDIFICIOID")
		self.btnNew.setVisible( False )
		self.setVisible( False )

	def setVisible(self, enable):
		MultiTabSection.setVisible(self, enable)
		self._hasTabs = enable

	def hasTabs(self):
		return self._hasTabs

	def save(self):
		if not MultiTabSection.save(self):
			return False

		# rimuovi i vecchi ID dalle tabella di normalizzazione
		self._deleteValue(self._tableName, { self._parentPkColumn : self._ID })

		if not self.hasTabs():
			return True

		# inserisci i nuovi ID nella tabella di normalizzazione evitando i doppioni
		allChildren = self._recursiveChildrenRefs()
		newIDs = []
		for widget in allChildren:
			if isinstance(widget, MappingOne2One):
				if widget._ID in newIDs:
					continue
				newIDs.append( widget._ID )

				values = {
					self._parentPkColumn : self._ID, 
					self._pkColumn : widget._ID
				}
				self._insertValue( values, self._tableName, None )

		return True

	def setupLoader(self, ID=None):
		MultiTabSection.setupLoader(self, ID)
		self.setVisible( self.tabWidget.count() > 1 or self.tabWidget.widget(0)._ID != None )
		

	def aggiornaPulsanti(self):
		self.btnDelete.setEnabled(True)

	def deleteTab(self):
		index = self.tabWidget.currentIndex()
		if index < 0:
			return

		# elimina il tab
		widget = self.tabWidget.widget(index)
		ret = widget.delete() # elimina dal db
		self.delChildRef(widget)	# elimina il riferimento
		if self.tabWidget.count() == 1:
			self.setVisible(False)
		else:
			self.tabWidget.removeTab(index)
			del widget
		
		for i in range(0, self.tabWidget.count()):
			text = "%s%d" % (self.baseTabName, i+1)
			self.tabWidget.setTabText(i, QString(text) )
		return ret


	def caricaImmagine(self, filename):
		if self.hasTabs():
			index = self.addTab()
		else:
			index = 0
			self.addChildRef(self.tabWidget.widget(index))
		self.tabWidget.setCurrentIndex(index)

		widget = self.tabWidget.widget( index )
		if widget.caricaImmagine( filename ):
			self.setVisible(True)
		else:
			self.deleteTab()

