import struct
from typing import Tuple
from src.classes.BmpFile import BmpFile


def change_contrast(color: Tuple[int, int, int], value: float) -> Tuple[int, int, int]:
	red = min(255, max(0, int(color[0] * value)))
	green = min(255, max(0, int(color[1] * value)))
	blue = min(255, max(0, int(color[2] * value)))
	return red, green, blue


def grayscale(bmp_file: BmpFile, contrast_factor: float) -> BmpFile:
	bmp_file_copy = bmp_file.copy()
	bmp_file_copy.biBitCount = 8
	bmp_file_copy.biClrUsed = 256
	bmp_file_copy.pixels_data = bytearray()
	bmp_file_copy.color_table = bytearray()

	for i in range(0, bmp_file_copy.biClrUsed):
		blue = struct.pack("B", i)
		green = struct.pack("B", i)
		red = struct.pack("B", i)
		alpha = struct.pack("B", 0)
		bmp_file_copy.color_table.extend(blue + green + red + alpha)

	bmp_file_copy.bfOffBits = 54 + len(bmp_file_copy.color_table)

	# Вычисление отступа
	padding = (4 - (bmp_file_copy.biWidth * (bmp_file_copy.biBitCount // 8)) % 4) % 4

	for row in range(0, bmp_file.biHeight):
		for col in range(0, bmp_file.biWidth):
			pixel_index = row * bmp_file.biWidth + col
			red, green, blue = bmp_file.get_color(pixel_index)

			# Контрастность
			red, green, blue = change_contrast((red, green, blue), contrast_factor)

			# Полутоновый GRAYSCALE-цвет
			avg_color = (red + green + blue) // 3
			avg_color = min(255, max(0, avg_color))
			bmp_file_copy.pixels_data.extend(struct.pack("B", avg_color))

		# Добавление отступа
		bmp_file_copy.pixels_data.extend(b'\x00' * padding)

	bmp_file_copy.biSizeImage = len(bmp_file_copy.pixels_data)
	bmp_file_copy.bfSize = len(bmp_file_copy.pixels_data) + bmp_file_copy.bfOffBits
	return bmp_file_copy
