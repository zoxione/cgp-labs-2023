import struct
from src.classes import BmpFile


def binarization(bmp_file: BmpFile, threshold: int) -> BmpFile:
	bmp_file_copy = bmp_file.copy()
	bmp_file_copy.biBitCount = 1
	bmp_file_copy.biClrUsed = 2
	bmp_file_copy.pixels_data = bytearray()
	bmp_file_copy.color_table = bytearray()

	# Цвета
	black_color = struct.pack("BBBB", 0, 0, 0, 0)
	bmp_file_copy.color_table.extend(black_color)
	white_color = struct.pack("BBBB", 255, 255, 255, 0)
	bmp_file_copy.color_table.extend(white_color)

	bmp_file_copy.bfOffBits = 54 + len(bmp_file_copy.color_table)

	bit_buffer = 0  # Инициализация буфера для хранения битов
	bit_count = 0   # Счетчик битов

	# Вычисление отступа для каждой строки
	bytes_per_row = (bmp_file_copy.biWidth + 7) // 8  # Количество байтов на строку, округленное вверх до целого числа байтов
	padding = 4 - (bytes_per_row % 4)  # Вычисление отступа
	if padding == 4:  # Если отступ равен 4, то устанавливаем его обратно в 0
		padding = 0

	for row in range(0, bmp_file.biHeight):
		for col in range(0, bmp_file.biWidth):
			pixel_index = row * bmp_file.biWidth + col
			pixel_value = bmp_file.get_value(pixel_index)

			# Устанавливаем бит в буфере в зависимости от порога
			if pixel_value > threshold:
				bit_buffer |= (1 << (7 - bit_count))
			bit_count += 1

			# Если набралось 8 битов, добавляем байт в pixels_data
			if bit_count == 8:
				bmp_file_copy.pixels_data.extend(struct.pack("B", bit_buffer))
				bit_buffer = 0
				bit_count = 0

		# Обработка оставшихся битов, если есть
		if bit_count > 0:
			bmp_file_copy.pixels_data.extend(struct.pack("B", bit_buffer))
			bit_buffer = 0
			bit_count = 0

		# Добавляем отступ после каждой строки изображения
		bmp_file_copy.pixels_data.extend(b'\x00' * padding)

	bmp_file_copy.biSizeImage = len(bmp_file_copy.pixels_data)
	bmp_file_copy.bfSize = len(bmp_file_copy.pixels_data) + bmp_file_copy.bfOffBits
	return bmp_file_copy
