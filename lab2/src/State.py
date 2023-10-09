from typing import List, Tuple


class SingletonMetaclass(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]


class State(metaclass=SingletonMetaclass):
	def __init__(self):
		self.width_image: int = 0
		self.height_image: int = 0
		self.bits_per_pixel: int = 0
		self.palette_values_count: int = 0
		self.palette_values: List[Tuple] = []
		self.pixels_colors: List[int] = []
		self.pixels_values: List[Tuple] = []
		self.pixels_values_count: int = 0

	def clear(self):
		self.width_image: int = 0
		self.height_image: int = 0
		self.bits_per_pixel: int = 0
		self.palette_values_count: int = 0
		self.palette_values: List[Tuple] = []
		self.pixels_colors: List[int] = []
		self.pixels_values: List[Tuple] = []
		self.pixels_values_count: int = 0
