# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
import qgis.gui

class MapTool(QObject):
	canvas = None

	def __init__(self, mapToolClass, canvas=None):
		QObject.__init__(self)
		if canvas == None:
			if MapTool.canvas == None:
				raise Exception( "MapTool.canvas is None" )
			else:
				self.canvas = MapTool.canvas
		else:
			self.canvas = canvas

		self.tool = mapToolClass( self.canvas )
		QObject.connect(self.tool, SIGNAL( "geometryDrawingEnded(const QgsGeometry *)" ), self.onEnd)

	def onEnd(self, geometry):
		if geometry == None:
			return
		self.stopCapture()
		self.emit( SIGNAL( "geometryEmitted(const QgsGeometry *)" ), geometry )

	def startCapture(self):
		self.canvas.setMapTool( self.tool )

	def stopCapture(self):
		self.canvas.unsetMapTool( self.tool )

	class Drawer(qgis.gui.QgsMapToolEmitPoint):
		def __init__(self, canvas, isPolygon=False):
			self.canvas = canvas
			self.isPolygon = isPolygon
			qgis.gui.QgsMapToolEmitPoint.__init__(self, self.canvas)

			self.rubberBand = qgis.gui.QgsRubberBand( self.canvas, self.isPolygon )
			self.rubberBand.setColor( Qt.red )
			self.rubberBand.setWidth( 1 )

			self.isEmittingPoints = False

		def reset(self):
			self.isEmittingPoints = False
			self.rubberBand.reset( self.isPolygon )

		def canvasPressEvent(self, e):
			if e.button() == Qt.RightButton:
				self.isEmittingPoints = False
				self.emit( SIGNAL("geometryDrawingEnded(const QgsGeometry *)"), self.geometry() )
				return

			if e.button() == Qt.LeftButton:
				self.isEmittingPoints = True
			else:
				return
			point = self.toMapCoordinates( e.pos() )
			self.rubberBand.addPoint( point, True )	# true to update canvas
			self.rubberBand.show()

		def canvasMoveEvent(self, e):
			if not self.isEmittingPoints:
				return

			point = self.toMapCoordinates( e.pos() )
			self.rubberBand.movePoint( point )

		def isValid(self):
			return self.rubberBand.numberOfVertices() > 0

		def geometry(self):
			if not self.isValid():
				return None
			return QgsGeometry.fromWkt( self.rubberBand.asGeometry().exportToWkt() )

		def deactivate(self):
			qgis.gui.QgsMapTool.deactivate(self)
			self.reset()
			self.emit(SIGNAL("deactivated()"))


class FeatureFinder(MapTool):

	def __init__(self, canvas=None):
		MapTool.__init__(self, qgis.gui.QgsMapToolEmitPoint, canvas=canvas)
		QObject.connect(self.tool, SIGNAL( "canvasClicked(const QgsPoint &, Qt::MouseButton)" ), self.onEnd)

	def onEnd(self, point, button):
		self.stopCapture()
		self.emit( SIGNAL("pointEmitted(const QgsPoint &, Qt::MouseButton)"), point, button )

	def findAtPoint(self, layer, point):
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		# recupera il valore del raggio di ricerca
		settings = QSettings()
		(radius, ok) = settings.value( "/Map/identifyRadius", QGis.DEFAULT_IDENTIFY_RADIUS ).toDouble()
		if not ok or radius <= 0:
			radius = QGis.DEFAULT_IDENTIFY_RADIUS
		radius = self.canvas.extent().width() * radius/100

		# crea il rettangolo da usare per la ricerca
		rect = QgsRectangle()
		rect.setXMinimum(point.x() - radius)
		rect.setXMaximum(point.x() + radius)
		rect.setYMinimum(point.y() - radius)
		rect.setYMaximum(point.y() + radius)
		rect = self.canvas.mapRenderer().mapToLayerCoordinates(layer, rect)

		# recupera le feature che intersecano il rettangolo
		layer.select([], rect, True, True)

		minDist = -1
		featureId = None
		rect = QgsGeometry.fromRect(rect)
		count = 0

		f = QgsFeature()
		while layer.nextFeature(f):
			geom = f.geometry()
			distance = geom.distance(rect)
			if minDist < 0 or distance < minDist:
				minDist = distance
				featureId = f.id()

		if featureId != None:
			layer.featureAtId(featureId, f, True, True)
		else:
			f = None

		QApplication.restoreOverrideCursor()
		return f

class PolygonDrawer(MapTool):

	class PolygonDrawer(MapTool.Drawer):
		def __init__(self, canvas):
			MapTool.Drawer.__init__(self, canvas, True)

	def __init__(self, canvas=None):
		MapTool.__init__(self, self.PolygonDrawer, canvas)

class LineDrawer(MapTool):

	class LineDrawer(MapTool.Drawer):
		def __init__(self, canvas):
			MapTool.Drawer.__init__(self, canvas, False)

	def __init__(self, canvas=None):
		MapTool.__init__(self, self.LineDrawer, canvas)

