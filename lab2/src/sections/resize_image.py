import math
from colorama import Fore
from colorama import Style
from src.classes.State import State


def resize_image():
	"""
	Функция для увеличения изображения
	"""
	state = State()

	# Проверка на то прочитан ли файл
	if state.image_file is None:
		print(f'{Fore.RED}Нет прочитанного bin-файла!\n{Style.RESET_ALL}')
		return

	resize_factor = int(input('Введите коэффициент (1-10): '))
	if resize_factor < 1 or resize_factor > 10:
		print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
		return

	# Вычисление новых параметров изображения
	new_width = state.image_file.width * resize_factor
	new_height = state.image_file.height * resize_factor
	new_pixels_values_count = new_width * new_height
	new_pixels_values = [0 for _ in range(0, new_pixels_values_count)]

	# Метод ближайшего соседа
	for new_i in range(0, new_height):
		for new_j in range(0, new_width):
			new_pixel_index = new_i * new_width + new_j
			i = math.floor(new_i / resize_factor)
			j = math.floor(new_j / resize_factor)
			pixel_index = i * state.image_file.width + j
			new_pixels_values[new_pixel_index] = state.image_file.pixels_values[pixel_index]

	# Присваивание новых значений
	state.image_file.width = new_width
	state.image_file.height = new_height
	state.image_file.pixels_values_count = new_pixels_values_count
	state.image_file.pixels_values = new_pixels_values

	print(f'{Fore.GREEN}Размер изображения изменен в {resize_factor} раз(а)\n{Style.RESET_ALL}')
