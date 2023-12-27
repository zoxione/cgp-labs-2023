import math

import numpy as np
from src.classes import BmpFile
from src.data.constants import IMAGE_VALUE
from src.modules.analyze_image.find_areas import find_areas
from src.modules.analyze_image.negate import negate


def recursive_connected_areas(input_bmp_file: BmpFile):
	pixels = negate(input_bmp_file)
	areas = find_areas(pixels, input_bmp_file.biHeight, input_bmp_file.biWidth, 0)
	result = []

	for area in areas:
		xl, xr, yt, yb = area[1].get_minmax_points(input_bmp_file.biWidth, input_bmp_file.biHeight, 2)
		n = xr - xl
		m = yt - yb
		p_hash = ''

		new_bmp_file = input_bmp_file.copy()
		new_bmp_file.biHeight = m
		new_bmp_file.biWidth = n
		new_bmp_file.biSizeImage = m * n
		size = math.ceil(new_bmp_file.biSizeImage / 8)
		new_bmp_file.pixels_data = bytearray(size)
		pixels_data_index = 0

		new_bmp_file.normalize()

		for row in range(yb, yt):
			binary_str = ''

			for col in range(xl, xr):
				if pixels[col][row] != 0:
					binary_str += '0'
					new_bmp_file.set_value(pixels_data_index, 0)
					pixels_data_index += 1
				else:
					binary_str += '1'
					new_bmp_file.set_value(pixels_data_index, 1)
					pixels_data_index += 1

			if binary_str:
				binary_str = binary_str[::-1]
				hex_value = hex(int(binary_str, 2))
				p_hash += hex_value[2:]

		result.append((new_bmp_file, p_hash))

	return result
