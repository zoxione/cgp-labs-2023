import math
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, Shape, Color, LIMIT_TRAIL, Direction, MovementMode, RADIUS_MOVE_CIRCULAR


class Figure:
    def __init__(self, shape: Shape, x: int, y: int, width, height, dx: int, dy: int, color_fill: Color, color_outline: Color):
        self.shape = shape
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.s_dx = dx
        self.s_dy = dy
        self.dx = dx
        self.dy = dy
        self.color_fill = color_fill
        self.color_outline = color_outline
        self.trail = []
        self.angle = random.uniform(0, 2 * math.pi)

    def check_screen_boundary(self):
        """
        Метод проверки на отражение от краев экрана (Отхонов + Бакухин)
        """
        if self.x - self.width / 2 <= 0 or self.x + self.width / 2 >= SCREEN_WIDTH:
            self.dx = -self.dx
            self.x = max(self.width / 2, min(SCREEN_WIDTH - self.width / 2, self.x))
        if self.y - self.height / 2 <= 0 or self.y + self.height / 2 >= SCREEN_HEIGHT:
            self.dy = -self.dy
            self.y = max(self.height / 2, min(SCREEN_HEIGHT - self.height / 2, self.y))

    def move(self, movement_mode: MovementMode):
        """
        Метод для движения (Общий)
        """
        if movement_mode.value == MovementMode.Linear.value:
            self.move_linear()
        elif movement_mode.value == MovementMode.Circular.value:
            self.move_circular(RADIUS_MOVE_CIRCULAR)

    def move_linear(self):
        """
        Метод для движения по направлению (Отхонов)
        """
        self.x += self.dx
        self.y += self.dy
        self.check_screen_boundary()

    def move_circular(self, radius: float):
        """
        Метод для движения по концентрической траектории (Бакухин)
        """
        self.x = SCREEN_WIDTH / 2 + radius * math.cos(self.angle)
        self.y = SCREEN_HEIGHT / 2 + radius * math.sin(self.angle)
        self.angle += 0.02
        self.angle %= 2 * math.pi # угол остается в диапазоне [0, 2*pi)

    def change_direction(self, direction: Direction):
        """
        Метод для изменения направления движения (Отхонов)
        """
        if direction.value == Direction.Up.value:
            # Движение вверх
            self.dy = abs(self.dx) * -1 if self.s_dy == 0 else abs(self.s_dy) * -1
            self.dy = -3 if self.dy == 0 else self.dy
            self.dx = 0
        elif direction.value == Direction.Down.value:
            # Движение вниз
            self.dy = abs(self.dx) if self.s_dy == 0 else abs(self.s_dy)
            self.dy = 3 if self.dy == 0 else self.dy
            self.dx = 0
        elif direction.value == Direction.Left.value:
            # Движение влево
            self.dx = abs(self.dy) * -1 if self.s_dx == 0 else abs(self.s_dx) * -1
            self.dx = -3 if self.dx == 0 else self.dx
            self.dy = 0
        elif direction.value == Direction.Right.value:
            # Движение вправо
            self.dx = abs(self.dy) if self.s_dx == 0 else abs(self.s_dx)
            self.dx = 3 if self.dx == 0 else self.dx
            self.dy = 0

    def update_trail(self):
        """
        Метод для обновления хвоста фигуры (Отхонов)
        """
        self.trail.append([self.x, self.y])
        if len(self.trail) > LIMIT_TRAIL:
            self.trail.pop(0)