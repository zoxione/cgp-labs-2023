import os
from colorama import Fore
from colorama import Style
from src.classes.State import State
from src.classes.ImageFile import ImageFile


def read_file():
	"""
	Функция для чтения bin-файла
	"""
	state = State()
	state.clear()

	print('Выберите файл для чтения: ')
	files = os.listdir('./binaries')
	for i in range(0, len(files)):
		print(f'{i}. {files[i]}')
	fileIndex = int(input('Номер файла: '))

	if fileIndex < 0 or fileIndex > len(files):
		print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
		return

	with open(f'./binaries/{files[fileIndex]}', 'rb') as binary_file:
		image_file = ImageFile()

		# Чтение ширины
		temp_bytes = binary_file.read(1)
		temp_bytes += binary_file.read(1)
		image_file.width = int.from_bytes(temp_bytes, byteorder='big')

		# Чтение высоты
		temp_bytes = binary_file.read(1)
		temp_bytes += binary_file.read(1)
		image_file.height = int.from_bytes(temp_bytes, byteorder='big')

		# Чтение кол-ва бит для 1 пикселя
		temp_bytes = binary_file.read(1)
		image_file.bits_per_pixel = int.from_bytes(temp_bytes, byteorder='big')

		# Чтение кол-во цветов
		temp_bytes = binary_file.read(1)
		temp_bytes += binary_file.read(1)
		image_file.palette_values_count = int.from_bytes(temp_bytes, byteorder='big')

		# Чтение ARGB цветов
		for i in range(0, image_file.palette_values_count):
			alpha_byte = binary_file.read(1)
			alpha = int.from_bytes(alpha_byte, byteorder='big')

			red_byte = binary_file.read(1)
			red = int.from_bytes(red_byte, byteorder='big')

			green_byte = binary_file.read(1)
			green = int.from_bytes(green_byte, byteorder='big')

			blue_byte = binary_file.read(1)
			blue = int.from_bytes(blue_byte, byteorder='big')

			image_file.palette_values.append((red, green, blue, alpha))

		# Чтение пикселей
		image_file.pixels_values_count = image_file.width * image_file.height
		temp_bytes = binary_file.read()
		binary_string = ''.join('{:08b}'.format(byte) for byte in temp_bytes)

		# Разделение бинарной строки на пакеты
		batches = []
		for i in range(0, len(binary_string), image_file.bits_per_pixel):
			batches.append(binary_string[i:i+image_file.bits_per_pixel])

		# Чтение пакетов
		for batch in batches:
			image_file.pixels_values.append(int(batch, 2))

		state.image_file = image_file
		print(f'{Fore.GREEN}Bin-файл прочитан\n{Style.RESET_ALL}')
