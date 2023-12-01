import math
from typing import List, Tuple


class Polygon:
	def __init__(self, fill_color, contour, contour_color, points):
		self.fill_color: Tuple[int, int, int] = fill_color
		self.contour: str = contour
		self.contour_color: Tuple[int, int, int] = contour_color
		self.points: List[Tuple[int, int]] = points

	def copy(self):
		return Polygon(self.fill_color, self.contour, self.contour_color, self.points.copy())

	def __eq__(self, other):
		if not isinstance(other, Polygon):
			return False

		if self.fill_color != other.fill_color or self.contour != other.contour or self.contour_color != other.contour_color:
			return False

		if len(self.points) != len(other.points):
			return False

		self.normalize()
		other.normalize()

		for i in range(0, len(self.points)):
			if self.points[i] != other.points[i]:
				return False

		return True

	def normalize(self):
		# Удаление повторяющихся точек
		self.points = list(set(self.points))

		# Сортировка точек по углу относительно центра масс
		centroid = [sum(x) / len(self.points) for x in zip(*self.points)]
		self.points.sort(key=lambda point: -math.atan2(point[1] - centroid[1], point[0] - centroid[0]))

		# Добавление зацикливания
		self.points.append(self.points[0])

	def get_center(self):
		self.normalize()
		sum_x = sum(item[0] for item in self.points)
		sum_y = sum(item[1] for item in self.points)
		center_x = sum_x // len(self.points)
		center_y = sum_y // len(self.points)
		return center_x, center_y

	def get_minmax_points(self):
		xl = min(self.points, key=lambda item: item[0])[0]
		xr = max(self.points, key=lambda item: item[0])[0]
		yt = max(self.points, key=lambda item: item[1])[1]
		yb = min(self.points, key=lambda item: item[1])[1]
		return xl, xr, yt, yb
