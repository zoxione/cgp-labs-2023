from src.classes import BmpFile
from src.data.constants import IMAGE_VALUE


def morphology_dilation(bmp_file: BmpFile, size: int) -> BmpFile:
	bmp_file_copy = bmp_file.copy()
	size_half = size // 2

	for row in range(0, bmp_file.biHeight):
		for col in range(0, bmp_file.biWidth):
			if size_half <= row < bmp_file.biHeight - size_half and size_half <= col < bmp_file.biWidth - size_half:
				mask_center_index = row * bmp_file.biWidth + col
				pixel_value = bmp_file.get_value(mask_center_index)
				if pixel_value == IMAGE_VALUE:
					# Проход по маске
					for mask_row in range(-size_half, size_half + 1):
						for mask_col in range(-size_half, size_half + 1):
							mask_index = (row + mask_row) * bmp_file.biWidth + (col + mask_col)
							bmp_file_copy.set_value(mask_index, IMAGE_VALUE)

	return bmp_file_copy
