from random import choice, randint
import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTRAL_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Обрабатывает нажатия клавиш и обновляет направление движения объекта."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:  # Закрытие игры при нажатии ESC
                pygame.quit()
                raise SystemExit


class GameObject:
    """Базовый класс для игровых объектов, таких как яблоко и змейка."""

    def __init__(self, body_color=None, position=None):
        if position is None:
            self.position = CENTRAL_POSITION
        else:
            self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Абстрактный метод для отрисовки объекта.
        Переопределяется в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре. Наследуется от GameObject."""

    def __init__(self):
        """Инициализация яблока со случайной позицией."""
        self.randomize_position()
        super().__init__(APPLE_COLOR, self.position)

    def randomize_position(self):
        """Генерация случайной позиции яблока на поле."""
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                         randint(0, GRID_HEIGHT) * GRID_SIZE)

    # Метод draw класса Apple
    def draw(self):
        """Отрисовка яблока на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку в игре. Наследуется от GameObject."""

    def __init__(self):
        """Инициализация змейки с начальной длиной и направлением."""
        super().__init__(SNAKE_COLOR)
        self.length = 1
        self.positions = [CENTRAL_POSITION]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """
        Обновление направления движения змейки в
        соответствии с пользовательским вводом.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Движение змейки в выбранном направлении и проверка
        на столкновения с границами и самой собой.
        """
        head_width, head_height = self.get_head_position()
        new_head_width = head_width + self.direction[0] * GRID_SIZE
        new_head_height = head_height + self.direction[1] * GRID_SIZE
        if new_head_width < 0 or new_head_width > SCREEN_WIDTH:
            new_head_width = abs(new_head_width - SCREEN_WIDTH)
        if new_head_height < 0 or new_head_height > SCREEN_HEIGHT:
            new_head_height = abs(new_head_height - SCREEN_HEIGHT)
        new_head_position = (new_head_width, new_head_height)
        if new_head_position in self.positions[2:]:
            self.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            return
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions[self.length]
            self.positions.pop(self.length)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает параметры змейки до начальных значений."""
        self.length = 1
        self.positions = [CENTRAL_POSITION]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])
        self.next_direction = None

    def draw(self):
        """Отрисовка тела змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def main():
    """
    Основная функция, запускающая игру.
    Создает экземпляры классов Snake и Apple и выполняет основной игровой цикл.
    """
    # Инициализация PyGame:
    pygame.init()

    # Создание экземпляров классов
    snake = Snake()
    apple = Apple()

    high_score = 0

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на съеденное яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            # Обновление рекорда
            if snake.length > high_score:
                high_score = snake.length
            while True:
                apple.randomize_position()
                if apple.position not in snake.positions:
                    break
        pygame.display.set_caption(f'Змейка - Рекорд: {high_score}')
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
