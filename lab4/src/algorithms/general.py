from typing import Tuple
from src.classes.Layer import Layer
from src.classes.Polygon import Polygon
from src.data.constants import Color, TRANSPARENT_COLOR, Mode


def is_inside_polygon(point, points):
	x, y = point
	n = len(points)
	inside = False

	p1x, p1y = points[0]
	for i in range(n + 1):
		p2x, p2y = points[i % n]
		if y > min(p1y, p2y):
			if y <= max(p1y, p2y):
				if x <= max(p1x, p2x):
					if p1y != p2y:
						xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
						if p1x == p2x or x <= xinters:
							inside = not inside
		p1x, p1y = p2x, p2y

	return inside


def alternative_color(color: Tuple[int, int, int]):
	new_color = ()
	for i in range(len(color)):
		new_color += (255 - color[i],)
	return Color.RED.value


def draw_one_layer(win, current_layer: Layer, current_layer_index: int):
	"""
	Обработчик нажатия на кнопку для рисования текущего полигона
	"""
	for i in range(0, len(current_layer.polygons)):
		current_polygon: Polygon = current_layer.polygons[i].copy()

		if current_layer_index == 0:
			win.draw_lines(current_layer.polygons[0], 0)
		else:
			# Поиск перекрытий по прошлым многоугольникам текущего слоя
			if win.overlapCheckBox.isChecked():
				prev_polygons = current_layer.polygons[0:i]
				for polygon in prev_polygons:
					win.container.find_overlap_polygons(current_polygon, polygon, current_layer_index)

			# Поиск перекрытий по каждому многоугольнику предыдущих слоев
			if win.overlapCheckBox.isChecked():
				prev_layers = win.container.layers[1:current_layer_index]
				prev_layers.reverse()
				for j in range(0, len(prev_layers)):
					for polygon in prev_layers[j].polygons:
						win.container.find_overlap_polygons(current_polygon, polygon, j)

			# Отрисовка исходного многоугольника
			win.draw_lines(current_polygon, current_layer_index)
			win.draw_areas(current_polygon, current_layer_index)

			# Закраска всех перекрытий
			if win.overlapCheckBox.isChecked():
				for index in range(current_layer_index - 1, 0, -1):
					for line in current_layer.overlap_lines:
						if index == line[1]:
							if win.current_mode == Mode.ALPHA:
								line[0].contour_color = TRANSPARENT_COLOR
							elif win.current_mode == Mode.BRAVO:
								line[0].contour_color = alternative_color(line[0].contour_color)
							win.draw_lines(line[0], line[1])
					for area in current_layer.overlap_areas:
						if index == area[1]:
							if win.current_mode == Mode.ALPHA:
								area[0].fill_color = TRANSPARENT_COLOR
							elif win.current_mode == Mode.BRAVO:
								area[0].fill_color = alternative_color(area[0].fill_color)
							win.draw_areas(area[0], area[1])
