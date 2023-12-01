from typing import List, Tuple
from PyQt5.QtGui import QColor
from src.algorithms.general import is_inside_polygon
from src.classes import UniqueQueue


def area_modified_stack_internal(win, pixel_queue: UniqueQueue, p: Tuple[int, int], new_color: QColor, old_color: QColor, points: List[Tuple[int, int]], layer_index: int):
	"""
	Алгоритм растеризации сплошной области «Б»: модифицированный стековый алгоритм заливки внутренне-определённой 4-х связной области.
	"""
	if new_color == old_color:
		return

	if win.texture:
		new_color = win.get_color_texture(p[0], p[1])
	pixel_queue.append((p[0], p[1], new_color, layer_index))

	stack = [(p[0], p[1])]
	while stack:
		x, y = stack.pop()

		# Проверка и закраска соседних пикселей
		for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
			xt, yt = x + dx, y + dy
			if is_inside_polygon((xt, yt), points):
				pixel_color = win.get_pixel_color(xt, yt, layer_index)
				if win.texture:
					new_color = win.get_color_texture(p[0], p[1])
				if pixel_color == old_color:
					pixel_queue.append((xt, yt, new_color, layer_index))
					stack.append((xt, yt))
