# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
from qgis.core import *

from ui.wdgSezUnitaVolumetriche_ui import Ui_Form
from AutomagicallyUpdater import *

from ManagerWindow import ManagerWindow

class WdgSezUnitaVolumetriche(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "SCHEDA_UNITA_VOLUMETRICA")
		self.setupUi(self)

		if not AutomagicallyUpdater.DEBUG:
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
		
		# salva le tabelle collegate a questa con relazione Uno a Uno
		for widget in self._recursiveChildrenRefs():
			if not ( isinstance(widget, MappingOne2Many) or isinstance(widget, MappingMany2Many) ):
				if not isinstance(widget, MappingOne2One):
					continue

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
		for widget in self._recursiveChildrenRefs():
			if not ( isinstance(widget, MappingOne2Many) or isinstance(widget, MappingMany2Many) ):
				value = self.getValue(widget)

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
		if IDoldUV == None:
			self.setValue(self.debugInfo, '')
		else:
			self.setValue(self.debugInfo, self.uvID + "\t" + IDoldUV)

	def selectUV(self):
		# seleziona l'UV ma non centrarla
		ManagerWindow.instance.selezionaScheda(self.uvID, False)


	def toHtml(self, index):
		strutture_oriz_copertura = self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_ORDINARIID.toHtml() if self.getValue(self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_ORDINARIID) != None else self.STRUTTURE_ORIZZONTALI_COPERTURA_EDIFICI_GRANDI_LUCIID.toHtml()
		return QString( u"""
<table class="blue border">
	<tr class="line">
		<td class="middle subtitle" rowspan="2" width="5%%">UV%d</td>
		<td>ID_UV</td><td colspan="3" class="value">%s</td>
	</tr>
	<tr class="line">
		<td>N. piani interrati</td><td class="value">%s</td>
		<td class="line">N. piani f. t.</td><td class="value">%s</td>
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
"""	% ( index+1, self._ID, self.getValue(self.INTERR_NPIANI), self.getValue(self.FUORITERR_NPIANI), self.ZZ_MORFOLOGIA_COPERTURAID.currentText(), self.MANTO_COPERTURA_UNITA_VOLUMETRICAID.toHtml(), strutture_oriz_copertura )
)
