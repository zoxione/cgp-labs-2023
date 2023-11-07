from enum import Enum, unique
from Polygon import Polygon


IMAGES_SIZES = (600, 600)
BACKGROUND_COLOR = (32, 32, 48)
CONTOUR_COLOR = (0, 0, 0)
GRID_COLOR = (220, 220, 220)
GRID_GAP_SIZE = 1
CELL_SIZE = 4
MULTIPLICATION_FACTOR = 10

@unique
class Color(Enum):
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	YELLOW = (255, 255, 0)
	LIGHT_YELLOW = (255, 253, 141)
	PURPLE = (255, 0, 255)
	CYAN = (0, 255, 255)
	DARK_RED = (128, 0, 0)
	DARK_GREEN = (0, 128, 0)
	DARK_BLUE = (0, 0, 128)
	DARK_YELLOW = (128, 128, 0)
	DARK_PURPLE = (128, 0, 128)
	DARK_CYAN = (0, 128, 128)
	ORANGE = (255, 128, 0)
	LIME = (128, 255, 0)
	PINK = (255, 128, 128)
	SALAD = (128, 255, 128)
	INDIGO = (128, 0, 255)
	LILAC = (255, 128, 255)

	@classmethod
	def list(cls):
		return list(map(lambda c: c.name, cls))


POLYGONS = [
	Polygon("closed", Color.YELLOW.value, [(-4, 3), (-2, 5), (-2, 1)]),
	Polygon("closed", Color.ORANGE.value, [(-2, 5.1), (-1.6, 5.3), (-1.6, 0.7), (-2, 0.9)]),
	Polygon("closed", Color.YELLOW.value, [(-1.6, 5), (-0.6, 6.6), (0.4, 6.6), (0.4, 0.8), (0.2, 0.4), (-0.6, 0.4), (-0.8, 0.8), (-1.6, 0.8)]),
	Polygon("closed", Color.ORANGE.value, [(0.4, 5), (3, 4), (4.5, 4.5), (4.5, 1), (3, 1.5), (0.4, 0.8)]),
	Polygon("closed", Color.YELLOW.value, [(4.5, 4), (5.5, 4.5), (5.5, 1), (4.5, 1.5)]),
	Polygon("closed", Color.LIGHT_YELLOW.value, [(5.5, 4), (6.5, 4.5), (6.5, 1), (5.5, 1.5)]),
	Polygon("closed", Color.LIGHT_YELLOW.value, [(3.6, 4.2), (3.9, 4.3), (3.9, 1.2), (3.6, 1.3)]),
	Polygon("closed", Color.BLACK.value, [(-3.8, 3), (-3.5, 3.2), (-3.5, 2.8)])
]

TEST_DATA_LINES = [
	((2, 2), 1, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]),
	((2, 2), 12, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]),
	((2, 2), 23, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]),
	((2, 2), 64, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
]

TEST_DATA_AREAS = [
	(64, [(0.3, 1.0), (0.4, 1.1), (0.5, 1.0)]),
	(128, [(0.4, 0.2), (0.5, 0.5), (0.6, 0.2)]),
	(240, [(0.3, 0.2), (0.6, 0.6), (0.7, 0.2)]),
	(544, [(-0.1, 0.2), (0.3, 0.8), (0.5, 0.6), (0.7, 0.3)]),
	(1936, [(1.5, 2.0), (2.5, 2.5), (2.5, 1.0), (1.5, 1.5)]),
	(3600, [(-2.0, 5.1), (-1.6, 5.3), (-1.6, 0.7), (-2.0, 0.9)]),
	(5456, [(5.5, 4.0), (6.5, 4.5), (6.5, 1.0), (5.5, 1.5)]),
]
