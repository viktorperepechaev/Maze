import random
from collections import deque
import pygame

class Maze:
    def __init__(self, width, height, player_image=None):
        """
        Инициализация класса лабиринта.
        
        width: Ширина лабиринта в клетках
        height: Высота лабиринта в клетках
        """
        self.width = width
        self.height = height
        self.player_image = player_image

        # Начальное положение игрока (в левом верхнем углу)
        self.p_pos_x = 0
        self.p_pos_y = 0

        # Путь, пройденный игроком
        self.p_path = [[0 for _ in range(width)] for _ in range(height)]

        # Положение выхода (будет определено после генерации)
        self.g_pos_x, self.g_pos_y = 1, 1

        # Изначально лабиринт полностью заполнен стенами
        self.maze = [[1 for _ in range(width)] for _ in range(height)]
        
        # Статус посещения клеток для генерации лабиринта
        self.visited = [[False for _ in range(width)] for _ in range(height)]

        # Возможные направления для движения при генерации лабиринта
        self.directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Вниз, вправо, вверх, влево

    def reset(self):
        """
        Сбросить лабиринт и положение игрока к начальному состоянию.
        """
        self.p_pos_x = 0
        self.p_pos_y = 0
        self.p_path = [[0 for _ in range(self.width)] for _ in range(self.height)]

        self.g_pos_x, self.g_pos_y = 1, 1

        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]

    def generate(self):
        """
        Сгенерировать лабиринт с помощью алгоритма Прима.
        """
        # Начинаем с лабиринта, полностью заполненного стенами
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]

        # Начальная клетка для генерации лабиринта
        start_x, start_y = self.p_pos_x, self.p_pos_y
        self.maze[start_y][start_x] = 0
        self.visited[start_y][start_x] = True

        # Список стен для обработки
        walls = []
        self._add_walls(start_x, start_y, walls)

        while walls:
            # Выбираем случайную стену из списка
            wall = random.choice(walls)
            walls.remove(wall)

            x, y, direction = wall
            nx, ny = x + direction[0], y + direction[1]

            # Проверяем, что соседняя клетка в пределах лабиринта и не посещена
            if 0 <= nx < self.width and 0 <= ny < self.height and not self.visited[ny][nx]:
                # Создаём проход в стене между текущей и соседней клеткой
                self.maze[y + direction[1] // 2][x + direction[0] // 2] = 0
                
                # Открываем соседнюю клетку
                self.maze[ny][nx] = 0
                self.visited[ny][nx] = True

                # Добавляем стены новой клетки в список
                self._add_walls(nx, ny, walls)

        # Найти самую далёкую точку от начальной позиции
        self.find_farthest_point(start_x, start_y)

    def _add_walls(self, x, y, walls):
        """
        Добавить стены вокруг текущей клетки в список для обработки.
        
        x: X координата клетки
        y: Y координата клетки
        param walls: Список стен для добавления
        """
        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            
            # Добавляем стену, если соседняя клетка не посещена и находится в пределах лабиринта
            if 0 <= nx < self.width and 0 <= ny < self.height and not self.visited[ny][nx]:
                walls.append((x, y, (dx, dy)))

    def find_farthest_point(self, start_x, start_y):
        """
        Найти самую далёкую точку от начальной позиции с помощью поиска в ширину (BFS).
        
        start_x: X координата начальной точки
        start_y: Y координата начальной точки
        """
        queue = deque([(start_x, start_y, 0)])  # Очередь с начальными координатами и расстоянием
        max_distance = -1
        farthest_point = (start_x, start_y)
        
        # Сброс статуса посещений
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        
        while queue:
            x, y, distance = queue.popleft()
            
            if distance > max_distance:
                max_distance = distance
                farthest_point = (x, y)
            
            # Перебираем соседние клетки
            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < self.width and 0 <= ny < self.height and self.maze[ny][nx] == 0 and not self.visited[ny][nx]:
                    self.visited[ny][nx] = True
                    queue.append((nx, ny, distance + 1))

        # Устанавливаем выход в самой далёкой точке
        self.g_pos_x, self.g_pos_y = farthest_point

    def is_solved(self):
        """
        Проверить, достиг ли игрок выхода.
        
        return: True, если игрок достиг выхода, иначе False
        """
        return (self.p_pos_x == self.g_pos_x) and (self.p_pos_y == self.g_pos_y)

    def move_player(self, dx, dy):
        """
        Переместить игрока в заданном направлении, если это возможно.
        
        dx: Смещение по оси X
        dy: Смещение по оси Y
        """
        if dx == 0 and dy == 0:
            return

        self.p_pos_x += dx
        self.p_pos_y += dy

        # Если переместили в стену или за пределы возвращаем игрока назад
        if (not (0 <= self.p_pos_y < self.height) or
                not (0 <= self.p_pos_x < self.width) or
                (self.maze[self.p_pos_y][self.p_pos_x] != 0)):
            self.p_pos_y -= dy
            self.p_pos_x -= dx
            return
        
        if self.p_path[self.p_pos_y][self.p_pos_x] == 0:
            # Если перешли на клетку на которой нет пути игрока, то прошлая клетка путь игрока
            self.p_path[self.p_pos_y - dy][self.p_pos_x - dx] = 1
        elif self.p_path[self.p_pos_y][self.p_pos_x] == 1:
            # Если перешли на клетку на которой есть путь игрока, то игрок идёт назад, удаляем путь
            self.p_path[self.p_pos_y - dy][self.p_pos_x - dx] = 0

    def draw(self, screen, cell_size):
        """
        Отобразить лабиринт на экране.
        
        screen: Экран для отрисовки
        cell_size: Размер клетки в пикселях
        """
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 1:
                    color = (108, 60, 12)  # Стена (коричневый цвет)
                else:
                    color = (0, 127, 0)  # Путь (зеленый цвет)

                if (x, y) == (self.g_pos_x, self.g_pos_y):
                    color = (255, 127, 0) # Exit
                elif self.p_path[y][x] == 1:
                    color = (154, 205, 50)

                if (x, y) != (self.p_pos_x, self.p_pos_y):
                    pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
                else:
                    color = (154, 205, 50)  # Путь (зеленый цвет)
                    pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
                    screen.blit(self.player_image, (x * cell_size, y * cell_size))
                    color = (0, 127, 0)

