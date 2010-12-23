# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/multiTabSection.ui'
#
# Created: Wed Dec 22 15:46:03 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MultiTabSection(object):
    def setupUi(self, MultiTabSection):
        MultiTabSection.setObjectName("MultiTabSection")
        MultiTabSection.resize(382, 248)
        self.gridLayout = QtGui.QGridLayout(MultiTabSection)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtGui.QTabWidget(MultiTabSection)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setObjectName("tabWidget")
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName("tab1")
        self.tabWidget.addTab(self.tab1, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 3)
        self.btnDelete = QtGui.QPushButton(MultiTabSection)
        self.btnDelete.setObjectName("btnDelete")
        self.gridLayout.addWidget(self.btnDelete, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(197, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.btnNew = QtGui.QPushButton(MultiTabSection)
        self.btnNew.setObjectName("btnNew")
        self.gridLayout.addWidget(self.btnNew, 1, 2, 1, 1)

        self.retranslateUi(MultiTabSection)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MultiTabSection)

    def retranslateUi(self, MultiTabSection):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QtGui.QApplication.translate("MultiTabSection", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDelete.setText(QtGui.QApplication.translate("MultiTabSection", "Elimina", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNew.setText(QtGui.QApplication.translate("MultiTabSection", "Nuovo", None, QtGui.QApplication.UnicodeUTF8))

