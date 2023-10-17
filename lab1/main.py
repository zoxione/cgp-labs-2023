import math
import random
import pygame
import sys
import time
from Figure import Figure
from State import State
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, Color, BACKGROUND_COLOR, Shape, COUNT_FIGURES, TARGET_FPS, Direction, MovementMode, K


def clear_screen(current_x, current_y, future_x, future_y, width, height, shape: Shape):
    """
    Функция для очистки экрана (Общая)
    """
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


def display_info(font, x, y, dx, dy):
    """
    Функция для отображения инфы о фигуре (Общая)
    """
    state = State()
    velocity_text = font.render(f"Velocity: ({dx}, {dy})", True, Color.WHITE.value)
    state.screen.blit(velocity_text, (x - 20, y - 40))


def display_fps(clock, font, surface):
    """
    Функция для отображения фпс (Общая)
    """
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, Color.WHITE.value)
    surface.fill(BACKGROUND_COLOR)
    surface.blit(fps_text, (10, 10))


def draw_figure(surface, shape: Shape, x, y, width, height, color_fill, color_outline = None):
    """
    Функция для рисования фигуры (Общая)
    """
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


def draw_trail(trail, shape: Shape, width, height, color_fill):
    """
    Функция для рисования следа от фигуры (Отхонов)
    """
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


def handle_keys():
    """
    Функция для обработки событий клавиш (Отховнов + Бакухин + Гром)
    """
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

    if keys[pygame.K_1]:
        state.movement_mode = MovementMode.Linear
    elif keys[pygame.K_2]:
        state.movement_mode = MovementMode.Circular
    elif keys[pygame.K_3]:
        for f in state.figures:
            f.dy = -3
        state.movement_mode = MovementMode.Gravity
    elif keys[pygame.K_4]:
        state.movement_mode = MovementMode.Linear
        init_figures(True)
    elif keys[pygame.K_5]:
        for f in state.figures:
            f.dx = 1
            f.dy = K


def check_collision(figure1, figure2):
    """
    Функция проверки на коллизию двух фигур (Бакухин)
    """
    if (figure1.x + figure1.width / 2 > figure2.x - figure2.width / 2 and
            figure1.x - figure1.width / 2 < figure2.x + figure2.width / 2 and
            figure1.y + figure1.height / 2 > figure2.y - figure2.height / 2 and
            figure1.y - figure1.height / 2 < figure2.y + figure2.height / 2):
        return True
    return False


def handle_collision(figure1, figure2):
    """
    Функция для обработки коллизии двух фигур (Бакухин + Гром)
    """
    if (state.movement_mode == MovementMode.Gravity):
        top_figure = figure1 if figure1.y < figure2.y else figure2
        bottom_figure = figure2 if figure1.y < figure2.y else figure1
        top_figure.dy = 0
        top_figure.y = bottom_figure.y - bottom_figure.height / 2 - top_figure.height / 2
    else:
        # Рассчитываем расстояние между центрами фигур
        distance = math.sqrt((figure1.x - figure2.x) ** 2 + (figure1.y - figure2.y) ** 2)

        # Рассчитываем перекрытие
        overlap = (figure1.width + figure2.width) / 2 - distance

        # Если есть перекрытие, то отодвигаем фигуры
        if overlap > 0:
            angle = math.atan2(figure2.y - figure1.y, figure2.x - figure1.x)
            dx = overlap * math.cos(angle)
            dy = overlap * math.sin(angle)
            figure1.x -= dx
            figure1.y -= dy
            figure2.x += dx
            figure2.y += dy

            # Меняем направление движения
            figure1.dx = -figure1.dx
            figure1.dy = -figure1.dy
            figure2.dx = -figure2.dx
            figure2.dy = -figure2.dy


last_click = time.time()
def draw_menu(surface, font):
    global last_click
    state = State()

    pygame.draw.rect(surface, 'blue', pygame.Rect(200, 10, 80, 30))
    exit_text = font.render("Выход", True, Color.WHITE.value)
    state.screen.blit(exit_text, (210, 20))

    pygame.draw.rect(surface, 'blue', pygame.Rect(300, 10, 150, 30))
    pause_text = font.render("Пауза/Продолжить", True, Color.WHITE.value)
    state.screen.blit(pause_text, (310, 20))

    pygame.draw.rect(surface, 'blue', pygame.Rect(470, 10, 120, 30))
    exit_text = font.render("Перезапустить", True, Color.WHITE.value)
    state.screen.blit(exit_text, (480, 20))
    
    mouse_key = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    if (mouse_key[0] and mouse_pos[1] > 10 and mouse_pos[1] < 40):
        if (mouse_pos[0] > 200 and mouse_pos[0] < 280):
            exit()
        elif (mouse_pos[0] > 300 and mouse_pos[0] < 450):
            if (time.time() - last_click > 0.5):
                state.game_run = not state.game_run
                last_click = time.time()
        elif (mouse_pos[0] > 470 and mouse_pos[0] < 590):
            state.movement_mode = MovementMode.Linear
            init_figures()


def init_figures(rect_only=False):
    state.figures.clear()
    # Инициализация фигур
    for _ in range(COUNT_FIGURES):
        shape = Shape.Rectangle if rect_only else random.choice(list(Shape))
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
    state.user_figure = Figure(Shape.Circle, user_position[0], user_position[1], user_size[0], user_size[1], user_velocity[0], user_velocity[1], Color.RED, Color.YELLOW)


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

    init_figures()

    # Основной цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if (state.game_run):
            user_current_x = state.user_figure.x
            user_current_y = state.user_figure.y

            state.user_figure.move(MovementMode.Linear)
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

            # Обработка нажатий на клавиши
            handle_keys()

            # Отображение ФПС
            display_fps(clock, fps_font, fps_surface)
            screen.blit(fps_surface, (10, 10))

            # Цикл работы с фигурами
            for figure in state.figures:
                # Проверка на коллизию каждой фигуры с каждой
                for other_figure in state.figures:
                    if figure != other_figure:
                        if check_collision(figure, other_figure):
                            handle_collision(figure, other_figure)

                figure.color_fill = random.choice(list(Color))
                current_x = figure.x
                current_y = figure.y
                
                figure.move(state.movement_mode)

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

        draw_menu(screen, info_font)
    
        pygame.display.flip()
        clock.tick(TARGET_FPS)
