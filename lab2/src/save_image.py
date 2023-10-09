import time
from PIL import Image
from colorama import Fore
from colorama import Style
from State import State


def save_image():
	"""
	Функция для сохранения изображения
	"""
	state = State()

	if state.width_image == 0 or state.height_image == 0:
		print(f'{Fore.RED}Нет прочитанного bin-файла!\n{Style.RESET_ALL}')
		return

	image = Image.new('RGBA', (state.width_image, state.height_image))
	for y in range(state.height_image):
		for x in range(state.width_image):
			pixel_index = y * state.width_image + x
			a, r, g, b = state.pixels_values[pixel_index]
			image.putpixel((x, y), (a, r, g, b))

	image.save(f'../output_images/image_{state.width_image}_{state.height_image}_{state.bits_per_pixel}_{state.palette_values_count}_{time.time()}.png')

	print(f'{Fore.GREEN}Изображение сохранено в папку output_images\n{Style.RESET_ALL}')
