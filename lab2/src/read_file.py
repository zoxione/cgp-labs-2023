import os
from colorama import Fore
from colorama import Style
from State import State
from constants import BACKGROUND_COLOR


def read_file():
	"""
	Функция для чтения bin-файла
	"""
	state = State()
	state.clear()

	print('Выберите файл для чтения: ')
	files = os.listdir('../binaries')
	for i in range(0, len(files)):
		print(f'{i}. {files[i]}')
	fileIndex = int(input('Номер файла: '))

	if fileIndex < 0 or fileIndex > len(files):
		print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
		return

	with open(f'../binaries/{files[fileIndex]}', 'rb') as binary_file:
		# Чтение ширины
		temp_bytes = binary_file.read(1)
		temp_bytes += binary_file.read(1)
		state.width_image = int.from_bytes(temp_bytes, byteorder='big')

		# Чтение высоты
		temp_bytes = binary_file.read(1)
		temp_bytes += binary_file.read(1)
		state.height_image = int.from_bytes(temp_bytes, byteorder='big')

		# Чтение кол-ва бит для 1 пикселя
		temp_bytes = binary_file.read(1)
		state.bits_per_pixel = int.from_bytes(temp_bytes, byteorder='big')

		# Чтение кол-во цветов
		temp_bytes = binary_file.read(1)
		temp_bytes += binary_file.read(1)
		state.palette_values_count = int.from_bytes(temp_bytes, byteorder='big')

		# Чтение ARGB цветов
		for i in range(0, state.palette_values_count):
			alpha_byte = binary_file.read(1)
			alpha = int.from_bytes(alpha_byte, byteorder='big')

			red_byte = binary_file.read(1)
			red = int.from_bytes(red_byte, byteorder='big')

			green_byte = binary_file.read(1)
			green = int.from_bytes(green_byte, byteorder='big')

			blue_byte = binary_file.read(1)
			blue = int.from_bytes(blue_byte, byteorder='big')

			state.palette_values.append((red, green, blue, alpha))

		# Чтение пикселей
		state.pixels_values_count = state.width_image * state.height_image
		temp_bytes = binary_file.read()
		binary_string = ''.join('{:08b}'.format(byte) for byte in temp_bytes)

		# Разделение бинарной строки на пакеты и преобразование в число
		batches = []
		for i in range(0, len(binary_string), state.bits_per_pixel):
			batches.append(binary_string[i:i+state.bits_per_pixel])
		for batch in batches:
			state.pixels_colors.append(int(batch, 2))

		# Преобразование цветов пикселей
		for i in range(0, state.pixels_values_count):
			color_index = state.pixels_colors[i]
			if color_index < 0 or color_index > state.palette_values_count - 1:
				state.pixels_values.append(BACKGROUND_COLOR)
			else:
				state.pixels_values.append(state.palette_values[color_index])

		print(f'{Fore.GREEN}Bin-файл прочитан\n{Style.RESET_ALL}')
