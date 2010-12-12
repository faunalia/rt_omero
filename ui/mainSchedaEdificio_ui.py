# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainSchedaEdificio.ui'
#
# Created: Wed Nov 24 15:49:41 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SchedaEdificio(object):
    def setupUi(self, SchedaEdificio):
        SchedaEdificio.setObjectName("SchedaEdificio")
        SchedaEdificio.resize(868, 524)
        self.centralwidget = QtGui.QWidget(SchedaEdificio)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.sectionsList = QtGui.QListWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sectionsList.sizePolicy().hasHeightForWidth())
        self.sectionsList.setSizePolicy(sizePolicy)
        self.sectionsList.setAlternatingRowColors(True)
        self.sectionsList.setObjectName("sectionsList")
        QtGui.QListWidgetItem(self.sectionsList)
        QtGui.QListWidgetItem(self.sectionsList)
        QtGui.QListWidgetItem(self.sectionsList)
        QtGui.QListWidgetItem(self.sectionsList)
        QtGui.QListWidgetItem(self.sectionsList)
        QtGui.QListWidgetItem(self.sectionsList)
        QtGui.QListWidgetItem(self.sectionsList)
        QtGui.QListWidgetItem(self.sectionsList)
        self.verticalLayout.addWidget(self.sectionsList)
        self.sectionsStacked = QtGui.QStackedWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sectionsStacked.sizePolicy().hasHeightForWidth())
        self.sectionsStacked.setSizePolicy(sizePolicy)
        self.sectionsStacked.setObjectName("sectionsStacked")
        self.PRINCIPALE = SezPrincipale()
        self.PRINCIPALE.setObjectName("PRINCIPALE")
        self.sectionsStacked.addWidget(self.PRINCIPALE)
        self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ = SezLocalizzazione()
        self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.setObjectName("LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ")
        self.sectionsStacked.addWidget(self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ)
        self.UNITA_VOLUMETRICHE = SezUnitaVolumetriche()
        self.UNITA_VOLUMETRICHE.setObjectName("UNITA_VOLUMETRICHE")
        self.sectionsStacked.addWidget(self.UNITA_VOLUMETRICHE)
        self.INTERVENTI = SezInterventi()
        self.INTERVENTI.setObjectName("INTERVENTI")
        self.sectionsStacked.addWidget(self.INTERVENTI)
        self.STATO_UTILIZZO_EDIFICIOID = SezStatoUtilizzo()
        self.STATO_UTILIZZO_EDIFICIOID.setObjectName("STATO_UTILIZZO_EDIFICIOID")
        self.sectionsStacked.addWidget(self.STATO_UTILIZZO_EDIFICIOID)
        self.CARATTERISTICHE_STRUTTURALI = SezCaratteristicheStrutturali()
        self.CARATTERISTICHE_STRUTTURALI.setObjectName("CARATTERISTICHE_STRUTTURALI")
        self.sectionsStacked.addWidget(self.CARATTERISTICHE_STRUTTURALI)
        self.CARATTERISTICHE_ARCHITETTONICHE_EDIFICIOID = SezCaratteristicheArchitettoniche()
        self.CARATTERISTICHE_ARCHITETTONICHE_EDIFICIOID.setObjectName("CARATTERISTICHE_ARCHITETTONICHE_EDIFICIOID")
        self.sectionsStacked.addWidget(self.CARATTERISTICHE_ARCHITETTONICHE_EDIFICIOID)
        self.FOTO_IMMAGINI = QtGui.QWidget()
        self.FOTO_IMMAGINI.setObjectName("FOTO_IMMAGINI")
        self.sectionsStacked.addWidget(self.FOTO_IMMAGINI)
        self.verticalLayout_2.addWidget(self.splitter)
        SchedaEdificio.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(SchedaEdificio)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 868, 25))
        self.menubar.setObjectName("menubar")
        SchedaEdificio.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(SchedaEdificio)
        self.statusbar.setObjectName("statusbar")
        SchedaEdificio.setStatusBar(self.statusbar)

        self.retranslateUi(SchedaEdificio)
        self.sectionsList.setCurrentRow(0)
        self.sectionsStacked.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(SchedaEdificio)

    def retranslateUi(self, SchedaEdificio):
        SchedaEdificio.setWindowTitle(QtGui.QApplication.translate("SchedaEdificio", "Scheda Edificio", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SchedaEdificio", "Sezioni", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.sectionsList.isSortingEnabled()
        self.sectionsList.setSortingEnabled(False)
        self.sectionsList.item(0).setText(QtGui.QApplication.translate("SchedaEdificio", "A1 - Sezione Principale", None, QtGui.QApplication.UnicodeUTF8))
        self.sectionsList.item(1).setText(QtGui.QApplication.translate("SchedaEdificio", "A2 - Localizzazione edificio", None, QtGui.QApplication.UnicodeUTF8))
        self.sectionsList.item(2).setText(QtGui.QApplication.translate("SchedaEdificio", "A3 - Unità volumetriche", None, QtGui.QApplication.UnicodeUTF8))
        self.sectionsList.item(3).setText(QtGui.QApplication.translate("SchedaEdificio", "A4 - Interventi strutturali", None, QtGui.QApplication.UnicodeUTF8))
        self.sectionsList.item(4).setText(QtGui.QApplication.translate("SchedaEdificio", "A5 - Stato e utilizzo", None, QtGui.QApplication.UnicodeUTF8))
        self.sectionsList.item(5).setText(QtGui.QApplication.translate("SchedaEdificio", "A6 - Caratteristiche strutturali", None, QtGui.QApplication.UnicodeUTF8))
        self.sectionsList.item(6).setText(QtGui.QApplication.translate("SchedaEdificio", "A7 - Caratteristiche architettoniche", None, QtGui.QApplication.UnicodeUTF8))
        self.sectionsList.item(7).setText(QtGui.QApplication.translate("SchedaEdificio", "A8 - Foto e immagini", None, QtGui.QApplication.UnicodeUTF8))
        self.sectionsList.setSortingEnabled(__sortingEnabled)

from ..SezLocalizzazione import SezLocalizzazione
from ..SezUnitaVolumetriche import SezUnitaVolumetriche
from ..SezCaratteristicheArchitettoniche import SezCaratteristicheArchitettoniche
from ..SezStatoUtilizzo import SezStatoUtilizzo
from ..SezCaratteristicheStrutturali import SezCaratteristicheStrutturali
from ..SezPrincipale import SezPrincipale
from ..SezInterventi import SezInterventi
