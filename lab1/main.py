import math
import random
import pygame
import sys
from Figure import Figure
from State import State
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, Color, BACKGROUND_COLOR, Shape, COUNT_FIGURES, TARGET_FPS, Direction


# Функция для очистки экрана
def clear_screen(current_x, current_y, future_x, future_y, width, height, shape: Shape):
    state = State()

    draw_figure(
        state.screen,
        shape,
        current_x,
        current_y,
        width,
        height,
        BACKGROUND_COLOR
    )
    draw_figure(
        state.screen,
        shape,
        future_x,
        future_y,
        width,
        height,
        BACKGROUND_COLOR
    )


# Функция для отображения инфы о фигуре
def display_info(font, x, y, dx, dy):
    state = State()
    velocity_text = font.render(f"Velocity: ({dx}, {dy})", True, Color.WHITE.value)
    state.screen.blit(velocity_text, (x - 20, y - 40))


# Функция для отображения фпс
def display_fps(clock, font, surface):
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, Color.WHITE.value)
    surface.fill(BACKGROUND_COLOR)
    surface.blit(fps_text, (10, 10))


# Функция для рисования фигуры
def draw_figure(surface, shape: Shape, x, y, width, height, color_fill, color_outline = None):
    outline_size = 3
    vertices = []

    if shape == Shape.Square:
        # Квадрат (4 вершины)
        half_width = width / 2
        half_height = height / 2
        vertices = [(x - half_width, y - half_height),
                    (x + half_width, y - half_height),
                    (x + half_width, y + half_height),
                    (x - half_width, y + half_height)]
    elif shape == Shape.Rectangle:
        # Прямоугольник (4 вершины)
        half_width = width / 2
        half_height = height / 2
        vertices = [(x - half_width, y - half_height),
                    (x + half_width, y - half_height),
                    (x + half_width, y + half_height),
                    (x - half_width, y + half_height)]
    elif shape == Shape.Circle:
        # Круг (num_vertices вершин)
        num_vertices = 20
        radius = min(width, height) / 2
        for i in range(num_vertices):
            angle = 2 * math.pi * i / num_vertices
            vertex_x = x + int(radius * math.cos(angle))
            vertex_y = y + int(radius * math.sin(angle))
            vertices.append((vertex_x, vertex_y))
    elif shape == Shape.Triangle:
        # Треугольник (3 вершины)
        half_width = width / 2
        half_height = height / 2
        vertices = [(x, y - half_height),
                    (x - half_width, y + half_height),
                    (x + half_width, y + half_height)]

    pygame.draw.polygon(surface, color_fill, vertices)
    if color_outline != None:
        pygame.draw.polygon(surface, color_outline, vertices, outline_size)


# Функция для рисования следа от фигуры
def draw_trail(trail, shape: Shape, width, height, color_fill):
    state = State()

    # Создаем поверхность для хвоста с прозрачностью
    trail_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    # Отображаем хвост
    for i, position in enumerate(trail):
        alpha = int(255 * (i + 1) / len(trail) / 2)
        trail_color = color_fill + (alpha,)
        draw_figure(trail_surface, shape, position[0], position[1], width, height, trail_color)

    # Отображаем хвост за текущей фигурой
    state.screen.blit(trail_surface, (0, 0))


# Функция для обработки событий клавиш
def handle_keys():
    keys = pygame.key.get_pressed()
    state = State()

    if keys[pygame.K_UP]:
        state.user_figure.change_direction(Direction.Up)
    elif keys[pygame.K_DOWN]:
        state.user_figure.change_direction(Direction.Down)
    if keys[pygame.K_LEFT]:
        state.user_figure.change_direction(Direction.Left)
    elif keys[pygame.K_RIGHT]:
        state.user_figure.change_direction(Direction.Right)


# Главная функция для выполнения основной логики
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    pygame.display.set_caption('[1] Средства вывода графики')
    fps_surface = pygame.Surface((100, 50))

    clock = pygame.time.Clock()
    fps_font = pygame.font.Font(None, 36)
    info_font = pygame.font.Font(None, 20)

    state = State()
    state.screen = screen

    # Инициализация фигур
    for _ in range(COUNT_FIGURES):
        shape = random.choice(list(Shape))
        position = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
        size = [random.randint(16, 42), random.randint(16, 42)]
        velocity = [random.randint(-5, 5), random.randint(-5, 5)]
        color_fill = random.choice(list(Color))
        color_outline = random.choice(list(Color))
        state.figures.append(Figure(shape, position[0], position[1], size[0], size[1], velocity[0], velocity[1], color_fill, color_outline))

    # Инициализация фигуры для пользователя
    user_position = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
    user_size = [random.randint(16, 42), random.randint(16, 42)]
    user_velocity = [random.randint(-5, 5), random.randint(-5, 5)]
    state.user_figure = Figure(Shape.Square, user_position[0], user_position[1], user_size[0], user_size[1], user_velocity[0], user_velocity[1], Color.RED, Color.YELLOW)

    # Основной цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        user_current_x = state.user_figure.x
        user_current_y = state.user_figure.y

        state.user_figure.move()
        clear_screen(
            user_current_x,
            user_current_y,
            state.user_figure.x,
            state.user_figure.y,
            state.user_figure.width,
            state.user_figure.height,
            state.user_figure.shape
        )
        state.screen.fill(BACKGROUND_COLOR)
        draw_figure(
            screen,
            state.user_figure.shape,
            state.user_figure.x,
            state.user_figure.y,
            state.user_figure.width,
            state.user_figure.height,
            state.user_figure.color_fill.value,
            state.user_figure.color_outline.value
        )

        state.user_figure.update_trail()
        draw_trail(
            state.user_figure.trail,
            state.user_figure.shape,
            state.user_figure.width,
            state.user_figure.height,
            state.user_figure.color_fill.value
        )
        display_info(info_font, state.user_figure.x, state.user_figure.y, state.user_figure.dx, state.user_figure.dy)

        # Обработка нажатий на стрелки
        handle_keys()

        # Отображение ФПС
        display_fps(clock, fps_font, fps_surface)
        screen.blit(fps_surface, (10, 10))

        for figure in state.figures:
            figure.color_fill = random.choice(list(Color))
            current_x = figure.x
            current_y = figure.y

            figure.move()
            clear_screen(
                current_x,
                current_y,
                figure.x,
                figure.y,
                figure.width,
                figure.height,
                figure.shape
            )
            draw_figure(
                screen,
                figure.shape,
                figure.x,
                figure.y,
                figure.width,
                figure.height,
                figure.color_fill.value
            )
            display_info(info_font, figure.x, figure.y, figure.dx, figure.dy)

        pygame.display.flip()
        clock.tick(TARGET_FPS)
