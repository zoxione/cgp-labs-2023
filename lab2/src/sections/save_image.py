import time
from colorama import Fore
from colorama import Style
from src.classes.State import State


def save_image():
	"""
	Функция для сохранения изображения
	"""
	state = State()

	# Проверка на то прочитан ли файл
	if state.image_file is None:
		print(f'{Fore.RED}Нет прочитанного bin-файла!\n{Style.RESET_ALL}')
		return

	state.create_image_view()

	# Сохранение изображения
	state.image_view.save(f'./output_images/image_{state.image_file.width}_{state.image_file.height}_{state.image_file.bits_per_pixel}_{state.image_file.palette_values_count}_{time.time()}.png')

	print(f'{Fore.GREEN}Изображение сохранено в папку output_images\n{Style.RESET_ALL}')
