import os
import random
import time
from PIL import Image
from colorama import Fore
from colorama import Style
import concurrent.futures


def generate_random_colors(palette_values_count):
	"""
	Функция для рандомной генерации цветов пикселей.
	"""
	colors = []

	for _ in range(0, palette_values_count):
		alpha = random.randint(0, 255)
		red = random.randint(0, 255)
		green = random.randint(0, 255)
		blue = random.randint(0, 255)
		colors.extend([alpha, red, green, blue])

	return colors


def generate_random_pixels(pixel_values_count, palette_values_count):
	"""
	Функция для рандомной генерации пикселей
	"""
	pixels = []

	for _ in range(0, pixel_values_count):
		# Может генерировать цвет, которого нет
		color_index = random.randint(0, palette_values_count + 1)
		pixels.append(color_index)

	return pixels


def convert_to_bytes(pixel_values, bits_per_pixel):
	"""
	Функция для конвертации пикселей в байты
	"""
	def convert_to_bytes_chunk(chunk, bits_per_pixel_chunk):
		output_hex_chunk = ''
		for value in chunk:
			binary_representation = bin(value)[2:]
			binary_representation = binary_representation.zfill(bits_per_pixel_chunk)
			output_hex_chunk += binary_representation

		return output_hex_chunk

	# Разбиение значений пикселей на фрагменты на основе битов на пиксель
	chunk_size = bits_per_pixel * 4
	pixel_chunks = []
	for i in range(0, len(pixel_values), chunk_size):
		pixel_chunks.append(pixel_values[i:i+chunk_size])

	# Параллельное выполнение функции convert_to_bytes_chunk()
	with concurrent.futures.ThreadPoolExecutor() as executor:
		hex_result_chunks = executor.map(lambda chunk: convert_to_bytes_chunk(chunk, bits_per_pixel), pixel_chunks)

	# Конкатенация результатов, полученных из разных фрагментов
	output_hex = ''.join(hex_result_chunks)

	# Разбиение выходного_гекса на символы, кратные 8
	output_hex_length = len(output_hex)
	output_hex = output_hex.ljust((output_hex_length + 7) // 8 * 8, '0')

	# Преобразование двоичной строки в байты
	hex_result_bytes = bytes(int(output_hex[i:i + 8], 2) for i in range(0, len(output_hex), 8))

	return hex_result_bytes


def generate_file():
	"""
	Функция для генерации файла
	"""
	isUploadImage = str(input('Выбрать изображение? (Y/n): '))

	# Начальная инициализация
	width_image = 0
	height_image = 0
	bits_per_pixel = 0
	palette_values_count = 0
	binary_data = b''
	file_name = ''

	if isUploadImage == 'Y':
		print('Выберите изображение из папки images: ')
		files = os.listdir('./images')
		for i in range(0, len(files)):
			print(f'{i}. {files[i]}')
		file_index = int(input('Номер изображения: '))

		if file_index < 0 or file_index > len(files):
			print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
			return

		# Инициализация изображения
		image = Image.open(f'./images/{files[file_index]}')
		width_image = image.width
		height_image = image.height
		bits_per_pixel = random.randint(6, 16)
		palette_values_count = 32

		# Преобразование изображения в нужный формат
		image = image.convert('P', palette=Image.ADAPTIVE, colors=palette_values_count)
		image = image.convert('RGBA')

		# Получение палитры из изображения
		colors = image.getcolors()
		palette_values = []
		for color in colors:
			palette_values.append(color[1])

		# Присваивание пикселям индексов цветов
		pixels_values = []
		for y in range(0, height_image):
			for x in range(0, width_image):
				color = image.getpixel((x, y))
				if color in palette_values:
					pixels_values.append(palette_values.index(color))
				else:
					pixels_values.append(34)

		# Преобразование палитры в нужный формат
		temp_palette_values = palette_values
		palette_values = []
		for item in temp_palette_values:
			r, g, b, a = item
			palette_values.extend([a, r, g, b])

		file_name = f'{files[file_index].split(".")[0]}_{width_image}_{height_image}_{bits_per_pixel}_{palette_values_count}_{time.time()}.bin'

	else:
		width_image = int(input('Ширина изображения (1-5000): '))
		if width_image < 1 or width_image > 5000:
			print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
			return

		height_image = int(input('Высота изображения (1-5000): '))
		if height_image < 1 or height_image > 5000:
			print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
			return

		bits_per_pixel = int(input('Кол-во бит на пиксель (1-16): '))
		if bits_per_pixel < 1 or bits_per_pixel > 16:
			print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
			return

		palette_values_count = int(input('Кол-во значений в палитре (1-32): '))
		if palette_values_count < 1 or palette_values_count > 32:
			print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
			return

		# Проверка на минимально возможное число бит для одного пикселя
		if len(bin(palette_values_count)[2:]) > bits_per_pixel:
			print(f'{Fore.RED}Числа бит для пикселя недостаточно!\n{Style.RESET_ALL}')
			return

		# Рандомная генерация изображения
		palette_values = generate_random_colors(palette_values_count)
		pixels_values = generate_random_pixels(width_image * height_image, palette_values_count)

		file_name = f'input_{width_image}_{height_image}_{bits_per_pixel}_{palette_values_count}_{time.time()}.bin'

	# Преобразование данных в бинарный формат
	binary_data += int(width_image).to_bytes(2, byteorder='big')
	binary_data += int(height_image).to_bytes(2, byteorder='big')
	binary_data += int(bits_per_pixel).to_bytes(1, byteorder='big')
	binary_data += int(palette_values_count).to_bytes(2, byteorder='big')
	for i in range(0, len(palette_values)):
		binary_data += int(palette_values[i]).to_bytes(1, byteorder='big')
	binary_data += convert_to_bytes(pixels_values, bits_per_pixel)

	# Сохранение данных в файл
	with open(f'./binaries/{file_name}', "wb") as file:
		file.write(binary_data)
		print(f'{Fore.GREEN}Bin-файл сгенерирован в папку binaries\n{Style.RESET_ALL}')
