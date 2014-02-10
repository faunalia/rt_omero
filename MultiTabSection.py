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

from ui.multiTabSection_ui import Ui_MultiTabSection
from AutomagicallyUpdater import *

class MultiTabSection(QWidget, MappingOne2Many, Ui_MultiTabSection):

	def __init__(self, parent=None, basePageWidget=QWidget, baseTabName="Tab ", table=None, pk=None, parentPk=None):
		QWidget.__init__(self, parent)
		MappingOne2Many.__init__(self, table, pk, parentPk)
		self.setupUi(self)

		self.baseTabName = baseTabName
		self.basePageWidget = basePageWidget

		self.clear()

		self.connect(self.tabWidget, SIGNAL( "currentChanged(int)" ), self.aggiornaPulsanti)
		self.connect(self.btnDelete, SIGNAL( "clicked()" ), self.btnDeleteTabClicked)
		self.connect(self.btnNew, SIGNAL( "clicked()" ), self.btnAddTabClicked)

		self.aggiornaPulsanti()

	def clear(self):
		for i in range(self.tabWidget.count()):
			w = self.tabWidget.widget(0)
			self.tabWidget.removeTab(0)
			del w

		self.tabWidget.clear()
		first = self.addTab()
		

	def aggiornaPulsanti(self):
		self.btnDelete.setEnabled(self.tabWidget.currentIndex() > 0)


	def btnDeleteTabClicked(self):
		self.deleteTab()

	def deleteTab(self):
		index = self.tabWidget.currentIndex()
		if index <= 0:
			return

		widget = self.tabWidget.widget(index)
		ret = widget.delete() # elimina dal db
		self.delChildRef(widget)	# elimina il riferimento
		self.tabWidget.removeTab(index)
		del widget
		
		for i in range(1, self.tabWidget.count()):
			text = "%s%d" % (self.baseTabName, i+1)
			self.tabWidget.setTabText(i, str(text) )
		return ret

	def btnAddTabClicked(self):
		index = self.addTab()
		self.tabWidget.setCurrentIndex(index)

	def addTab(self):
		index = self.tabWidget.addTab(self.basePageWidget(), "")
		text = "%s%d" % (self.baseTabName, index+1)
		self.tabWidget.setTabText(index, str(text) )
		self.addChildRef(self.tabWidget.widget(index))
		return index

	def setBaseTabName(self, name):
		self.baseTabName = name

	def setBasePageWidget(self, widget):
		self.basePageWidget = widget

	def setBaseTab(self, widget, name):
		self.setBasePageWidget(widget)
		self.setBaseTabName(name)


	def addNewChild(self):
		self.addTab()
		return True

	#def setupLoader(self, ID=None):
	#	MappingOne2Many.setupUpdater(self, ID)
	#	self.tabWidget.setCurrentIndex(0)

	def toHtml(self, *args, **kwargs):
		html = ""
		for index in range(self.tabWidget.count()):
			html += self.tabWidget.widget(index).toHtml(index, *args, **kwargs)
		return html
