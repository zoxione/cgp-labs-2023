from typing import Union, Tuple, List
from PyQt5.QtGui import QImage, QColor
from constants import MULTIPLICATION_FACTOR


def multiplication_points(points: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
	"""
	Функция для умножения всех точек
	"""
	new_points = points.copy()
	for i in range(0, len(points)):
		new_points[i] = int(points[i][0] * MULTIPLICATION_FACTOR), int(points[i][1] * MULTIPLICATION_FACTOR)
	return new_points


def find_center(points: List[Tuple[int, int]]) -> Tuple[int, int]:
	"""
	Функция для поиска центра тяжести
	"""
	sum_x = 0
	sum_y = 0

	for i in range(len(points)):
		sum_x += points[i][0]
		sum_y += points[i][1]

	center_x = sum_x // len(points)
	center_y = sum_y // len(points)

	return center_x, center_y


def sign(x: Union[int, float]) -> Union[int, float]:
	"""
	Функция для возврата знака числа
	"""
	if x == 0:
		return 0
	else:
		return x // abs(x)


def line_DDA(pixel_queue: List[Tuple[int, int, QColor]], p1: Tuple[int, int], p2: Tuple[int, int], color: QColor):
	"""
	Алгоритм растеризации отрезка «А»: алгоритм ЦДА (DDA) – алгоритм цифрового дифференциального анализатора
	"""
	# Считаем минимальное количество итераций, необходимое для отрисовки отрезка
	# Выбирая максимум из длины и высоты отрезка, обеспечиваем связность отрезка
	if abs(p2[0] - p1[0]) >= abs(p2[1] - p1[1]):
		length = abs(p2[0] - p1[0])
	else:
		length = abs(p2[1] - p1[1])

	# Особый случай, когда на экране закрашивается ровно один пиксель
	if length == 0:
		pixel_queue.append((p1[0], p1[1], color))
		return

	# Вычисляем приращения на каждом шаге по осям абсцисс и ординат
	dX = (p2[0] - p1[0]) / length
	dY = (p2[1] - p1[1]) / length

	# Начальные значения
	x = p1[0]
	y = p1[1]

	# Основной цикл
	index = 0
	while index <= length:
		pixel_queue.append((round(x), round(y), color))
		x += dX
		y += dY
		index += 1


def line_bresenham(pixel_queue: List[Tuple[int, int, QColor]], p1: Tuple[int, int], p2: Tuple[int, int], color: QColor):
	"""
	Алгоритм растеризации отрезка «Б»: алгоритм Брезенхема для отрезка
	"""
	# Особый случай, когда на экране закрашивается ровно один пиксель
	if p1 == p2:
		pixel_queue.append((p1[0], p1[1], color))
		return

	# Начальные значения
	x = p1[0]
	y = p1[1]
	dX = abs(p2[0] - p1[0])
	dY = abs(p2[1] - p1[1])
	s1 = sign(p2[0] - p1[0])
	s2 = sign(p2[1] - p1[1])

	# Обмен значений dx и dy в зависимости от
	# углового коэффициента наклона отрезка
	if dY > dX:
		dX, dY = dY, dX
		isChange = True
	else:
		isChange = False

	# Инициализация ошибки e
	# с поправкой на половину пикселя
	e = 2 * dY - dX

	# Основной цикл
	for i in range(0, dX):
		pixel_queue.append((x, y, color))

		while e >= 0:
			if isChange:
				x += s1
			else:
				y += s2
			e = e - 2 * dX

		if isChange:
			y += s2
		else:
			x += s1
		e = e + 2 * dY


def get_pixel_color(image: QImage, x: int, y: int, cell_size: int, pixel_queue: List[Tuple[int, int, QColor]]) -> QColor:
	"""
	Функция для получения цвета пикселя
	"""
	for i in range(0, len(pixel_queue)):
		p_x, p_y, p_color = pixel_queue[i]
		if x == p_x and y == p_y:
			return p_color

	# Корректировка координат, чтобы пиксель соответствовал ячейке сетки
	image_x = image.width() // 2 + (x * cell_size)
	image_y = image.height() // 2 + (-y * cell_size)

	pixel_color = image.pixelColor(image_x, image_y)
	return pixel_color


def area_recursive_internal(win, image: QImage, pixel_queue: List[Tuple[int, int, QColor]], p: Tuple[int, int], new_color: QColor, old_color: QColor):
	"""
	Алгоритм растеризации сплошной области «А»: рекурсивный алгоритм заливки внутренне-определённой 4-х связной области
	"""
	stack = [(p[0], p[1])]

	while stack:
		x, y = stack.pop()
		if win.texture:
			new_color = win.texture.pixelColor(x, y)
		pixel_queue.append((x, y, new_color))

		# Проверка и закраска соседних пикселей
		for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
			xt, yt = x + dx, y + dy
			pixel_color = get_pixel_color(image, xt, yt, win.cell_size, pixel_queue)
			if pixel_color == old_color:
				stack.append((xt, yt))


def area_modified_stack_internal(win, image: QImage, pixel_queue: List[Tuple[int, int, QColor]], p: Tuple[int, int], new_color: QColor, old_color: QColor):
	"""
	Алгоритм растеризации сплошной области «Б»: модифицированный стековый алгоритм заливки внутренне-определённой 4-х связной области.
	"""
	if win.texture:
		new_color = win.texture.pixelColor(p[0], p[1])
	pixel_queue.append((p[0], p[1], new_color))

	stack = [(p[0], p[1])]
	while stack:
		x, y = stack.pop()

		# Проверка и закраска соседних пикселей
		for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
			xt, yt = x + dx, y + dy
			pixel_color = get_pixel_color(image, xt, yt, win.cell_size, pixel_queue)
			if win.texture:
				new_color = win.texture.pixelColor(xt, yt)
			if pixel_color == old_color:
				pixel_queue.append((xt, yt, new_color))
				stack.append((xt, yt))
