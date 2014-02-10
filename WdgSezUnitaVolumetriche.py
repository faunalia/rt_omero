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

from ui.wdgSezUnitaVolumetriche_ui import Ui_Form
from AutomagicallyUpdater import *

class WdgSezUnitaVolumetriche(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "SCHEDA_UNITA_VOLUMETRICA")
		self.setupUi(self)

		self.SCHEDA_EDIFICIOID.hide()
		self.uvID = None

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_MORFOLOGIA_COPERTURAID: AutomagicallyUpdater.ZZTable( "ZZ_MORFOLOGIA_COPERTURA" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.SCHEDA_EDIFICIOID, 
			self.INTERR_NPIANI,
			self.FUORITERR_NPIANI,
			self.ALTEZZA_VOLUME, 
			self.ZZ_MORFOLOGIA_COPERTURAID,
			self.MANTO_COPERTURA_UNITA_VOLUMETRICAID,
			(self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_ORDINARIID, AutomagicallyUpdater.OPTIONAL),
			(self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_GRANDI_LUCIID, AutomagicallyUpdater.OPTIONAL)
		]
		self.setupValuesUpdater(childrenList)

		self.connect(self.edificioOrdinarioRadio, SIGNAL("toggled(bool)"), self.abilitaTipoEdificio)
		self.abilitaTipoEdificio()

	def abilitaTipoEdificio(self):
		self.tipoEdificiStacked.setCurrentIndex( 1 if self.edificioGrandiLuciRadio.isChecked() else 0 )

	def setupLoader(self, ID=None):
		MappingOne2One.setupLoader(self, ID)

		IDEdificioOrd = self.getValue(self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_ORDINARIID)
		IDEdificioGrand = self.getValue(self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_GRANDI_LUCIID)
		enabler = True if IDEdificioOrd or not IDEdificioGrand else False
		self.edificioOrdinarioRadio.setChecked( enabler )
		self.edificioGrandiLuciRadio.setChecked( not enabler )

		# aggiorna le info di DEBUG sulla UV
		uvID = AutomagicallyUpdater.Query( "SELECT GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW FROM SCHEDA_UNITA_VOLUMETRICA WHERE ID_SCHEDA_UV = ?", [ID] ).getFirstResult()
		self.setUV( uvID )

	def save(self):
		if self.uvID == None:
			return False

		allChildren = self._recursiveChildrenRefs()

		# salva le tabelle collegate a questa con relazione Uno a Uno
		for parent, widget in allChildren:
			if isinstance(widget, MappingOne2One):
				if widget == self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_ORDINARIID:
					if not self.edificioOrdinarioRadio.isChecked():
						self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_ORDINARIID.delete()
						continue

				if widget == self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_GRANDI_LUCIID:
					if self.edificioOrdinarioRadio.isChecked():
						self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_GRANDI_LUCIID.delete()
						continue

				if not widget.save():
					return False

		values = {}
		for parent, widget in allChildren:
			if not isinstance(widget, (MappingOne2Many, MappingMany2Many)):
				value = parent.getValue(widget)

				if widget == self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_ORDINARIID:
					if not self.edificioOrdinarioRadio.isChecked():
						value = None

				if widget == self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_GRANDI_LUCIID:
					if self.edificioOrdinarioRadio.isChecked():
						value = None

				values[widget.objectName()] = value

		values["GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATEID_UV_NEW"] = self.uvID

		ID = self._saveValue(values, self._tableName, self._pkColumn, self._ID)
		if ID == None:
			return False

		self._ID = ID
		return True

	def delete(self):
		MappingOne2One.delete(self)

		# imposta la geometria come non abbinata a scheda
		AutomagicallyUpdater._updateValue( { "ABBINATO_A_SCHEDA" : '0' }, "GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE", "ID_UV_NEW", self.uvID )

		# elimina la geometria solo se si tratta di geometria non spezzata
		query = AutomagicallyUpdater.Query( "SELECT ZZ_STATO_GEOMETRIAID FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE WHERE ID_UV_NEW = ?", [self.uvID] )
		if query.getFirstResult() != '2':
			return self._deleteGeometria(self.uvID)

		return False


	def getUV(self):
		return self.uvID

	def setUV(self, uvID=None):
		self.uvID = uvID

		IDoldUV = AutomagicallyUpdater.Query( "SELECT GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE WHERE ID_UV_NEW = ?", [self.uvID] ).getFirstResult()
		self.setValue(self.codUvCensita, self.uvID)
		self.setValue(self.codUvOriginale, IDoldUV)

	def selectUV(self):
		# seleziona l'UV ma non centrarla
		from ManagerWindow import ManagerWindow
		ManagerWindow.instance.selezionaScheda(self.uvID, False)


	def toHtml(self, index):
		strutture_oriz_copertura = self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_ORDINARIID.toHtml() if self.getValue(self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_ORDINARIID) != None else self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_GRANDI_LUCIID.toHtml()
		return u"""
<table class="blue border">
	<tr class="line">
		<td class="middle subtitle" rowspan="2" width="5%%">UV%d</td>
		<td>ID_UV</td><td colspan="5" class="value">%s</td>
	</tr>
	<tr class="line">
		<td>N. piani interrati</td><td class="value">%s</td>
		<td class="line">N. piani f. t.</td><td class="value">%s</td>
		<td class="line">Altezza in gronda (m)</td><td class="value">%s</td>
	</tr>
</table>
<table class="yellow border">
	<tr class="line">
		<td class="subtitle" rowspan="3" width="5%%"></td>
		<td>Morfologia della copertura</td><td colspan="3" class="value">%s</td>
	</tr>
%s
</table>
%s
"""	% ( index+1, self._ID, self.getValue(self.INTERR_NPIANI), self.getValue(self.FUORITERR_NPIANI), self.getValue(self.ALTEZZA_VOLUME), self.ZZ_MORFOLOGIA_COPERTURAID.currentText(), self.MANTO_COPERTURA_UNITA_VOLUMETRICAID.toHtml(), strutture_oriz_copertura )
