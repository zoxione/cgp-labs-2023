import math
import struct
import numpy as np
from PyQt5.QtGui import QImage, QColor
from src.algorithms.general import greater_multiple_of_4
from src.data.constants import IMAGE_VALUE


class BmpFile:
	def __init__(self, path=None):
		if path is not None:
			self.name = path.split("/")[-1]
			self.read_file(path)
		else:
			self.name = ''
			self.bfType = b''
			self.bfSize = 0
			self.bfReserved1 = 0
			self.bfReserved2 = 0
			self.bfOffBits = 0
			self.biSize = 0
			self.biWidth = 0
			self.biHeight = 0
			self.biPlanes = 0
			self.biBitCount = 0
			self.biCompression = 0
			self.biSizeImage = 0
			self.biXPelsPerMeter = 0
			self.biYPelsPerMeter = 0
			self.biClrUsed = 0
			self.biClrImportant = 0
			self.color_table = bytearray()
			self.pixels_data = bytearray()

	def copy(self):
		copied_bmp_file = BmpFile()
		copied_bmp_file.name = self.name
		copied_bmp_file.bfType = self.bfType
		copied_bmp_file.bfSize = self.bfSize
		copied_bmp_file.bfReserved1 = self.bfReserved1
		copied_bmp_file.bfReserved2 = self.bfReserved2
		copied_bmp_file.bfOffBits = self.bfOffBits
		copied_bmp_file.biSize = self.biSize
		copied_bmp_file.biWidth = self.biWidth
		copied_bmp_file.biHeight = self.biHeight
		copied_bmp_file.biPlanes = self.biPlanes
		copied_bmp_file.biBitCount = self.biBitCount
		copied_bmp_file.biCompression = self.biCompression
		copied_bmp_file.biSizeImage = self.biSizeImage
		copied_bmp_file.biXPelsPerMeter = self.biXPelsPerMeter
		copied_bmp_file.biYPelsPerMeter = self.biYPelsPerMeter
		copied_bmp_file.biClrUsed = self.biClrUsed
		copied_bmp_file.biClrImportant = self.biClrImportant
		copied_bmp_file.color_table = self.color_table.copy()
		copied_bmp_file.pixels_data = self.pixels_data.copy()
		return copied_bmp_file

	def read_file(self, path):
		with open(path, 'rb') as file:
			# BITMAPFILEHEADER
			self.bfType = file.read(2)
			self.bfSize = struct.unpack('I', file.read(4))[0]
			self.bfReserved1 = struct.unpack('H', file.read(2))[0]
			self.bfReserved2 = struct.unpack('H', file.read(2))[0]
			self.bfOffBits = struct.unpack('I', file.read(4))[0]

			# BITMAPINFO
			self.biSize = struct.unpack('I', file.read(4))[0]
			self.biWidth = struct.unpack('I', file.read(4))[0]
			self.biHeight = struct.unpack('I', file.read(4))[0]
			self.biPlanes = struct.unpack('H', file.read(2))[0]
			self.biBitCount = struct.unpack('H', file.read(2))[0]
			self.biCompression = struct.unpack('I', file.read(4))[0]
			self.biSizeImage = struct.unpack('I', file.read(4))[0]
			self.biXPelsPerMeter = struct.unpack('I', file.read(4))[0]
			self.biYPelsPerMeter = struct.unpack('I', file.read(4))[0]
			self.biClrUsed = struct.unpack('I', file.read(4))[0]
			self.biClrImportant = struct.unpack('I', file.read(4))[0]

			# Таблица цветов
			self.color_table = bytearray(file.read(self.biClrUsed * 4))

			# Пиксельные данные
			file.seek(self.bfOffBits)
			self.pixels_data = bytearray(file.read())

	def show(self):
		print('Имя: ', self.name)

		# BITMAPFILEHEADER
		print('Тип: ', self.bfType)
		print('Размер: ', self.bfSize)
		print('Зарезервировано 1: ', self.bfReserved1)
		print('Зарезервировано 2: ', self.bfReserved2)
		print('Смещение пикселей: ', self.bfOffBits)

		# BITMAPINFO
		print('Размер заголовка BITMAPINFO: ', self.biSize)
		print('Ширина: ', self.biWidth)
		print('Высота: ', self.biHeight)
		print('Цветные плоскости: ', self.biPlanes)
		print('Количество бит на пиксель: ', self.biBitCount)
		print('Метод сжатия: ', self.biCompression)
		print('Размер пиксельных данных в байтах: ', self.biSizeImage)
		print('Количество пикселей на метр по горизонтали: ', self.biXPelsPerMeter)
		print('Количество пикселей на метр по вертикали: ', self.biYPelsPerMeter)
		print('Размер таблицы цветов в ячейках: ', self.biClrUsed)
		print('Количество ячеек таблицы цветов: ', self.biClrImportant)

	def calculate_padding(self, pixel_index):
		total_padding = 0

		if self.biBitCount == 24:
			padding = ((4 - (self.biWidth * (self.biBitCount // 8)) % 4) & 3)
			rows_before_index = pixel_index // self.biWidth
			total_padding = rows_before_index * padding
		elif self.biBitCount == 8:
			padding = ((4 - (self.biWidth * (self.biBitCount // 8)) % 4) & 3)
			rows_before_index = pixel_index // self.biWidth
			total_padding = rows_before_index * padding
		elif self.biBitCount == 1:
			bytes_per_row = math.ceil(self.biWidth / 8)
			padded_bytes_per_row = greater_multiple_of_4(bytes_per_row)
			padding = padded_bytes_per_row * 8 - self.biWidth
			rows_before_index = pixel_index // self.biWidth
			total_padding = rows_before_index * padding

		return total_padding

	def calculate_hash(self):
		p_hash = ''

		for row in range(0, self.biHeight):
			binary_str = ''
			for col in range(0, self.biWidth):
				pixel_index = row * self.biWidth + col
				pixel_value = self.get_value(pixel_index)
				if pixel_value == IMAGE_VALUE:
					binary_str += '0'
				else:
					binary_str += '1'
			binary_str = binary_str[::-1]
			hex_value = hex(int(binary_str, 2))
			p_hash += hex_value[2:]

		return p_hash

	def get_value(self, pixel_index):
		if self.biBitCount == 24:
			byte_index = pixel_index * 3 + self.calculate_padding(pixel_index)
			blue = self.pixels_data[byte_index]
			green = self.pixels_data[byte_index + 1]
			red = self.pixels_data[byte_index + 2]
			return red, green, blue
		elif self.biBitCount == 8:
			pixel_index += self.calculate_padding(pixel_index)
			avg = self.pixels_data[pixel_index]
			return avg
		elif self.biBitCount == 1:
			total_padding_bits = self.calculate_padding(pixel_index)

			byte_index = (pixel_index + total_padding_bits) // 8
			bit_offset = 7 - ((pixel_index + total_padding_bits) % 8)
			bit = (self.pixels_data[byte_index] >> bit_offset) & 1
			return bit
		else:
			raise ValueError(f'Неподдерживаемое количество бит: {self.biBitCount}')

	def set_value(self, pixel_index, value):
		if self.biBitCount == 24:
			byte_index = pixel_index * 3 + self.calculate_padding(pixel_index)
			self.pixels_data[byte_index] = value[0]
			self.pixels_data[byte_index + 1] = value[1]
			self.pixels_data[byte_index + 2] = value[2]
		elif self.biBitCount == 8:
			pixel_index += self.calculate_padding(pixel_index)
			self.pixels_data[pixel_index] = value
		elif self.biBitCount == 1:
			total_padding_bits = self.calculate_padding(pixel_index)

			byte_index = (pixel_index + total_padding_bits) // 8
			bit_offset = 7 - ((pixel_index + total_padding_bits) % 8)
			self.pixels_data[byte_index] &= ~(1 << bit_offset)      # Очищаем бит
			self.pixels_data[byte_index] |= value << bit_offset     # Записываем бит
		else:
			raise ValueError(f'Неподдерживаемое количество бит: {self.biBitCount}')

	def get_color(self, pixel_index):
		if self.biBitCount == 24:
			byte_index = pixel_index * 3 + self.calculate_padding(pixel_index)
			blue = self.pixels_data[byte_index]
			green = self.pixels_data[byte_index + 1]
			red = self.pixels_data[byte_index + 2]
			return red, green, blue
		elif self.biBitCount == 8:
			pixel_index += self.calculate_padding(pixel_index)
			pixel_value = self.pixels_data[pixel_index]
			pixel_value *= 4
			red = self.color_table[pixel_value]
			green = self.color_table[pixel_value + 1]
			blue = self.color_table[pixel_value + 2]
			alpha = self.color_table[pixel_value + 3]
			return red, green, blue
		elif self.biBitCount == 1:
			total_padding_bits = self.calculate_padding(pixel_index)
			byte_index = (pixel_index + total_padding_bits) // 8
			bit_offset = 7 - ((pixel_index + total_padding_bits) % 8)
			bit = (self.pixels_data[byte_index] >> bit_offset) & 1

			bit *= 4
			red = self.color_table[bit]
			green = self.color_table[bit + 1]
			blue = self.color_table[bit + 2]
			alpha = self.color_table[bit + 3]
			return red, green, blue
		else:
			raise ValueError(f'Неподдерживаемое количество бит: {self.biBitCount}')

	def to_image(self):
		image = QImage(self.biWidth, self.biHeight, QImage.Format_RGB888)
		for row in range(self.biHeight):
			for col in range(self.biWidth):
				pixel_index = (self.biHeight - row - 1) * self.biWidth + col
				pixel_color = self.get_color(pixel_index)
				image.setPixelColor(col, row, QColor(*pixel_color))
		return image

	def save_file(self, path):
		with open(path, 'wb') as file:
			# Запись BITMAPFILEHEADER
			file.write(self.bfType)
			file.write(struct.pack('I', self.bfSize))
			file.write(struct.pack('H', self.bfReserved1))
			file.write(struct.pack('H', self.bfReserved2))
			file.write(struct.pack('I', self.bfOffBits))

			# Запись BITMAPINFO
			file.write(struct.pack('I', self.biSize))
			file.write(struct.pack('I', self.biWidth))
			file.write(struct.pack('I', self.biHeight))
			file.write(struct.pack('H', self.biPlanes))
			file.write(struct.pack('H', self.biBitCount))
			file.write(struct.pack('I', self.biCompression))
			file.write(struct.pack('I', self.biSizeImage))
			file.write(struct.pack('I', self.biXPelsPerMeter))
			file.write(struct.pack('I', self.biYPelsPerMeter))
			file.write(struct.pack('I', self.biClrUsed))
			file.write(struct.pack('I', self.biClrImportant))

			# Запись таблицы цветов (если есть)
			file.write(self.color_table)

			# Запись пиксельных данных
			file.write(self.pixels_data)

	def normalize(self):
		aligned_pixels_data = bytearray()

		if self.biBitCount == 1:
			bytes_per_row = math.ceil((self.biWidth * self.biBitCount) / 8)
			padding = 4 - (bytes_per_row % 4)
			if padding == 4:
				padding = 0

			for i in range(0, self.biHeight):
				start = i * bytes_per_row
				end = start + bytes_per_row
				aligned_pixels_data.extend(self.pixels_data[start:end])
				if end > len(self.pixels_data):
					aligned_pixels_data.extend(b'\x00' * (end - len(self.pixels_data)))
				aligned_pixels_data.extend(b'\x00' * padding)
		else:
			raise ValueError(f'Неподдерживаемое количество бит: {self.biBitCount}')

		self.pixels_data = aligned_pixels_data
