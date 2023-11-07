import time
from typing import List, Tuple
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QColor, QPixmap
import sys


from algorithms import line_DDA, line_bresenham, area_recursive_internal, area_modified_stack_internal, get_pixel_color
from constants import GRID_COLOR, IMAGES_SIZES, CELL_SIZE
from handlers import start_draw, show_grid, upscale, downscale, clear_all, add_texture, change_polygon, \
	show_differences, calculate_lines_metrics, calculate_areas_metrics, show_count_draw_pixels


def measure_execution_time(func, *args):
	start_time = time.perf_counter()
	result = func(*args)
	end_time = time.perf_counter()
	execution_time = (end_time - start_time) * 1000
	return result, execution_time


class Window(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		uic.loadUi("window.ui", self)
		self.setWindowIcon(QtGui.QIcon('logo.ico'))

		# Инициализация параметров
		self._cell_size = CELL_SIZE
		self.images_sizes = IMAGES_SIZES
		self.is_show_grid = True
		self.current_draw = "line"
		self.current_polygon_index = 0
		self.left_pixels_queue = []
		self.right_pixels_queue = []
		self.texture = None

		# Настройка таймера
		self.draw_timer = QTimer()
		self.draw_timer.setInterval(0)
		self.draw_timer.timeout.connect(self.draw_next_pixel)

		# Данные для испытаний
		self.current_test_line_index = 0
		self.current_test_line_angle_index = 0
		self.current_test_area_index = 0

		# Инициализация текста
		self.countPixelsInCellLabel.setText(f'Количество пикселей в ячейке: {self.cell_size ** 2}')
		self.countDrawPixelsALabel.setText(f'Количество закрашенных пикселей "А": ')
		self.countDrawPixelsBLabel.setText(f'Количество закрашенных пикселей "Б": ')
		self.timeSpentALabel.setText(f'Затраченное время "А" (t): ')
		self.timeSpentBLabel.setText(f'Затраченное время "Б" (t): ')
		self.quanDiffLabel.setText(f'Количественная разность (ΔI): ')
		self.relativeQuanDiffLabel.setText(f'Относительная количественная разность (µ): ')

		# Левое и правое изображения
		self.leftScene = QtWidgets.QGraphicsScene()
		self.leftGraphicsView.setScene(self.leftScene)
		self.leftImage = QImage(self.images_sizes[0], self.images_sizes[1], QImage.Format_ARGB32_Premultiplied)
		self.rightScene = QtWidgets.QGraphicsScene()
		self.rightGraphicsView.setScene(self.rightScene)
		self.rightImage = QImage(self.images_sizes[0], self.images_sizes[1], QImage.Format_ARGB32_Premultiplied)
		self.leftImage.fill(QColor(255, 255, 255))
		self.rightImage.fill(QColor(255, 255, 255))

		# Рисуем сетку
		self.gridImage = QImage(self.images_sizes[0], self.images_sizes[1], QImage.Format_ARGB32_Premultiplied)
		self.draw_grid(QColor(*GRID_COLOR))

		# Обработчики нажатий
		self.drawPushButton.clicked.connect(lambda: start_draw(self))
		self.backPushButton.clicked.connect(lambda: change_polygon(self, "back"))
		self.forwardPushButton.clicked.connect(lambda: change_polygon(self, "forward"))
		self.gridPushButton.clicked.connect(lambda: show_grid(self))
		self.clearPushButton.clicked.connect(lambda: clear_all(self))
		self.upscalePushButton.clicked.connect(lambda: upscale(self))
		self.downscalePushButton.clicked.connect(lambda: downscale(self))
		self.testLinesPushButton.clicked.connect(lambda: calculate_lines_metrics(self))
		self.testAreasPushButton.clicked.connect(lambda: calculate_areas_metrics(self))
		self.diffPushButton.clicked.connect(lambda: show_differences(self))
		self.countDrawPixelsPushButton.clicked.connect(lambda: show_count_draw_pixels(self))
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
		self.drawPushButton.setEnabled(state)
		self.backPushButton.setEnabled(state)
		self.forwardPushButton.setEnabled(state)
		self.gridPushButton.setEnabled(state)
		self.clearPushButton.setEnabled(state)
		self.upscalePushButton.setEnabled(state)
		self.downscalePushButton.setEnabled(state)
		self.testLinesPushButton.setEnabled(state)
		self.testAreasPushButton.setEnabled(state)
		self.diffPushButton.setEnabled(state)
		self.countDrawPixelsPushButton.setEnabled(state)
		self.texturePushButton.setEnabled(state)

	def change_current_draw(self, value):
		"""
		Метод для изменения состояния того, что нужно отрисовать
		"""
		if value == "line":
			self.current_draw = "line"
			self.drawPushButton.setText("Нарисовать отрезки")
		elif value == "area":
			self.current_draw = "area"
			self.drawPushButton.setText("Нарисовать области")

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
		if len(self.left_pixels_queue) > 0:
			x, y, color = self.left_pixels_queue.pop(0)
			self.draw_pixel(self.leftImage, x, y, color)
			self.update_scenes()
			self.change_buttons_state(False)
		if len(self.right_pixels_queue) > 0:
			x, y, color = self.right_pixels_queue.pop(0)
			self.draw_pixel(self.rightImage, x, y, color)
			self.update_scenes()
			self.change_buttons_state(False)

		# Если очереди пустые
		if len(self.left_pixels_queue) == 0 and len(self.right_pixels_queue) == 0:
			self.draw_timer.stop()
			self.change_buttons_state(True)

	def draw_lines(self, points: List[Tuple[int, int]], color: QColor):
		"""
		Метод для рисования отрезков
		"""
		execution_times = [[], []]  # времена выполнения алгоритмов рисования отрезков

		for i in range(0, len(points) - 1):
			x1, y1 = points[i]
			x2, y2 = points[i + 1]
			result_a, execution_time_a = measure_execution_time(line_DDA, self.left_pixels_queue, (x1, y1), (x2, y2), color)
			result_b, execution_time_b = measure_execution_time(line_bresenham, self.right_pixels_queue, (x1, y1), (x2, y2), color)
			execution_times[0].append(execution_time_a)
			execution_times[1].append(execution_time_b)

		execution_times_avg_a = sum(execution_times[0]) / len(execution_times[0])
		execution_times_avg_b = sum(execution_times[1]) / len(execution_times[1])
		self.timeSpentALabel.setText(f'Затраченное время "A" (t): {execution_times_avg_a:.4f}')
		self.timeSpentBLabel.setText(f'Затраченное время "B" (t): {execution_times_avg_b:.4f}')

	def draw_areas(self, p: Tuple[int, int], new_color: QColor):
		"""
		Метод для рисования областей
		"""
		pixel_color_left = get_pixel_color(self.leftImage, p[0], p[1], self.cell_size, self.left_pixels_queue)
		pixel_color_right = get_pixel_color(self.rightImage, p[0], p[1], self.cell_size, self.right_pixels_queue)
		result_a, execution_time_a = measure_execution_time(area_recursive_internal, self, self.leftImage, self.left_pixels_queue, p, new_color, pixel_color_left)
		result_b, execution_time_b = measure_execution_time(area_modified_stack_internal, self, self.rightImage, self.right_pixels_queue, p, new_color, pixel_color_right)
		self.timeSpentALabel.setText(f'Затраченное время "A" (t): {execution_time_a:.4f}')
		self.timeSpentBLabel.setText(f'Затраченное время "B" (t): {execution_time_b:.4f}')

	def update_scenes(self):
		"""
		Метод для обновления всех сцен
		"""
		self.leftScene.clear()
		self.rightScene.clear()

		scene_rect = self.leftScene.sceneRect()
		leftPixmap = QPixmap(scene_rect.size().toSize())
		leftPixmap.convertFromImage(self.leftImage)
		self.leftScene.addPixmap(leftPixmap)

		scene_rect = self.rightScene.sceneRect()
		rightPixmap = QPixmap(scene_rect.size().toSize())
		rightPixmap.convertFromImage(self.rightImage)
		self.rightScene.addPixmap(rightPixmap)

		leftPixmap.convertFromImage(self.gridImage)
		rightPixmap.convertFromImage(self.gridImage)
		self.leftScene.addPixmap(leftPixmap)
		self.rightScene.addPixmap(rightPixmap)

	def draw_grid(self, grid_color: QColor):
		"""
		Метод для рисования сетки
		"""
		width, height = self.leftImage.width(), self.leftImage.height()

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
		new_cell_size = int(self.cell_size * resize_factor)
		if new_cell_size > 40 or new_cell_size < 4:
			return
		self.cell_size = new_cell_size

		new_images_sizes = int(self.images_sizes[0] * resize_factor),  int(self.images_sizes[1] * resize_factor)
		self.images_sizes = new_images_sizes

		# Изменить размеры методом ближайшего соседа
		scaled_left_image = self.leftImage.scaled(
			self.images_sizes[0],
			self.images_sizes[1],
			Qt.IgnoreAspectRatio,
			Qt.FastTransformation
		)
		scaled_right_image = self.rightImage.scaled(
			self.images_sizes[0],
			self.images_sizes[1],
			Qt.IgnoreAspectRatio,
			Qt.FastTransformation
		)
		scaled_grid_image = self.gridImage.scaled(
			self.images_sizes[0],
			self.images_sizes[1],
			Qt.IgnoreAspectRatio,
			Qt.FastTransformation
		)

		self.leftImage.fill(QColor(255, 255, 255))
		self.rightImage.fill(QColor(255, 255, 255))
		self.gridImage.fill(QColor(255, 255, 255))
		self.update_scenes()

		self.leftImage = scaled_left_image
		self.rightImage = scaled_right_image
		self.gridImage = scaled_grid_image
		self.update_scenes()

	def get_count_draw_pixels(self):
		"""
		Метод для получения числа отрисованных пикселей
		"""
		count_draw_pixels_a = 0
		count_draw_pixels_b = 0

		width, height = self.leftImage.width(), self.leftImage.height()

		for x in range(0, width):
			for y in range(0, height):
				left_pixel_color = self.leftImage.pixelColor(x, y)
				right_pixel_color = self.rightImage.pixelColor(x, y)

				if left_pixel_color != QColor(255, 255, 255):
					count_draw_pixels_a += 1
				if right_pixel_color != QColor(255, 255, 255):
					count_draw_pixels_b += 1

		self.countDrawPixelsALabel.setText(f'Количество закрашенных пикселей "А": {count_draw_pixels_a}')
		self.countDrawPixelsBLabel.setText(f'Количество закрашенных пикселей "Б": {count_draw_pixels_b}')

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = Window()
	window.show()
	sys.exit(app.exec_())
