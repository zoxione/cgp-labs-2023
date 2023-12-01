import time
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QFileDialog
from src.algorithms.framing_sutherland_cohen import framing_sutherland_cohen
from src.algorithms.general import alternative_color
from src.algorithms.overlap_sutherland_hodgman import overlap_sutherland_hodgman
from src.classes.Polygon import Polygon
from src.data.constants import Mode, GRID_COLOR, BACKGROUND_COLOR, Color


def draw_one(win):
	"""
	Обработчик нажатия на кнопку для рисования текущего полигона
	"""
	start_time = time.perf_counter()
	win.draw_timer.start()

	for i in range(0, len(win.container.current_layer.polygons)):
		current_polygon: Polygon = win.container.current_layer.polygons[i].copy()

		if win.container.current_layer_index == 0:
			win.draw_lines(win.container.crop_layer.polygons[0], 0)
		else:
			# Поиск перекрытий по прошлым многоугольникам текущего слоя
			prev_polygons = win.container.current_layer.polygons[0:i]
			for polygon in prev_polygons:
				win.container.find_overlap_polygons(current_polygon, polygon, win.container.current_layer_index)

			# Поиск перекрытий по каждому многоугольнику предыдущих слоев
			prev_layers = win.container.layers[1:win.container.current_layer_index]
			prev_layers.reverse()
			for j in range(0, len(prev_layers)):
				for polygon in prev_layers[j].polygons:
					win.container.find_overlap_polygons(current_polygon, polygon, j)

			# Отрисовка исходного многоугольника
			win.draw_lines(current_polygon, win.container.current_layer_index)
			win.draw_areas(current_polygon, win.container.current_layer_index)

			if win.overlapCheckBox.isChecked():
				# Закраска всех перекрытий
				for index in range(win.container.current_layer_index - 1, 0, -1):
					for line in win.container.current_layer.overlap_lines:
						if index == line[1]:
							if win.current_mode == Mode.BETA:
								line[0].contour_color = alternative_color(line[0].contour_color)
							win.draw_lines(line[0], line[1])
					for area in win.container.current_layer.overlap_areas:
						if index == area[1]:
							if win.current_mode == Mode.BETA:
								area[0].fill_color = alternative_color(area[0].fill_color)
							win.draw_areas(area[0], area[1])

	end_time = time.perf_counter()
	execution_time = (end_time - start_time) * 1000
	if win.overlapCheckBox.isChecked():
		win.timeSpentOverlapsLabel.setText(f'Затраченное время на растеризацию слоёв с отсечениями: {execution_time:.4f}')
	else:
		win.timeSpentLabel.setText(f'Затраченное время на растеризацию слоёв без отсечений: {execution_time:.4f}')


def draw_all(win):
	pass


def change_layer(win, mode: str):
	"""
	Обработчик нажатия на кнопку для изменения номера полигона
	"""
	if mode == "back":
		win.container.current_layer_index = (win.container.current_layer_index - 1) % win.container.count_layers
	if mode == "forward":
		win.container.current_layer_index = (win.container.current_layer_index + 1) % win.container.count_layers
	win.currentLayerLabel.setText(f'Текущий слой: {win.container.current_layer_index}/{win.container.count_layers - 1}')


def clear_all(win):
	"""
	Обработчик нажатия на кнопку для очистки изображений
	"""
	win.mainImage.fill(QColor(*BACKGROUND_COLOR))
	win.update_scenes()


def upscale(win):
	"""
	Обработчик нажатия на кнопку для увеличения изображений
	"""
	resize_factor = win.resizeDoubleSpinBox.value()
	win.resize_images(resize_factor)


def toggle_show_grid(win):
	"""
	Обработчик нажатия на кнопку для отображения/скрытия сетки
	"""
	state = win.gridCheckBox.isChecked()
	if state:
		grid_color = QColor(*GRID_COLOR)
	else:
		grid_color = QColor(*BACKGROUND_COLOR)

	win.draw_grid(grid_color)


def toggle_mode(win, clicked_button):
	if win.modeAlphaRadioButton == clicked_button:
		win.current_mode = Mode.ALPHA
	elif win.modeBetaRadioButton == clicked_button:
		win.current_mode = Mode.BETA


def change_frame_sizes(win, value):
	win.container.frame_sizes = (value, value)
	win.container.crop_layer.polygons[0].points = [
		(-(win.container.frame_sizes[0] // 2), -(win.container.frame_sizes[1] // 2)),
		(-(win.container.frame_sizes[0] // 2), (win.container.frame_sizes[1] // 2)),
		((win.container.frame_sizes[0] // 2), (win.container.frame_sizes[1] // 2)),
		((win.container.frame_sizes[0] // 2), -(win.container.frame_sizes[1] // 2))
	]
	win.frameSizeLabel.setText(f'{win.container.frame_sizes[0]}')


def add_texture(win):
	"""
	Обработчик нажатия на кнопку для добавления текстуры
	"""
	file = QFileDialog.getOpenFileName(win, "Open File", "textures/", "All Files (*);;PNG Files (*.png);;Jpg Files (*.jpg)")
	pixmap = QPixmap(file[0])
	win.texture = pixmap.toImage()
