from colorama import Fore
from colorama import Style
from src.classes.State import State


def change_contrast():
	"""
	Функция для изменения уровня контрастности изображения
	"""
	state = State()

	# Проверка на то прочитан ли файл
	if state.image_file is None:
		print(f'{Fore.RED}Нет прочитанного bin-файла!\n{Style.RESET_ALL}')
		return

	contrast_value = int(input('Введите уровень (-255-255): '))
	if contrast_value < -255 or contrast_value > 255:
		print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
		return

	# Нормализация значения
	contrast_correction_factor = (259 * (contrast_value + 255)) / (255 * (259 - contrast_value))

	# Изменение палитры изображения
	for i in range(0, state.image_file.palette_values_count):
		a, r, g, b = state.image_file.palette_values[i]

		# Применяем фактор контрастности к каждому каналу цвета
		r = int(contrast_correction_factor * (r - 128) + 128)
		g = int(contrast_correction_factor * (g - 128) + 128)
		b = int(contrast_correction_factor * (b - 128) + 128)

		# Ограничиваем значения каналов от 0 до 255
		r = min(max(0, r), 255)
		g = min(max(0, g), 255)
		b = min(max(0, b), 255)

		state.image_file.palette_values[i] = a, r, g, b

	print(f'{Fore.GREEN}Уровень контрастности изображения изменен на {contrast_value}\n{Style.RESET_ALL}')
