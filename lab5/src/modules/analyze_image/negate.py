import numpy as np
from src.classes import BmpFile
from src.data.constants import IMAGE_VALUE


def negate(bmp_file: BmpFile) -> np.ndarray:
	pixels = np.zeros((bmp_file.biWidth, bmp_file.biHeight), dtype=int)

	for row in range(0, bmp_file.biHeight):
		for col in range(0, bmp_file.biWidth):
			pixel_index = row * bmp_file.biWidth + col
			pixel_value = bmp_file.get_value(pixel_index)
			if pixel_value == IMAGE_VALUE:
				pixels[col][row] = -1
			else:
				pixels[col][row] = 0

	return pixels
