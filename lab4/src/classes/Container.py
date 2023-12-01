from typing import List

from src.algorithms.framing_sutherland_cohen import framing_sutherland_cohen
from src.algorithms.overlap_sutherland_hodgman import overlap_sutherland_hodgman
from src.classes.Layer import Layer
from src.classes.Polygon import Polygon


class SingletonMetaclass(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]


class Container(metaclass=SingletonMetaclass):
	def __init__(self, layers, frame_sizes):
		self.layers: List[Layer] = layers
		self._count_layers = len(self.layers)
		self._current_layer_index = 0
		self._frame_sizes = frame_sizes

	@property
	def current_layer_index(self):
		return self._current_layer_index

	@current_layer_index.setter
	def current_layer_index(self, value):
		self._current_layer_index = value

	@property
	def current_layer(self):
		return self.layers[self.current_layer_index]

	@property
	def crop_layer(self):
		return self.layers[0]

	@property
	def count_layers(self):
		return self._count_layers

	@count_layers.setter
	def count_layers(self, value):
		self._count_layers = value

	@property
	def frame_sizes(self):
		return self._frame_sizes

	@frame_sizes.setter
	def frame_sizes(self, value):
		self._frame_sizes = value

	def find_overlap_polygons(self, current_polygon: Polygon, polygon: Polygon, index: int):
		overlap_polygon_points = overlap_sutherland_hodgman(current_polygon.points, polygon.points)
		if len(overlap_polygon_points) > 0:
			overlap_polygon = Polygon(polygon.fill_color, polygon.contour, polygon.contour_color, overlap_polygon_points)
			# Области
			self.current_layer.overlap_areas.append((overlap_polygon, self.current_layer_index - (index + 1)))
			# Отрезки
			if overlap_polygon == polygon:
				# Если многоугольник полностью вписан
				self.current_layer.overlap_lines.append((overlap_polygon, self.current_layer_index - (index + 1)))
			else:
				# Если нет, то сначала добавляем обводку цвета заливки
				self.current_layer.overlap_lines.append((
					Polygon(overlap_polygon.fill_color, overlap_polygon.contour, overlap_polygon.fill_color, overlap_polygon.points),
					self.current_layer_index - (index + 1)
				))
				# Потом добавляем контуры, которые видны
				xl, xr, yt, yb = current_polygon.get_minmax_points()
				for o in range(0, len(polygon.points)):
					x1, y1 = polygon.points[o]
					x2, y2 = polygon.points[(o + 1) % len(polygon.points)]
					p1, p2 = framing_sutherland_cohen(xl, xr, yt, yb, (x1, y1), (x2, y2))
					if p1 is not None and p2 is not None:
						self.current_layer.overlap_lines.append((
							Polygon(polygon.fill_color, polygon.contour, polygon.contour_color, [p1, p2]),
							self.current_layer_index - (index + 1)
						))

