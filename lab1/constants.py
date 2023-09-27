from enum import Enum, unique


# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (32, 32, 48)
COUNT_FIGURES = 10
TARGET_FPS = 60
LIMIT_TRAIL = 24
RADIUS_MOVE_CIRCULAR = 200


# Типы фигуры
@unique
class Shape(Enum):
    Square = 0
    Rectangle = 1
    Circle = 2
    Triangle = 3
    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))

# Направление
@unique
class Direction(Enum):
    Up = 0
    Left = 1
    Down = 2
    Right = 3
    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))

# Режим движения
@unique
class MovementMode(Enum):
    Linear = 0
    Circular = 1
    Gravity = 2
    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))

# Цвета
@unique
class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    CYAN = (0, 255, 255)
    DARK_RED = (128, 0, 0)
    DARK_GREEN = (0, 128, 0)
    DARK_BLUE = (0, 0, 128)
    DARK_YELLOW = (128, 128, 0)
    DARK_PURPLE = (128, 0, 128)
    DARK_CYAN = (0, 128, 128)
    ORANGE = (255, 128, 0)
    LIME = (128, 255, 0)
    PINK = (255, 128, 128)
    SALAD = (128, 255, 128)
    LIGHT_PURPLE = (128, 128, 255)
    PURPURE = (255, 0, 128)
    INDIGO = (128, 0, 255)
    LILAC = (255, 128, 255)
    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))