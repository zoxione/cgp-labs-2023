import math
from colorama import Fore
from colorama import Style
from State import State
from constants import BACKGROUND_COLOR

def flip_image():
    """
    Функция для отражения изображения
    """
    state = State()

    if state.width_image == 0 or state.height_image == 0:
        print(f'{Fore.RED}Нет прочитанного bin-файла!\n{Style.RESET_ALL}')
        return

    # Создаем новый список для пикселей отраженного изображения
    new_pixels_colors = [0 for _ in range(state.pixels_values_count)]

    # Проходим по каждой строке изображения
    for i in range(state.height_image):
        # Проходим по каждому пикселю в строке
        for j in range(state.width_image):
            # Вычисляем индекс пикселя в исходном изображении
            pixel_index = i * state.width_image + j
            # Вычисляем индекс пикселя в отраженном изображении
            new_pixel_index = i * state.width_image + (state.width_image - 1 - j)
            # Копируем цвет пикселя из исходного изображения в отраженное изображение
            new_pixels_colors[new_pixel_index] = state.pixels_colors[pixel_index]

    # Присваиваем новые значения пикселей
    state.pixels_colors = new_pixels_colors

    print(f'{Fore.GREEN}Изображение отражено\n{Style.RESET_ALL}')
