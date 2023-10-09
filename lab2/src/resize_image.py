import math
from colorama import Fore
from colorama import Style
from State import State
from constants import BACKGROUND_COLOR


def reshape(array, height, width):
	"""
	Функция для изменения формы массива
	"""
	matrix = []
	for i in range(height):
		row = []
		for j in range(width):
			pixel_index = i * width + j
			row.append(array[pixel_index])
		matrix.append(row)
	return matrix


def resize_image():
	"""
	Функция для увеличения изображения
	"""
	state = State()

	if state.width_image == 0 or state.height_image == 0:
		print(f'{Fore.RED}Нет прочитанного bin-файла!\n{Style.RESET_ALL}')
		return

	resize_factor = int(input('Введите коэффициент (1-10): '))
	if resize_factor < 1 or resize_factor > 10:
		print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
		return

	# Вычисление новых параметров изображения
	pixels_colors_matrix = reshape(state.pixels_colors, state.height_image, state.width_image)
	new_width_image = state.width_image * resize_factor
	new_height_image = state.height_image * resize_factor
	new_pixels_values_count = new_width_image * new_height_image
	new_pixels_colors = [0 for _ in range(0, new_pixels_values_count)]

	# Метод ближайшего соседа
	for i in range(0, new_height_image):
		for j in range(0, new_width_image):
			x = math.floor(i / resize_factor)
			y = math.floor(j / resize_factor)
			pixel_index = i * new_width_image + j
			new_pixels_colors[pixel_index] = pixels_colors_matrix[x][y]

	# Присваивание новых значений
	state.width_image = new_width_image
	state.height_image = new_height_image
	state.pixels_values_count = new_pixels_values_count
	state.pixels_colors = new_pixels_colors

	# Заполнение пикселей цветами
	state.pixels_values = []
	for i in range(0, state.pixels_values_count):
		color_index = state.pixels_colors[i]
		if color_index < 0 or color_index > state.palette_values_count - 1:
			state.pixels_values.append(BACKGROUND_COLOR)
		else:
			state.pixels_values.append(state.palette_values[color_index])

	print(f'{Fore.GREEN}Размер изображения изменен в {resize_factor} раз(а)\n{Style.RESET_ALL}')
