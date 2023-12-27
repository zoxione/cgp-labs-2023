import sys

from src.classes import Polygon
from src.modules.analyze_image.search import search


def find_areas(pixels, max_rows: int, max_cols: int, label: int):
	areas = []

	for row in range(0, max_rows):
		for col in range(0, max_cols):
			if pixels[col][row] == -1:
				label = label + 1
				area = Polygon((0, 0, 0), 'closed', (255, 255, 255), [])
				search(pixels, max_cols, max_rows, label, row, col, area)
				areas.append((label, area))

	return areas
