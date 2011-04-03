# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dlgAbout.ui'
#
# Created: Sat Mar 26 13:52:07 2011
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DlgAbout(object):
    def setupUi(self, DlgAbout):
        DlgAbout.setObjectName("DlgAbout")
        DlgAbout.resize(639, 473)
        self.gridLayout = QtGui.QGridLayout(DlgAbout)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtGui.QDialogButtonBox(DlgAbout)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Help)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)
        self.txt = QtGui.QTextBrowser(DlgAbout)
        self.txt.setObjectName("txt")
        self.gridLayout.addWidget(self.txt, 0, 0, 1, 2)

        self.retranslateUi(DlgAbout)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DlgAbout.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DlgAbout.reject)
        QtCore.QMetaObject.connectSlotsByName(DlgAbout)

    def retranslateUi(self, DlgAbout):
        DlgAbout.setWindowTitle(QtGui.QApplication.translate("DlgAbout", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.txt.setHtml(QtGui.QApplication.translate("DlgAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Schede Edifici</span><span style=\" font-size:12pt; font-weight:600;\"> v. $PLUGIN_VER$ </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"></p>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Regione Toscana</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Sistema Informativo Territoriale Ambientale</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">http://www.regione.toscana.it/territorio/cartografia/index.html</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Questo plugin è distribuito con licenza GPLv2</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Database<span style=\" font-weight:600;\"> v. $DB_VER$ </span>   ultima modifica<span style=\" font-weight:600;\"> $DB_REV$ </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">$DB_PATH$ </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Versione Quantum GIS $QGIS_VER$ (r$QGIS_REV$)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

