# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/multipleChoise2Lists.ui'
#
# Created: Wed Nov 24 15:49:41 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MultipleChoise(object):
    def setupUi(self, MultipleChoise):
        MultipleChoise.setObjectName("MultipleChoise")
        MultipleChoise.resize(400, 134)
        self.gridLayout = QtGui.QGridLayout(MultipleChoise)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtGui.QLabel(MultipleChoise)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.nonSelezionateList = QtGui.QListView(MultipleChoise)
        self.nonSelezionateList.setObjectName("nonSelezionateList")
        self.verticalLayout_4.addWidget(self.nonSelezionateList)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 4, 1)
        spacerItem = QtGui.QSpacerItem(20, 27, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.btnAdd = QtGui.QPushButton(MultipleChoise)
        self.btnAdd.setObjectName("btnAdd")
        self.gridLayout.addWidget(self.btnAdd, 1, 1, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtGui.QLabel(MultipleChoise)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.selezionateList = QtGui.QListView(MultipleChoise)
        self.selezionateList.setObjectName("selezionateList")
        self.verticalLayout_3.addWidget(self.selezionateList)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 2, 4, 1)
        self.btnDel = QtGui.QPushButton(MultipleChoise)
        self.btnDel.setObjectName("btnDel")
        self.gridLayout.addWidget(self.btnDel, 2, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 27, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 1, 1, 1)

        self.retranslateUi(MultipleChoise)
        QtCore.QMetaObject.connectSlotsByName(MultipleChoise)

    def retranslateUi(self, MultipleChoise):
        MultipleChoise.setWindowTitle(QtGui.QApplication.translate("MultipleChoise", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MultipleChoise", "Non selezionate", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAdd.setText(QtGui.QApplication.translate("MultipleChoise", "Aggiungi >", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MultipleChoise", "Selezionate", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDel.setText(QtGui.QApplication.translate("MultipleChoise", "< Rimuovi", None, QtGui.QApplication.UnicodeUTF8))

