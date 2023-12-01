from typing import Tuple


# Определение кодов регионов
INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8


def compute_code(xl, xr, yt, yb, x, y):
	code = INSIDE

	# Проверка для левого кода
	if x < xl:
		code = code | LEFT
	# Проверка для правого кода
	elif x > xr:
		code = code | RIGHT
	# Проверка для нижнего кода
	if y < yb:
		code = code | BOTTOM
	# Проверка для верхнего кода
	elif y > yt:
		code = code | TOP

	return code


def framing_sutherland_cohen(xl, xr, yt, yb, p1: Tuple[int, int], p2: Tuple[int, int]):
	"""
	Алгоритм определения видимости и отсечения для кадрирования: алгоритм Сазерленда-Коэна
	"""
	code1 = compute_code(xl, xr, yt, yb, p1[0], p1[1])
	code2 = compute_code(xl, xr, yt, yb, p2[0], p2[1])

	while True:
		# Условие полной видимости (оба кода равны 0)
		if code1 == 0 and code2 == 0:
			return p1, p2

		# Условие полной невидимости (оба кода не равны 0 и есть общий бит)
		elif (code1 & code2) != 0:
			return None, None

		else:
			x = 0
			y = 0
			code_out = code1 if code1 != 0 else code2  # Определение, у какой точки код не равен 0

			# Находим пересечение отрезка с границей окна
			if code_out & TOP:
				x = p1[0] + (p2[0] - p1[0]) * (yt - p1[1]) // (p2[1] - p1[1])
				y = yt
			elif code_out & BOTTOM:
				x = p1[0] + (p2[0] - p1[0]) * (yb - p1[1]) // (p2[1] - p1[1])
				y = yb
			elif code_out & LEFT:
				y = p1[1] + (p2[1] - p1[1]) * (xl - p1[0]) // (p2[0] - p1[0])
				x = xl
			elif code_out & RIGHT:
				y = p1[1] + (p2[1] - p1[1]) * (xr - p1[0]) // (p2[0] - p1[0])
				x = xr

			# Обновление координаты p1 или p2 в зависимости от кода
			if code_out == code1:
				p1 = (x, y)
				code1 = compute_code(xl, xr, yt, yb, p1[0], p1[1])
			else:
				p2 = (x, y)
				code2 = compute_code(xl, xr, yt, yb, p2[0], p2[1])
