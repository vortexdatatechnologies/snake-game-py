import pygame
import random

# Dimensiones de la ventana
WIDTH = 640
HEIGHT = 480

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Tamaño del bloque y velocidad de la serpiente
BLOCK_SIZE = 20
SNAKE_SPEED = 10

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

    def run(self):
        self.snake = Snake()
        self.food = Food()

        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_event(event.key)

            self.snake.update()
            self.check_collision()

            self.window.fill(BLACK)
            self.snake.draw(self.window)
            self.food.draw(self.window)
            pygame.display.update()
            self.clock.tick(SNAKE_SPEED)

        pygame.quit()

    def handle_key_event(self, key):
        if key == pygame.K_LEFT and self.snake.direction != (1, 0):
            self.snake.direction = (-1, 0)
        elif key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
            self.snake.direction = (1, 0)
        elif key == pygame.K_UP and self.snake.direction != (0, 1):
            self.snake.direction = (0, -1)
        elif key == pygame.K_DOWN and self.snake.direction != (0, -1):
            self.snake.direction = (0, 1)

    def check_collision(self):
        if self.snake.head == self.food.position:
            self.snake.grow()
            self.food.generate()
        elif self.snake.is_collision():
            self.game_over()

    def game_over(self):
        font = pygame.font.Font(None, 50)
        text = font.render("Game Over!", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.window.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)

class Snake:
    def __init__(self):
        self.head = [WIDTH // 2, HEIGHT // 2]
        self.body = [self.head]
        self.direction = (0, 0)

    def update(self):
        self.move()
        self.body.insert(0, list(self.head))
        self.body.pop()

    def move(self):
        self.head[0] += self.direction[0] * BLOCK_SIZE
        self.head[1] += self.direction[1] * BLOCK_SIZE

        self.check_boundary()

    def check_boundary(self):
        if self.head[0] < 0:
            self.head[0] = WIDTH - BLOCK_SIZE
        elif self.head[0] >= WIDTH:
            self.head[0] = 0

        if self.head[1] < 0:
            self.head[1] = HEIGHT - BLOCK_SIZE
        elif self.head[1] >= HEIGHT:
            self.head[1] = 0

    def draw(self, window):
        for segment in self.body:
            pygame.draw.rect(window, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

    def grow(self):
        self.body.append(list(self.head))

    def is_collision(self):
        return self.head in self.body[1:]

class Food:
    def __init__(self):
        self.position = [0, 0]
        self.generate()

    def generate(self):
        self.position[0] = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.position[1] = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE

    def draw(self, window):
        pygame.draw.rect(window, RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

if __name__ == '__main__':
    game = SnakeGame()
    game.run()
