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

from MultiTabSection import MultiTabSection
from WdgFoto import WdgFoto
from AutomagicallyUpdater import *

class WdgElencoFoto(MultiTabSection):

	def __init__(self, parent=None):
		self._hasTabs = True	# per creare il primo tab di tipo WdgFoto
		MultiTabSection.__init__(self, parent, WdgFoto, "Foto", "FOTO_GEOREF", None, "SCHEDA_EDIFICIOID")
		self.btnNew.setVisible( False )
		self.deleteTab()

	def aggiornaPulsanti(self):
		self.btnDelete.setEnabled(True)

	def setHasTabs(self, enable):
		MultiTabSection.setVisible(self, enable)
		self._hasTabs = enable

	def hasTabs(self):
		return self._hasTabs


	def setupLoader(self, ID=None):
		MultiTabSection.setupLoader(self, ID)
		self.setHasTabs( self.tabWidget.count() > 1 or self.tabWidget.widget(0)._ID != None )

	def _computeAction(self, action):
		# recupera le foto ordinate secondo ZZ_FRONTE_EDIFICIOID
		query = "SELECT %s FROM %s WHERE %s = :id ORDER BY abs(ZZ_FRONTE_EDIFICIOID) ASC" % ( self._pkColumn, self._tableName, self._parentPkColumn )
		return AutomagicallyUpdater.Query( query )


	def addTab(self):
		if not self.hasTabs():
			index = 0
		else:
			index = self.tabWidget.addTab(self.basePageWidget(), "")
		text = "%s%d" % (self.baseTabName, index+1)
		self.tabWidget.setTabText(index, text )
		self.addChildRef(self.tabWidget.widget(index))
		self.setHasTabs(True)
		return index

	def deleteTab(self):
		index = self.tabWidget.currentIndex()
		if index < 0:
			return

		# elimina il tab
		widget = self.tabWidget.widget(index)
		ret = widget.delete() # elimina dal db
		self.delChildRef(widget)	# elimina il riferimento
		if self.tabWidget.count() == 1:
			self.setHasTabs(False)
		else:
			self.tabWidget.removeTab(index)
			del widget
		
		for i in range(0, self.tabWidget.count()):
			text = "%s%d" % (self.baseTabName, i+1)
			self.tabWidget.setTabText(i, text )
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
			self.setHasTabs(True)
		else:
			self.deleteTab()

	def toHtml(self, prefix=None):
		if not self.hasTabs():
			return ""
		return MultiTabSection.toHtml(self, prefix)
