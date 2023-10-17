from PIL import Image
from src.classes.ImageFile import ImageFile
from src.data.constants import BACKGROUND_COLOR

class SingletonMetaclass(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]


class State(metaclass=SingletonMetaclass):
	def __init__(self):
		self.image_file: ImageFile | None = None
		self.image_view: Image | None = None

	def clear(self):
		self.image_file: ImageFile | None = None
		self.image_view: Image | None = None

	def create_image_view(self):
		if self.image_file is not None:
			# Преобразование цветов пикселей
			pixels_colors = []
			for i in range(0, self.image_file.pixels_values_count):
				color_index = self.image_file.pixels_values[i]
				if color_index < 0 or color_index > self.image_file.palette_values_count - 1:
					pixels_colors.append(BACKGROUND_COLOR)
				else:
					pixels_colors.append(self.image_file.palette_values[color_index])

			# Построение вида изображения
			image = Image.new('RGBA', (self.image_file.width, self.image_file.height))
			for y in range(0, self.image_file.height):
				for x in range(0, self.image_file.width):
					pixel_index = y * self.image_file.width + x
					a, r, g, b = pixels_colors[pixel_index]
					image.putpixel((x, y), (a, r, g, b))
			self.image_view = image
