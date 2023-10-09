from PIL import Image
from colorama import Fore
from colorama import Style
from State import State


def show_image():
	"""
	Функция для отображения изображения
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

	image.show()
