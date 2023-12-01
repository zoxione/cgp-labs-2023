import math
from typing import List, Tuple
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QColor, QPixmap

from src.algorithms.area_modified_stack_internal import area_modified_stack_internal
from src.algorithms.framing_sutherland_cohen import framing_sutherland_cohen
from src.algorithms.line_bresenham import line_bresenham
from src.classes.Container import Container
from src.classes.Polygon import Polygon
from src.classes.UniqueQueue import UniqueQueuePoints
from src.data.constants import LAYERS, Mode, FRAME_SIZES, IMAGES_SIZES, CELL_SIZE, BACKGROUND_COLOR
from src.handlers import draw_one, draw_all, change_layer, clear_all, upscale, toggle_show_grid, toggle_mode, \
	change_frame_sizes, add_texture


class Window(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		uic.loadUi("src/assets/window.ui", self)
		self.setWindowIcon(QtGui.QIcon('src/assets/logo.ico'))

		# Инициализация данных
		self._cell_size = CELL_SIZE
		self.current_mode = Mode.ALPHA
		self.container = Container(LAYERS, FRAME_SIZES)
		self.main_pixels_queue = UniqueQueuePoints([])
		self.texture = None

		# Настройка таймера
		self.draw_timer = QTimer()
		self.draw_timer.setInterval(0)
		self.draw_timer.timeout.connect(self.draw_next_pixel)

		# Инициализация текста
		self.currentLayerLabel.setText(f'Текущий слой: {self.container.current_layer_index}/{self.container.count_layers-1}')
		self.countPixelsInCellLabel.setText(f'Количество пикселей в ячейке: {self.cell_size ** 2}')
		self.timeSpentOverlapsLabel.setText(f'Затраченное время на растеризацию слоёв с отсечениями: ')
		self.timeSpentLabel.setText(f'Затраченное время на растеризацию слоёв без отсечений: ')
		self.frameSizeLabel.setText(f'{self.container.frame_sizes[0]}')

		# Настройка виджетов
		self.overlapCheckBox.setChecked(True)
		self.gridCheckBox.setChecked(False)
		self.frameSizeSlider.setValue(FRAME_SIZES[0])

		# Контейнер для изображения
		self.mainScene = QtWidgets.QGraphicsScene()
		self.mainGraphicsView.setScene(self.mainScene)
		self.mainImage = QImage(IMAGES_SIZES[0], IMAGES_SIZES[1], QImage.Format_ARGB32)
		self.mainImage.fill(QColor(*BACKGROUND_COLOR))

		# Рисуем сетку
		self.gridImage = QImage(IMAGES_SIZES[0], IMAGES_SIZES[1], QImage.Format_ARGB32)
		# self.draw_grid(QColor(*GRID_COLOR))

		self.update_scenes()

		# Обработчики нажатий
		self.drawOnePushButton.clicked.connect(lambda: draw_one(self))
		self.drawAllPushButton.clicked.connect(lambda: draw_all(self))
		self.backPushButton.clicked.connect(lambda: change_layer(self, "back"))
		self.forwardPushButton.clicked.connect(lambda: change_layer(self, "forward"))
		self.clearPushButton.clicked.connect(lambda: clear_all(self))
		self.upscalePushButton.clicked.connect(lambda: upscale(self))
		self.gridCheckBox.stateChanged.connect(lambda: toggle_show_grid(self))
		self.modeButtonGroup.buttonClicked.connect(lambda button: toggle_mode(self, button))
		self.frameSizeSlider.valueChanged.connect(lambda value: change_frame_sizes(self, value))
		self.texturePushButton.clicked.connect(lambda: add_texture(self))

	@property
	def cell_size(self):
		return self._cell_size

	@cell_size.setter
	def cell_size(self, value):
		self.countPixelsInCellLabel.setText(f'Количество пикселей в ячейке: {self.cell_size ** 2}')
		self._cell_size = value

	def change_buttons_state(self, state: bool):
		"""
		Метод для изменения состояния кнопок
		"""
		self.drawOnePushButton.setEnabled(state)
		self.drawAllPushButton.setEnabled(state)
		self.backPushButton.setEnabled(state)
		self.forwardPushButton.setEnabled(state)
		self.clearPushButton.setEnabled(state)
		self.upscalePushButton.setEnabled(state)
		self.gridCheckBox.setEnabled(state)
		for button in self.modeButtonGroup.buttons():
			button.setEnabled(state)
		self.frameSizeSlider.setEnabled(state)
		self.texturePushButton.setEnabled(state)

	def draw_pixel(self, image: QImage, x: int, y: int, color: QColor):
		"""
		Метод для рисования пикселя
		"""
		# Корректировка координат, чтобы пиксель соответствовал ячейке сетки
		image_x = image.width() // 2 + (x * self.cell_size)
		image_y = image.height() // 2 + (- y * self.cell_size)

		for i in range(self.cell_size):
			for j in range(self.cell_size):
				image.setPixel(image_x + i, image_y + j, color.rgb())

	def draw_next_pixel(self):
		"""
		Метод для рисования очередного пикселя
		"""
		if len(self.main_pixels_queue) > 0:
			x, y, color, layer_index = self.main_pixels_queue.pop()
			self.draw_pixel(self.mainImage, x, y, color)
			self.update_scenes()
			self.change_buttons_state(False)

		# Если очередь пустая
		if len(self.main_pixels_queue) == 0:
			self.draw_timer.stop()
			self.change_buttons_state(True)

	def get_pixel_color(self, x: int, y: int, layer_index: int) -> QColor:
		"""
		Функция для получения цвета пикселя
		"""
		for i in range(0, len(self.main_pixels_queue)):
			p_x, p_y, p_color, p_layer_index = self.main_pixels_queue[i]
			if x == p_x and y == p_y and layer_index == p_layer_index:
				return p_color

		return QColor(*BACKGROUND_COLOR)

	def draw_lines(self, polygon: Polygon, layer_index: int):
		"""
		Метод для рисования отрезков
		"""
		width, height = self.container.frame_sizes
		xl = -(width // 2)
		xr = width // 2
		yt = height // 2
		yb = -(height // 2)

		polygon.normalize()
		for i in range(0, len(polygon.points)):
			x1, y1 = polygon.points[i]
			x2, y2 = polygon.points[(i + 1) % len(polygon.points)]
			p1, p2 = framing_sutherland_cohen(xl, xr, yt, yb, (x1, y1), (x2, y2))
			if p1 is not None and p2 is not None:
				line_bresenham(self.main_pixels_queue, p1, p2, QColor(*polygon.contour_color), layer_index)

	def draw_areas(self, polygon: Polygon, layer_index: int):
		"""
		Метод для рисования областей
		"""
		width, height = self.container.frame_sizes
		xl = -(width // 2)
		xr = width // 2
		yt = height // 2
		yb = -(height // 2)

		framing_polygon = polygon.copy()
		framing_polygon.points = []
		for i in range(0, len(polygon.points)):
			x1, y1 = polygon.points[i]
			x2, y2 = polygon.points[(i + 1) % len(polygon.points)]
			p1, p2 = framing_sutherland_cohen(xl, xr, yt, yb, (x1, y1), (x2, y2))
			if p1 is not None:
				framing_polygon.points.append(p1)
			if p2 is not None:
				framing_polygon.points.append(p2)

		framing_polygon.normalize()
		if len(framing_polygon.points) > 2:
			center = framing_polygon.get_center()
			center_color = self.get_pixel_color(center[0], center[1], layer_index)
			area_modified_stack_internal(self, self.main_pixels_queue, center,  QColor(*polygon.fill_color), center_color, framing_polygon.points, layer_index)

	def update_scenes(self):
		"""
		Метод для обновления всех сцен
		"""
		self.mainScene.clear()

		scene_rect = self.mainScene.sceneRect()
		mainPixmap = QPixmap(scene_rect.size().toSize())
		mainPixmap.convertFromImage(self.mainImage)
		self.mainScene.addPixmap(mainPixmap)

		mainPixmap.convertFromImage(self.gridImage)
		self.mainScene.addPixmap(mainPixmap)

	def draw_grid(self, grid_color: QColor):
		"""
		Метод для рисования сетки
		"""
		width, height = self.gridImage.width(), self.gridImage.height()

		for x in range(0, width, self.cell_size):
			for y in range(0, height, self.cell_size):
				# Рисуем вертикальные линии с интервалом cell_size
				for i in range(self.cell_size):
					if x + i < width:
						self.gridImage.setPixel(x + i, y, grid_color.rgb())
				# Рисуем горизонтальные линии с интервалом cell_size
				for i in range(self.cell_size):
					if y + i < height:
						self.gridImage.setPixel(x, y + i, grid_color.rgb())

		# Рисуем координатную ось
		for x in range(0, width):
			if x == width // 2:
				for y in range(0, height):
					self.gridImage.setPixel(x, y, QColor(0, 0, 0).rgb())

		for y in range(0, height):
			if y == height // 2:
				for x in range(0, width):
					self.gridImage.setPixel(x, y, QColor(0, 0, 0).rgb())

		self.update_scenes()

	def resize_images(self, resize_factor):
		"""
		Метод для изменения размера всех изображений
		"""

		# width, height = self.mainImage.width(), self.mainImage.height()
		new_width = int(IMAGES_SIZES[0] * resize_factor)
		new_height = int(IMAGES_SIZES[1] * resize_factor)
		mainImage_old = self.mainImage.copy()
		self.mainImage = QImage(new_width, new_height, QImage.Format_ARGB32)

		# Метод ближайшего соседа
		for new_i in range(0, new_height):
			for new_j in range(0, new_width):
				i = math.floor(new_i / resize_factor)
				j = math.floor(new_j / resize_factor)
				self.mainImage.setPixel(new_i, new_j, mainImage_old.pixel(i, j))

		# Присваивание новых значений
		self.update_scenes()

	def get_color_texture(self, x: int, y: int) -> QColor:
		width, height = self.texture.width(), self.texture.height()
		return self.texture.pixelColor(x % width, y % height)
