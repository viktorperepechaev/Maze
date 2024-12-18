import pygame
import random
import sys
import os

from ComplexityManager import ComplexityManager
from Maze import Maze

# Инициализация Pygame
pygame.init()

info = pygame.display.Info()

# Размеры окна и частота кадров (FPS)
width, height = 800, 600
fps = 60
SCALE = 2
maze_cell_size = 15 * SCALE

font = pygame.font.Font(None, 32)

music_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "background_music.mp3")
pygame.mixer.init()
pygame.mixer.music.load(music_path)
pygame.mixer.music.set_volume(0.5)

win_sound_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "winning_sound.mp3")
win_sound = pygame.mixer.Sound(win_sound_path)
win_sound.set_volume(0.5)

fail_sound_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fail_music.mp3")
fail_sound = pygame.mixer.Sound(fail_sound_path)
fail_sound.set_volume(0.5)

menu_music_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "menu_music.mp3")
menu_music = pygame.mixer.Sound(menu_music_path)
menu_music.set_volume(0.5)

manager = ComplexityManager(width, height, menu_music=menu_music)
complexity = manager.toMenu()

# Создаём окно
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(f"Maze({complexity})")
clock = pygame.time.Clock()

player_image = pygame.image.load("assets/pig.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (maze_cell_size, maze_cell_size))

# Интервал между шагами движения
interval = 0.15  # Время между перемещениями в секундах
last = 0         # Время, прошедшее с последнего движения

# Генерация лабиринта
maze = Maze(width // maze_cell_size, (height - 50) // maze_cell_size, player_image=player_image)
maze.generate()

# Время начала и завершения прохождения лабиринта
start_time = pygame.time.get_ticks()
solved_time = None

# Флаг, указывающий на завершение лабиринта
solved = False

# Главный игровой цикл
failed = False
while True:
    # Обрабатываем события окна
    for event in pygame.event.get():
        fail_sound.stop()
        if event.type == pygame.QUIT:
            # Выходим из игры при закрытии окна
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                # При нажатии клавиш W, A, S или D сразу выполняем движение
                last = interval + 1
            elif event.key == pygame.K_SPACE:
                # Перезапуск лабиринта
                win_sound.stop()
                pygame.mixer.music.stop()
                maze.reset()
                maze.generate()
                pygame.mixer.music.play()
                start_time = pygame.time.get_ticks()
                solved_time = None
                solved = False
            elif event.key == pygame.K_r:
                win_sound.stop()
                pygame.mixer.music.stop()
                complexity = manager.toMenu()
                pygame.display.set_caption(f"Maze({complexity})")
                maze.reset()
                maze.generate()
                pygame.mixer.music.play(-1)
                start_time = pygame.time.get_ticks()
                solved_time = None
                solved = False
                failed = False
    if complexity == "H":
        interval = random.randint(1, 150) / 1000
    if not solved:
        # Логика для незавершённого лабиринта

        # Считываем нажатые клавиши
        pressed_keys = pygame.key.get_pressed()

        if last > interval:
            # Двигаемся в нужном направлении в зависимости от нажатой клавиши

            if maze.is_solved():
                # Если лабиринт пройден, фиксируем время завершения
                pygame.mixer.music.stop()
                win_sound.play()
                solved = True
                solved_time = pygame.time.get_ticks()
            elif pressed_keys[pygame.K_w]:
                maze.move_player(0, -1)  # Движение вверх
            elif pressed_keys[pygame.K_a]:
                maze.move_player(-1, 0)  # Движение влево
            elif pressed_keys[pygame.K_s]:
                maze.move_player(0, 1)   # Движение вниз
            elif pressed_keys[pygame.K_d]:
                maze.move_player(1, 0)   # Движение вправо

            last = 0

    solving_time = (pygame.time.get_ticks() - start_time) / 1000
    # Очистка экрана (заливаем чёрным цветом)
    screen.fill((0, 0, 0))
    if complexity == "G" and solving_time >= 35 or \
        complexity == "H" and solving_time >= 30:
            if not failed:
                pygame.mixer.music.stop()
                fail_sound.play()
                failed = True
            # Сообщение о поражении
            won_text = font.render(f'Поражение(', True, (255, 255, 255))
            time_text = font.render(f'Время вышло!', True, (255, 255, 255))
            restart_text = font.render(f'Нажмите пробел для перезапуска', True, (255, 255, 255))
            select_text = font.render(f'Нажмите R для выбора сложности', True, (255, 255, 255))
            # Размещение текстов на экране
            screen.blit(won_text, (width // 2 - won_text.get_width() // 2,
                               height // 2 - won_text.get_height() - time_text.get_height() // 2))
            screen.blit(time_text, (width // 2 - time_text.get_width() // 2,
                               height // 2 - time_text.get_height() // 2))
            screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2,
                               height // 2 + restart_text.get_height() - time_text.get_height() // 2))
            screen.blit(select_text, (width // 2 - select_text.get_width() // 2,
                               height // 2 + restart_text.get_height() + select_text.get_height() - time_text.get_height() // 2))
    elif not solved:
        # Отрисовка лабиринта, если он ещё не пройден
        maze.draw(screen, maze_cell_size)

        # Вычисление и отображение времени прохождения
        solving_time = (pygame.time.get_ticks() - start_time) / 1000
        time_text = font.render(f'{solving_time:.2f}', True, (255, 255, 255))
        r_text = font.render(f'R - выбор сложности', True, (255, 255, 255))
        space_text = font.render(f'Space - рестарт', True, (255, 255, 255))
        screen.blit(r_text, (width // 2 - time_text.get_width() // 2 - r_text.get_width() - 80, height - 50))
        screen.blit(time_text, (width // 2 - time_text.get_width() // 2, height - 50))
        screen.blit(space_text, (width // 2 - time_text.get_width() // 2 + 120, height - 50))
    else:
        # Отображение экрана победы
        solving_time = (solved_time - start_time) / 1000

        # Сообщение о победе
        won_text = font.render(f'Победа!', True, (255, 255, 255))
        time_text = font.render(f'{solving_time:.2f}s', True, (255, 255, 255))
        restart_text = font.render(f'Нажмите пробел для перезапуска', True, (255, 255, 255))
        select_text = font.render(f'Нажмите R для выбора сложности', True, (255, 255, 255))
        # Размещение текстов на экране
        screen.blit(won_text, (width // 2 - won_text.get_width() // 2,
                               height // 2 - won_text.get_height() - time_text.get_height() // 2))
        screen.blit(time_text, (width // 2 - time_text.get_width() // 2,
                                height // 2 - time_text.get_height() // 2))
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2,
                                   height // 2 + restart_text.get_height() - time_text.get_height() // 2))
        screen.blit(select_text, (width // 2 - select_text.get_width() // 2,
                                   height // 2 + restart_text.get_height() + select_text.get_height() - time_text.get_height() // 2))

    # Обновляем экран
    pygame.display.flip()

    # Поддерживаем нужный FPS
    delta = clock.tick(fps)
    last += delta / 1000
