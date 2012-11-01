# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dlgSettings.ui'
#
# Created: Thu Nov  1 22:55:05 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(414, 271)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.printModeGroup = QtGui.QGroupBox(self.groupBox)
        self.printModeGroup.setObjectName(_fromUtf8("printModeGroup"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.printModeGroup)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.printDefaultRadio = QtGui.QRadioButton(self.printModeGroup)
        self.printDefaultRadio.setObjectName(_fromUtf8("printDefaultRadio"))
        self.verticalLayout_2.addWidget(self.printDefaultRadio)
        self.printPdfRadio = QtGui.QRadioButton(self.printModeGroup)
        self.printPdfRadio.setChecked(True)
        self.printPdfRadio.setObjectName(_fromUtf8("printPdfRadio"))
        self.verticalLayout_2.addWidget(self.printPdfRadio)
        self.printHtmlRadio = QtGui.QRadioButton(self.printModeGroup)
        self.printHtmlRadio.setObjectName(_fromUtf8("printHtmlRadio"))
        self.verticalLayout_2.addWidget(self.printHtmlRadio)
        self.verticalLayout.addWidget(self.printModeGroup)
        self.printPdfResGroup = QtGui.QGroupBox(self.groupBox)
        self.printPdfResGroup.setObjectName(_fromUtf8("printPdfResGroup"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.printPdfResGroup)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.printPdfHighResRadio = QtGui.QRadioButton(self.printPdfResGroup)
        self.printPdfHighResRadio.setChecked(True)
        self.printPdfHighResRadio.setObjectName(_fromUtf8("printPdfHighResRadio"))
        self.horizontalLayout_2.addWidget(self.printPdfHighResRadio)
        self.printPdfLowResRadio = QtGui.QRadioButton(self.printPdfResGroup)
        self.printPdfLowResRadio.setObjectName(_fromUtf8("printPdfLowResRadio"))
        self.horizontalLayout_2.addWidget(self.printPdfLowResRadio)
        self.verticalLayout.addWidget(self.printPdfResGroup)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.printPdfRadio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.printPdfResGroup.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Impostazioni", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Stampe", None, QtGui.QApplication.UnicodeUTF8))
        self.printModeGroup.setTitle(QtGui.QApplication.translate("Dialog", "Opzioni di stampa", None, QtGui.QApplication.UnicodeUTF8))
        self.printDefaultRadio.setText(QtGui.QApplication.translate("Dialog", "mostra finestra di stampa", None, QtGui.QApplication.UnicodeUTF8))
        self.printPdfRadio.setText(QtGui.QApplication.translate("Dialog", "stampa su PDF", None, QtGui.QApplication.UnicodeUTF8))
        self.printHtmlRadio.setText(QtGui.QApplication.translate("Dialog", "stampa in HTML", None, QtGui.QApplication.UnicodeUTF8))
        self.printPdfResGroup.setTitle(QtGui.QApplication.translate("Dialog", "Risoluzione PDF", None, QtGui.QApplication.UnicodeUTF8))
        self.printPdfHighResRadio.setText(QtGui.QApplication.translate("Dialog", "alta", None, QtGui.QApplication.UnicodeUTF8))
        self.printPdfLowResRadio.setText(QtGui.QApplication.translate("Dialog", "bassa", None, QtGui.QApplication.UnicodeUTF8))

