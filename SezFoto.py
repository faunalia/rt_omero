# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgSezFoto_ui import Ui_Form
from AutomagicallyUpdater import *

class SezFoto(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "FOTO_EDIFICIO")
		self.setupUi(self)

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.listaFoto
		]
		self.setupValuesUpdater(childrenList)

		self.connect(self.selectFileBtn, SIGNAL( "clicked()" ), self.loadFile)

	def loadFile(self):
		supportedFormats = QImageReader.supportedImageFormats()
		supportedFormats = map( lambda x: "*.%s *.%s" % ( str(x).lower(), str(x).upper() ), supportedFormats )
		filterStr = "Immagini (%s);; Tutti i file (*);;" % " ".join( supportedFormats )

		filename = QFileDialog.getOpenFileName(self, self.tr( "Seleziona l'immagine" ), "", filterStr)
		if filename.isEmpty():
			return

		self.fileEdit.setText( filename )
		self.listaFoto.caricaImmagine( filename )

