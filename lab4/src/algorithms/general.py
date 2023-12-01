from typing import Tuple

from src.data.constants import Color


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
