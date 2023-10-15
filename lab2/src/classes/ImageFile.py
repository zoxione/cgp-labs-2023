from typing import List, Tuple


class ImageFile:
	def __init__(self):
		self.width: int = 0
		self.height: int = 0
		self.bits_per_pixel: int = 0
		self.palette_values_count: int = 0
		self.palette_values: List[Tuple] = []
		self.pixels_values_count: int = 0
		self.pixels_values: List[int] = []
