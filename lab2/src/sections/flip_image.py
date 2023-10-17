import math
from colorama import Fore
from colorama import Style
from src.classes.State import State
from src.data.constants import BACKGROUND_COLOR

def flip_image():
    """
    Функция для отражения изображения
    """
    state = State()

    if state.image_file is None:
        print(f'{Fore.RED}Нет прочитанного bin-файла!\n{Style.RESET_ALL}')
        return

    # Создаем новый список для пикселей отраженного изображения
    new_pixels_colors = [0 for _ in range(state.image_file.pixels_values_count)]

    # Проходим по каждой строке изображения
    for i in range(state.image_file.height):
        # Проходим по каждому пикселю в строке
        for j in range(state.image_file.width):
            # Вычисляем индекс пикселя в исходном изображении
            pixel_index = i * state.image_file.width + j
            # Вычисляем индекс пикселя в отраженном изображении
            new_pixel_index = i * state.image_file.width + (state.image_file.width - 1 - j)
            # Копируем цвет пикселя из исходного изображения в отраженное изображение
            new_pixels_colors[new_pixel_index] = state.image_file.pixels_values[pixel_index]

    # Присваиваем новые значения пикселей
    state.image_file.pixels_values = new_pixels_colors

    print(f'{Fore.GREEN}Изображение отражено\n{Style.RESET_ALL}')
