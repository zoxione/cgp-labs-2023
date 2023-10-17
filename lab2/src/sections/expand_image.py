from colorama import Fore
from colorama import Style
from src.classes.State import State


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

	# Проверка на то прочитан ли файл
	if state.image_file is None:
		print(f'{Fore.RED}Нет прочитанного bin-файла!\n{Style.RESET_ALL}')
		return

	axis = str(input('Введите ось для расширения (X,Y): '))
	if axis == 'X' or axis == 'x':
		axis = 'x'
	else:
		axis = 'y'

	resize_factor = int(input('Введите коэффициент (1-10): '))
	if resize_factor < 1 or resize_factor > 10:
		print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
		return

	# Создание матрицы
	pixels_values_matrix = reshape(state.image_file.pixels_values, state.image_file.height, state.image_file.width)

	# Вычисление новых параметров изображения
	new_width = state.image_file.width
	new_height = state.image_file.height
	if axis == 'x':
		new_width = state.image_file.width * resize_factor
		new_height = state.image_file.height
	elif axis == 'y':
		new_height = state.image_file.height * resize_factor
		new_width = state.image_file.width

	new_pixels_values = [
		[pixels_values_matrix[int(i * state.image_file.height / new_height)]
			[int(j * state.image_file.width / new_width)]
			for j in range(new_width)] for i in range(new_height)
	]

	# Присваивание новых значений
	state.image_file.width = new_width
	state.image_file.height = new_height
	state.image_file.pixels_values_count = new_width * new_height
	state.image_file.pixels_values = [color for row in new_pixels_values for color in row]

	print(f'{Fore.GREEN}Размер изображения изменен в {resize_factor} раз(а) по оси {axis}\n{Style.RESET_ALL}')
