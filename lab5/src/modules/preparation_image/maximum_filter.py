import struct
from src.classes.BmpFile import BmpFile


def maximum_filter(bmp_file: BmpFile, size: int) -> BmpFile:
	bmp_file_copy = bmp_file.copy()
	bmp_file_copy.pixels_data = bytearray()
	size_half = size // 2

	# Вычисление отступа
	padding = (4 - (bmp_file_copy.biWidth * (bmp_file_copy.biBitCount // 8)) % 4) % 4

	for row in range(0, bmp_file.biHeight):
		for col in range(0, bmp_file.biWidth):
			if size_half <= row < bmp_file.biHeight - size_half and size_half <= col < bmp_file.biWidth - size_half:
				# Проход по фильтру
				max_value = 0
				for filter_row in range(-size_half, size_half + 1):
					for filter_col in range(-size_half, size_half + 1):
						filter_index = (row + filter_row) * bmp_file.biWidth + (col + filter_col)
						filter_value = bmp_file.get_value(filter_index)
						max_value = max(max_value, filter_value)
				bmp_file_copy.pixels_data.extend(struct.pack("B", max_value))
			else:
				# Если это граница
				pixel_index = row * bmp_file.biWidth + col
				pixel_value = bmp_file.get_value(pixel_index)
				bmp_file_copy.pixels_data.extend(struct.pack("B", pixel_value))

		# Добавление отступа после каждой строки изображения
		bmp_file_copy.pixels_data.extend(b'\x00' * padding)

	return bmp_file_copy
