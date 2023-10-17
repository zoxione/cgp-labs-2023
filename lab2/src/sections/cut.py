import math
from colorama import Fore
from colorama import Style
from src.classes.State import State
from src.data.constants import BACKGROUND_COLOR
from src.sections.read_file import read_file

def cut():
    """
    Функция для вырезания
    """
    state = State()

    if state.image_file is None:
        print(f'{Fore.RED}Нет прочитанного bin-файла!\n{Style.RESET_ALL}')
        return

    print('Прочитайте файл часть которого хотите скопировать')

    source_image = state.image_file # сохранение текущего
    read_file() # чтение нового в текущий
    source_image, state.image_file = state.image_file, source_image # обмен значениями

    state.image_file.palette_values.extend(source_image.palette_values)

    for i in range(int(min(state.image_file.height, source_image.height / 2))):
        for j in range(int(min(state.image_file.width, source_image.width / 2))):

            state_index = i * state.image_file.width + j
            source_index = i * source_image.width + j

            state.image_file.pixels_values[state_index] = \
                source_image.pixels_values[source_index] + state.image_file.palette_values_count

    state.image_file.palette_values_count += len(source_image.palette_values)

    print(f'{Fore.GREEN}Часть изображения скопирована\n{Style.RESET_ALL}')