from constants import SCREEN_WIDTH, SCREEN_HEIGHT, Shape, Color, LIMIT_TRAIL, Direction
import math

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

    def move(self):
        # Движение по направлению
        self.x += self.dx
        self.y += self.dy

        # Проверка на отражение от краев экрана
        if self.x - self.width / 2 <= 0 or self.x + self.width / 2 >= SCREEN_WIDTH:
            self.dx = -self.dx
            self.x = max(self.width / 2, min(SCREEN_WIDTH - self.width / 2, self.x))
        if self.y - self.height / 2 <= 0 or self.y + self.height / 2 >= SCREEN_HEIGHT:
            self.dy = -self.dy
            self.y = max(self.height / 2, min(SCREEN_HEIGHT - self.height / 2, self.y))

    def change_direction(self, direction: Direction):
        # Выбор направления
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

        self.move()

    def update_trail(self):
        self.trail.append([self.x, self.y])

        if len(self.trail) > LIMIT_TRAIL:
            self.trail.pop(0)