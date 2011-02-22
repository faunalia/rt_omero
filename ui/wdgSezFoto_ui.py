# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wdgSezFoto.ui'
#
# Created: Mon Feb 14 18:44:00 2011
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(589, 104)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.fileEdit = QtGui.QLineEdit(self.groupBox)
        self.fileEdit.setReadOnly(True)
        self.fileEdit.setObjectName("fileEdit")
        self.gridLayout.addWidget(self.fileEdit, 0, 1, 1, 1)
        self.selectFileBtn = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectFileBtn.sizePolicy().hasHeightForWidth())
        self.selectFileBtn.setSizePolicy(sizePolicy)
        self.selectFileBtn.setObjectName("selectFileBtn")
        self.gridLayout.addWidget(self.selectFileBtn, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.listaFoto = WdgElencoFoto(Form)
        self.listaFoto.setObjectName("listaFoto")
        self.gridLayout_2.addWidget(self.listaFoto, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Nuova Foto/Immagine", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Foto/immagine", None, QtGui.QApplication.UnicodeUTF8))
        self.selectFileBtn.setText(QtGui.QApplication.translate("Form", "Seleziona...", None, QtGui.QApplication.UnicodeUTF8))

from ..WdgElencoFoto import WdgElencoFoto
