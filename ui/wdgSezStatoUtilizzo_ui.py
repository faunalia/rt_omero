# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wdgSezStatoUtilizzo.ui'
#
# Created: Thu Jan 13 00:47:56 2011
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(541, 406)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_17 = QtGui.QLabel(Form)
        self.label_17.setObjectName("label_17")
        self.gridLayout_2.addWidget(self.label_17, 0, 0, 1, 1)
        self.ZZ_TIPOLOGIA_EDILIZIAID = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_TIPOLOGIA_EDILIZIAID.sizePolicy().hasHeightForWidth())
        self.ZZ_TIPOLOGIA_EDILIZIAID.setSizePolicy(sizePolicy)
        self.ZZ_TIPOLOGIA_EDILIZIAID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_TIPOLOGIA_EDILIZIAID.setObjectName("ZZ_TIPOLOGIA_EDILIZIAID")
        self.gridLayout_2.addWidget(self.ZZ_TIPOLOGIA_EDILIZIAID, 0, 1, 1, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.ZZ_STATO_EDIFICIOID = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_STATO_EDIFICIOID.sizePolicy().hasHeightForWidth())
        self.ZZ_STATO_EDIFICIOID.setSizePolicy(sizePolicy)
        self.ZZ_STATO_EDIFICIOID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_STATO_EDIFICIOID.setObjectName("ZZ_STATO_EDIFICIOID")
        self.gridLayout_2.addWidget(self.ZZ_STATO_EDIFICIOID, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.ZZ_FRUIZIONE_TEMPORALEID = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_FRUIZIONE_TEMPORALEID.sizePolicy().hasHeightForWidth())
        self.ZZ_FRUIZIONE_TEMPORALEID.setSizePolicy(sizePolicy)
        self.ZZ_FRUIZIONE_TEMPORALEID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_FRUIZIONE_TEMPORALEID.setObjectName("ZZ_FRUIZIONE_TEMPORALEID")
        self.gridLayout_2.addWidget(self.ZZ_FRUIZIONE_TEMPORALEID, 2, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 120))
        self.groupBox.setChecked(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.DESCRIZIONE_VISIVA = QtGui.QPlainTextEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DESCRIZIONE_VISIVA.sizePolicy().hasHeightForWidth())
        self.DESCRIZIONE_VISIVA.setSizePolicy(sizePolicy)
        self.DESCRIZIONE_VISIVA.setObjectName("DESCRIZIONE_VISIVA")
        self.gridLayout.addWidget(self.DESCRIZIONE_VISIVA, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 3, 0, 1, 2)
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_3 = QtGui.QGridLayout(self.tab)
        self.gridLayout_3.setHorizontalSpacing(9)
        self.gridLayout_3.setVerticalSpacing(3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 2, 1, 1)
        self.catUsoPrevalenteList = QtGui.QListView(self.tab)
        self.catUsoPrevalenteList.setObjectName("catUsoPrevalenteList")
        self.gridLayout_3.addWidget(self.catUsoPrevalenteList, 1, 0, 1, 1)
        self.catUsoPianoTerraList = QtGui.QListView(self.tab)
        self.catUsoPianoTerraList.setObjectName("catUsoPianoTerraList")
        self.gridLayout_3.addWidget(self.catUsoPianoTerraList, 1, 1, 1, 1)
        self.catUsoAltriPianiList = QtGui.QListView(self.tab)
        self.catUsoAltriPianiList.setObjectName("catUsoAltriPianiList")
        self.gridLayout_3.addWidget(self.catUsoAltriPianiList, 1, 2, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_7 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.groupBox_3 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.CATEGORIA_USO_PREVALENTE = MultipleChoiseCatUsoPrevalente(self.groupBox_3)
        self.CATEGORIA_USO_PREVALENTE.setObjectName("CATEGORIA_USO_PREVALENTE")
        self.gridLayout_6.addWidget(self.CATEGORIA_USO_PREVALENTE, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_9 = QtGui.QGridLayout(self.tab_3)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.groupBox_4 = QtGui.QGroupBox(self.tab_3)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_8 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.CATEGORIA_USO_PIANO_TERRA = MultipleChoiseCatUsoPianoTerra(self.groupBox_4)
        self.CATEGORIA_USO_PIANO_TERRA.setObjectName("CATEGORIA_USO_PIANO_TERRA")
        self.gridLayout_8.addWidget(self.CATEGORIA_USO_PIANO_TERRA, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_4 = QtGui.QGridLayout(self.tab_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox_2 = QtGui.QGroupBox(self.tab_4)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.CATEGORIA_USO_ALTRI_PIANI = MultipleChoiseCatUsoAltriPiani(self.groupBox_2)
        self.CATEGORIA_USO_ALTRI_PIANI.setObjectName("CATEGORIA_USO_ALTRI_PIANI")
        self.gridLayout_5.addWidget(self.CATEGORIA_USO_ALTRI_PIANI, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.gridLayout_2.addWidget(self.tabWidget, 4, 0, 1, 2)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("Form", "Tipologia edilizia", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Stato", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Fruizione temporale", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Descrizione visiva dello stato attuale", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Cat. uso prevalente", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Cat.uso piano terra", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Cat. uso altri piani", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Form", "Riepilogo", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("Form", "Categorie", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Form", "Uso prevalente", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("Form", "Categorie", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("Form", "Uso piano terra", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Form", "Categorie", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("Form", "Uso altri piani", None, QtGui.QApplication.UnicodeUTF8))

from ..MultipleChoiseCatUsoAltriPiani import MultipleChoiseCatUsoAltriPiani
from ..MultipleChoiseCatUsoPrevalente import MultipleChoiseCatUsoPrevalente
from ..MultipleChoiseCatUsoPianoTerra import MultipleChoiseCatUsoPianoTerra
