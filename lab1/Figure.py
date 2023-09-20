from constants import SCREEN_WIDTH, SCREEN_HEIGHT, Shape, Color, LIMIT_TRAIL


class Figure:
    def __init__(self, shape: Shape, x: int, y: int, width, height, dx: int, dy: int, color_fill: Color, color_outline: Color):
        self.shape = shape
        self.x = x
        self.y = y
        self.width = width
        self.height = height
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
        if self.x <= 0 or self.x >= SCREEN_WIDTH:
            self.dx = -self.dx
            self.x = max(0, min(SCREEN_WIDTH, self.x))
        if self.y <= 0 or self.y >= SCREEN_HEIGHT:
            self.dy = -self.dy
            self.y = max(0, min(SCREEN_HEIGHT, self.y))

    def update_trail(self):
        self.trail.append([self.x, self.y])

        if len(self.trail) > LIMIT_TRAIL:
            self.trail.pop(0)