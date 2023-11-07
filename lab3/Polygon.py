from typing import List, Tuple


class Polygon:
	def __init__(self, contour, color, points):
		self.points: List[int] = points
		self.contour: str = contour
		self.color: Tuple[int, int, int] = color

	def copy(self):
		return Polygon(self.contour, self.color, self.points.copy())
