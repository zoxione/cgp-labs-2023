from enum import Enum, unique
from src.classes.Layer import Layer
from src.classes.Polygon import Polygon


IMAGES_SIZES = (800, 800)
FRAME_SIZES = (250, 250)
BACKGROUND_COLOR = (225, 225, 225)
TRANSPARENT_COLOR = (155, 0, 255)
FRAME_COLOR = (255, 128, 128)
OVERLAP_COLOR = (255, 0, 0)
GRID_COLOR = (220, 220, 220)
GRID_GAP_SIZE = 1
CELL_SIZE = 2
MULTIPLICATION_FACTOR = 1


@unique
class Color(Enum):
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	YELLOW = (255, 255, 0)
	PURPLE = (255, 0, 255)
	CYAN = (0, 255, 255)
	ORANGE = (230, 116, 43)
	LIME = (128, 255, 0)
	PINK = (255, 128, 128)
	SALAD = (128, 255, 128)
	INDIGO = (128, 0, 255)
	LILAC = (255, 128, 255)
	BROWN = (102, 51, 0)

	@classmethod
	def list(cls):
		return list(map(lambda c: c.name, cls))


@unique
class Mode(Enum):
	ALPHA = 1
	BRAVO = 2
	CHARLIE = 3


LAYERS = [
	Layer("Кадр", [
		Polygon(Color.WHITE.value, "solid", FRAME_COLOR, [
			(-(FRAME_SIZES[0] // 2), -(FRAME_SIZES[1] // 2)),
			(-(FRAME_SIZES[0] // 2), (FRAME_SIZES[1] // 2)),
			((FRAME_SIZES[0] // 2), (FRAME_SIZES[1] // 2)),
			((FRAME_SIZES[0] // 2), -(FRAME_SIZES[1] // 2))
		])
	]),
	Layer("Зрачки, внутри ушек, внутри лапок", [
		# Зрачки
		Polygon(Color.BLACK.value, "solid", Color.BLACK.value, [(-20, 72), (-12, 70), (-20, 68)]),
		Polygon(Color.BLACK.value, "solid", Color.BLACK.value, [(12, 70), (20, 72), (20, 68)]),
		# Внутри ушек
		Polygon(Color.WHITE.value, "solid", Color.BLACK.value, [(-30, 120), (-20, 105), (-40, 105)]),
		Polygon(Color.WHITE.value, "solid", Color.BLACK.value, [(30, 120), (40, 105), (20, 105)]),
		# Внутри лапок
		Polygon(Color.WHITE.value, "solid", Color.BLACK.value, [(-50, -25), (-39, -40), (-61, -40)]),
		Polygon(Color.WHITE.value, "solid", Color.BLACK.value, [(50, -25), (61, -40), (39, -40)]),
	]),
	Layer("Глаза, ушки, лапки, носик", [
		# Глаза
		Polygon(Color.WHITE.value, "solid", Color.BLACK.value, [(-25, 76), (-6, 70), (-25, 64)]),
		Polygon(Color.WHITE.value, "solid", Color.BLACK.value, [(6, 70), (25, 76), (25, 64)]),
		# Ушки
		Polygon(Color.ORANGE.value, "solid", Color.BLACK.value, [(-30, 130), (-10, 100), (-50, 100)]),
		Polygon(Color.ORANGE.value, "solid", Color.BLACK.value, [(30, 130), (50, 100), (10, 100)]),
		# Лапки
		Polygon(Color.ORANGE.value, "solid", Color.BLACK.value, [(-50, -10), (-34, -40), (-66, -40)]),
		Polygon(Color.ORANGE.value, "solid", Color.BLACK.value, [(50, -10), (66, -40), (34, -40)]),
		# Носик
		Polygon(Color.BROWN.value, "solid", Color.BLACK.value, [(-10, 36), (10, 36), (0, 20)])
	]),
	Layer("Голова", [
		# Голова
		Polygon(Color.ORANGE.value, "solid", Color.BLACK.value, [(-50, 100), (50, 100), (0, 20)]),
	]),
	Layer("Первый воротник", [
		# Первый воротник
		Polygon(Color.WHITE.value, "solid", Color.BLACK.value, [(-12, 28), (12, 28), (0, 0)]),
	]),
	Layer("Второй воротник", [
		# Второй воротник
		Polygon(Color.WHITE.value, "solid", Color.BLACK.value, [(-18, 25), (18, 25), (0, -15)]),
	]),
	Layer("Внутри брюшка", [
		# Внутри брюшка
		Polygon(Color.WHITE.value, "solid", Color.BLACK.value, [(0, 48), (34, -40), (-34, -40)]),
	]),
	Layer("Брюшко", [
		# Брюшко
		Polygon(Color.ORANGE.value, "solid", Color.BLACK.value, [(0, 65), (60, -40), (-60, -40)]),
	]),
	Layer("Хвост", [
		# Верхняя часть хвоста
		Polygon(Color.WHITE.value, "solid", Color.BLACK.value, [(40, 40), (57, 5), (23, 5)]),
		# Нижняя часть хвоста
		Polygon(Color.ORANGE.value, "solid", Color.BLACK.value, [(23, 5), (57, 5), (40, -30)]),
	]),
]
