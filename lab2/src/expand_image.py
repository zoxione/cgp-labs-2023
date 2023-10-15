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


def expand_image():
	"""
	Функция для изменения размера изображения
	"""
	state = State()

	if state.width_image == 0 or state.height_image == 0:
		print(f'{Fore.RED}Нет прочитанного bin-файла!\n{Style.RESET_ALL}')
		return

	axis = str(input('Введите ось для распирения (X,Y): '))
	if axis == 'X' or axis == 'x':
		axis = 'x'
	else:
		axis = 'y'



	resize_factor = int(input('Введите коэффициент (1-10): '))
	if resize_factor < 1 or resize_factor > 10:
		print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
		return

	# Вычисление новых параметров изображения
	pixels_colors_matrix = reshape(state.pixels_colors, state.height_image, state.width_image)

	if axis == 'x':
		new_width_image = state.width_image * resize_factor
		new_height_image = state.height_image
	elif axis == 'y':
		new_height_image = state.height_image * resize_factor
		new_width_image = state.width_image

	new_pixels_colors = [[pixels_colors_matrix[int(i * state.height_image / new_height_image)][
							  int(j * state.width_image / new_width_image)]
						  for j in range(new_width_image)] for i in range(new_height_image)]

	# Присваивание новых значений
	state.width_image = new_width_image
	state.height_image = new_height_image
	state.pixels_values_count = new_width_image * new_height_image
	state.pixels_colors = [color for row in new_pixels_colors for color in row]

	# Заполнение пикселей цветами
	state.pixels_values = []
	for i in range(0, state.pixels_values_count):
		color_index = state.pixels_colors[i]
		if color_index < 0 or color_index > state.palette_values_count - 1:
			state.pixels_values.append(BACKGROUND_COLOR)
		else:
			state.pixels_values.append(state.palette_values[color_index])

	print(f'{Fore.GREEN}Размер изображения изменен в {resize_factor} раз(а) по оси {axis}\n{Style.RESET_ALL}')
