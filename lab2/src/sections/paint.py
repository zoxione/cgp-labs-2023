import math
from colorama import Fore
from colorama import Style
from src.classes.State import State
from src.data.constants import BACKGROUND_COLOR
from src.sections.read_file import read_file

def paint():
    """
    Функция для покраски
    """
    state = State()

    if state.image_file is None:
        print(f'{Fore.RED}Нет прочитанного bin-файла!\n{Style.RESET_ALL}')
        return
    
    color = tuple(map(int, input("в какой цвет перекрасить (r g b a): ").split()))
    if (len(color) != 4):
        print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
        return
    
    for i in range(state.image_file.palette_values_count):
        if (state.image_file.palette_values[i][0] > 200 and
            state.image_file.palette_values[i][1] > 200 and
            state.image_file.palette_values[i][2] > 200):
        
            state.image_file.palette_values[i] = color


    print(f'{Fore.GREEN}Оттенок изображения изменен\n{Style.RESET_ALL}')