import sys
from typing import Callable

from State import State
from generate_file import generate_file
from show_image import show_image
from save_image import save_image
from read_file import read_file
from resize_image import resize_image
from change_contrast import change_contrast

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from expand_image import expand_image

colorama_init()


# Выход из программы
def exit_prog():
	print('Программа завершена', end=" ")
	sys.exit()


# Содержимое меню
MENU: list[tuple[str, Callable[[], None]]] = [
	('Выйти', exit_prog),
	('Сгенерировать bin-файл', generate_file),
	('Прочитать bin-файла', read_file),
	('Отобразить изображение', show_image),
	('Изменить размер изображения', resize_image),
	('Изменить ширину или высоту',expand_image),
	('Изменить уровень контрастности изображения', change_contrast),
	('Сохранить изображение', save_image),
]


# Основной поток программы
if __name__ == '__main__':
	print(f'{Fore.GREEN}--------------------------------------------')
	print(f'Форматы графических файлов. Вариант 3')
	print(f'Выполнили: КТбо4-8 Отхонов Б.Н., Бакухин А.П., Гром. С.А.')
	print(f'--------------------------------------------\n{Style.RESET_ALL}')

	# Начальная инициализация
	state = State()
	action = -1

	while action != 0:
		try:
			for i in range(0, len(MENU)):
				print(f'{i}. {MENU[i][0]}')

			action = int(input('Введите действие: '))
			print('')

			isAction = False
			for i in range(0, len(MENU)):
				if i == action:
					isAction = True
					MENU[action][1]()
					print()

			if not isAction:
				print(f'{Fore.RED}Неверный ввод!\n\n{Style.RESET_ALL}')

		except Exception as e:
			print(f'{Fore.RED}\nВозникла ошибка:\n{e}\n\n{Style.RESET_ALL}')
