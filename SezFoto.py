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

from ui.wdgSezFoto_ui import Ui_Form
from AutomagicallyUpdater import *
from Utils import Porting

class SezFoto(QWidget, MappingPart, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingPart.__init__(self, "SCHEDA_EDIFICIO")
		self.setupUi(self)

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.listaFoto
		]
		self.setupValuesUpdater(childrenList)

		self.connect(self.selectFileBtn, SIGNAL( "clicked()" ), self.loadFile)

	def loadFile(self):
		supportedFormats = QImageReader.supportedImageFormats()
		supportedFormats = map( lambda x: "*.%s *.%s" % ( Porting.str(x).lower(), Porting.str(x).upper() ), supportedFormats )
		filterStr = "Immagini (%s);; Tutti i file (*);;" % " ".join( supportedFormats )

		lastDir = AutomagicallyUpdater._getLastUsedDir( 'foto' )
		filename = QFileDialog.getOpenFileName(self, self.tr( "Seleziona l'immagine" ), lastDir, filterStr)
		if filename == "":
			return
		AutomagicallyUpdater._setLastUsedDir( 'foto', filename )

		self.fileEdit.setText( filename )
		self.listaFoto.caricaImmagine( filename )

	def toHtml(self, prefix=None):
		return self.listaFoto.toHtml(prefix)

