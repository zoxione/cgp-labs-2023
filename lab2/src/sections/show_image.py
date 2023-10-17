from colorama import Fore
from colorama import Style
from src.classes.State import State


def show_image():
	"""
	Функция для отображения изображения
	"""
	state = State()

	# Проверка на то прочитан ли файл
	if state.image_file is None:
		print(f'{Fore.RED}Нет прочитанного bin-файла!\n{Style.RESET_ALL}')
		return

	state.create_image_view()

	state.image_view.show()
