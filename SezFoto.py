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
		supportedFormats = map( lambda x: "*.%s *.%s" % ( str(x).lower(), str(x).upper() ), supportedFormats )
		filterStr = "Immagini (%s);; Tutti i file (*);;" % " ".join( supportedFormats )

		lastDir = AutomagicallyUpdater._getLastUsedDir( 'foto' )
		filename = QFileDialog.getOpenFileName(self, self.tr( "Seleziona l'immagine" ), lastDir, filterStr)
		if filename.isEmpty():
			return
		AutomagicallyUpdater._setLastUsedDir( 'foto', filename )

		self.fileEdit.setText( filename )
		self.listaFoto.caricaImmagine( filename )

	def toHtml(self):
		# recupera la scheda
		wdg = self
		while not isinstance(wdg, QMainWindow) or not hasattr(wdg, 'creaStralcioCartografico'):
			if wdg.parent() == None:
				wdg = None
				break
			wdg = wdg.parent()

		filename = xmin = ymin = xmax = ymax = ""

		# dimensioni e scala originali
		realwidth = 700
		realscale = 1000

		# TRICK! aumenta la risoluzione dell'immagine
		# riduce la scala e ingrandisce le dimensioni dell'immagine in output
		factor = 1

		# size and scale will be passed to the map renderer
		renderwidth = realwidth * factor
		renderscale = realscale / factor

		# size of the image displayed in the HTML page
		printwidth = realwidth*1.1

		if wdg != None:
			filename, extent = wdg.creaStralcioCartografico( QSize(renderwidth, renderwidth), renderscale, "png", factor )
			filename = QUrl.fromLocalFile(filename).toString()
			if extent != None:
				xmin = extent.xMinimum()
				ymin = extent.yMinimum()
				xmax = extent.xMaximum()
				ymax = extent.yMaximum()

		return QString( u"""
<div id="sez8" class="block">
<p class="section">SEZIONE A8 - FOTOGRAFIE</p>
<table class="border">
	<tr>
		<td colspan="4">Stralcio cartografico dell'edificio</td>
	</tr>
	<tr>
		<td colspan="4" class="mapContainer"><img class="map border" style="width: %spx; height: %spx;" src="%s" alt="stralcio cartografico"></td>
	</tr>
	<tr>
		<td>xmin</td><td class="value">%s</td>
		<td>ymin</td><td class="value">%s</td>
	</tr>
	<tr>
		<td>xmax</td><td class="value">%s</td>
		<td>ymax</td><td class="value">%s</td>
	</tr>
</table>
%s
</div>
""" % ( printwidth, printwidth, filename, xmin, ymin, xmax, ymax, self.listaFoto.toHtml() ) 
)

