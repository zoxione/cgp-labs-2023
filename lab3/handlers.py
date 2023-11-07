import math
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QFileDialog
from algorithms import find_center, multiplication_points
from constants import POLYGONS, GRID_COLOR, TEST_DATA_LINES, TEST_DATA_AREAS


def start_draw(win):
	"""
	Обработчик нажатия на кнопку для рисования текущего полигона
	"""
	win.draw_timer.start()
	now_polygon = POLYGONS[win.current_polygon_index].copy()
	now_polygon.points = multiplication_points(now_polygon.points)

	if win.current_draw == "line":
		now_polygon.points.append(now_polygon.points[0])  # чтобы замкнуть полигон
		win.draw_lines(now_polygon.points, QColor(*now_polygon.color))
		win.change_current_draw("area")
	elif win.current_draw == "area":
		center = find_center(now_polygon.points)
		win.draw_areas(center, QColor(*now_polygon.color))
		win.change_current_draw("line")


def change_polygon(win, mode: str):
	"""
	Обработчик нажатия на кнопку для изменения номера полигона
	"""
	if mode == "back":
		win.current_polygon_index = (win.current_polygon_index - 1) % len(POLYGONS)
	if mode == "forward":
		win.current_polygon_index = (win.current_polygon_index + 1) % len(POLYGONS)
	win.currentPolygonLabel.setText(f"Текущий полигон: {win.current_polygon_index + 1}")
	win.change_current_draw("line")


def show_grid(win):
	"""
	Обработчик нажатия на кнопку для отображения/скрытия сетки
	"""
	win.is_show_grid = not win.is_show_grid
	if win.is_show_grid:
		grid_color = QColor(*GRID_COLOR)
	else:
		grid_color = QColor(255, 255, 255)

	win.draw_grid(grid_color)


def clear_all(win):
	"""
	Обработчик нажатия на кнопку для очистки изображений
	"""
	win.leftImage.fill(QColor(255, 255, 255))
	win.rightImage.fill(QColor(255, 255, 255))
	win.update_scenes()


def upscale(win):
	"""
	Обработчик нажатия на кнопку для увеличения изображений
	"""
	win.resize_images(2)


def downscale(win):
	"""
	Обработчик нажатия на кнопку для уменьшения изображений
	"""
	win.resize_images(1/2)


def show_differences(win):
	"""
	Обработчик нажатия на кнопку для отображения разности изображений
	"""
	leftImage = win.leftImage
	rightImage = win.rightImage
	count_diff_pixels = 0

	if leftImage.size() != rightImage.size():
		return
	width, height = leftImage.width(), leftImage.height()

	for x in range(0, width):
		for y in range(0, height):
			left_pixel_color = leftImage.pixelColor(x, y)
			right_pixel_color = rightImage.pixelColor(x, y)

			if left_pixel_color != right_pixel_color:
				count_diff_pixels += 1
				leftImage.setPixelColor(x, y, QColor(255, 0, 0))

	win.quanDiffLabel.setText(f'Количественная разность (ΔI): {count_diff_pixels}')
	relative_count_diff_pixels = count_diff_pixels / (width * height)
	win.relativeQuanDiffLabel.setText(f'Относительная количественная разность (µ): {relative_count_diff_pixels:.4%}')

	# Обновите сцены для отображения изменений
	win.update_scenes()


def show_count_draw_pixels(win):
	"""
	Обработчик нажатия на кнопку для отображения числа отрисованных пикселей
	"""
	win.get_count_draw_pixels()


def add_texture(win):
	"""
	Обработчик нажатия на кнопку для добавления текстуры
	"""
	file = QFileDialog.getOpenFileName(win, "Open File", "textures/", "All Files (*);;PNG Files (*.png);;Jpg Files (*.jpg)")
	pixmap = QPixmap(file[0])
	win.texture = pixmap.toImage()


def calculate_lines_metrics(win):
	"""
	Обработчик нажатия на кнопку для начала испытаний с отрезками
	"""
	win.draw_timer.start()

	(x1, y1), length, angles = TEST_DATA_LINES[win.current_test_line_index]
	angle = angles[win.current_test_line_angle_index]
	x2 = int(x1 + length * math.cos(math.radians(angle)))
	y2 = int(y1 + length * math.sin(math.radians(angle)))

	clear_all(win)
	win.draw_lines([(x1, y1), (x2, y2)], QColor(0, 0, 0))

	if win.current_test_line_angle_index == len(angles) - 1:
		win.current_test_line_index = (win.current_test_line_index + 1) % len(TEST_DATA_LINES)
	win.current_test_line_angle_index = (win.current_test_line_angle_index + 1) % len(angles)

	win.testLinesPushButton.setText(f'Начать испытание {win.current_test_line_index + 1} ({angles[win.current_test_line_angle_index]}°)')


def calculate_areas_metrics(win):
	"""
	Обработчик нажатия на кнопку для начала испытаний с областями
	"""
	win.draw_timer.start()

	s, points = TEST_DATA_AREAS[win.current_test_area_index]
	points = multiplication_points(points)

	if win.current_draw == "line":
		clear_all(win)
		points.append(points[0])  # чтобы замкнуть полигон
		win.draw_lines(points, QColor(0, 0, 0))
		if s >= 128:
			win.change_current_draw("area")
		else:
			win.current_test_area_index = (win.current_test_area_index + 1) % len(TEST_DATA_AREAS)
			win.testAreasPushButton.setText(f'Начать испытание {win.current_test_area_index + 1} ({TEST_DATA_AREAS[win.current_test_area_index][0]})')
	elif win.current_draw == "area":
		center = find_center(points)
		win.draw_areas(center, QColor(0, 0, 0))
		win.change_current_draw("line")
		win.current_test_area_index = (win.current_test_area_index + 1) % len(TEST_DATA_AREAS)
		win.testAreasPushButton.setText(f'Начать испытание {win.current_test_area_index + 1} ({TEST_DATA_AREAS[win.current_test_area_index][0]})')
