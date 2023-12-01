from typing import Union, Tuple
from PyQt5.QtGui import QColor
from src.classes import UniqueQueue


def sign(x: Union[int, float]) -> Union[int, float]:
	"""
	Функция для возврата знака числа
	"""
	if x == 0:
		return 0
	else:
		return x // abs(x)


def line_bresenham(pixel_queue: UniqueQueue, p1: Tuple[int, int], p2: Tuple[int, int], color: QColor, layer_index: int):
	"""
	Алгоритм растеризации отрезка «Б»: алгоритм Брезенхема для отрезка
	"""
	# Особый случай, когда на экране закрашивается ровно один пиксель
	if p1 == p2:
		pixel_queue.append((p1[0], p1[1], color, layer_index))
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
		pixel_queue.append((x, y, color, layer_index))

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
