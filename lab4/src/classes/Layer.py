from typing import List, Tuple
from src.classes.Polygon import Polygon


class Layer:
	def __init__(self, name, polygons):
		self.name: str = name
		self.polygons: List[Polygon] = polygons
		self.overlap_areas: List[Tuple[Polygon, int]] = []
		self.overlap_lines: List[Tuple[Polygon, int]] = []

