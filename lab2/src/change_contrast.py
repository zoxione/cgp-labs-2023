from colorama import Fore
from colorama import Style
from State import State
from constants import BACKGROUND_COLOR


def change_contrast():
	"""
	Функция для изменения уровня контрастности изображения
	"""
	state = State()

	if state.width_image == 0 or state.height_image == 0:
		print(f'{Fore.RED}Нет прочитанного bin-файла!\n{Style.RESET_ALL}')
		return

	contrast_value = int(input('Введите уровень (-255-255): '))
	if contrast_value < -255 or contrast_value > 255:
		print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
		return

	contrast_correction_factor = (259 * (contrast_value + 255)) / (255 * (259 - contrast_value))

	# Изменение палитры изображения
	for i in range(0, state.palette_values_count):
		a, r, g, b = state.palette_values[i]

		# Применяем фактор контрастности к каждому каналу цвета
		r = int(contrast_correction_factor * (r - 128) + 128)
		g = int(contrast_correction_factor * (g - 128) + 128)
		b = int(contrast_correction_factor * (b - 128) + 128)

		# Ограничиваем значения каналов от 0 до 255
		r = min(max(0, r), 255)
		g = min(max(0, g), 255)
		b = min(max(0, b), 255)

		state.palette_values[i] = a, r, g, b

	# Заполнение пикселей цветами
	state.pixels_values = []
	for i in range(0, state.pixels_values_count):
		color_index = state.pixels_colors[i]
		if color_index < 0 or color_index > state.palette_values_count - 1:
			state.pixels_values.append(BACKGROUND_COLOR)
		else:
			state.pixels_values.append(state.palette_values[color_index])

	print(f'{Fore.GREEN}Уровень контрастности изображения изменен на {contrast_value}\n{Style.RESET_ALL}')
