
# Coded by Lazutti 


import pygame
import sys
import random

# Ekran ve renkler (Screen and colors)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 20 # FPS Artırıp düşürerek yılan hızını ayarla. (Adjust the snake speed by increasing or decreasing the FPS.)

# Renkler (Colors)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)
        self.grow = False
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.positions[0] == point:
            return
        x1, y1 = self.get_head_position()
        x2, y2 = point
        if x1 + x2 == 0 or y1 + y2 == 0:
            return
        self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + x) % GRID_WIDTH), (cur[1] + y) % GRID_HEIGHT)
        if self.grow and new != self.get_head_position():
            self.grow = False
        self.positions.insert(0, new)
        if not self.grow:
            self.positions.pop()

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)
        self.grow = False
        self.color = GREEN

    def grow_snake(self):
        self.grow = True

    def change_color(self, color):
        self.color = color

class Apple:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        self.color = RED

    def respawn(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Yılan Oyunu - Snake Game')
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        self.snake = Snake()
        self.apple = Apple()
        self.score = 0
        self.font = pygame.font.SysFont('Arial', 24)
        self.game_over = False

    def draw_snake(self):
        for p in self.snake.positions:
            r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(self.surface, self.snake.color, r)

    def draw_apple(self):
        r = pygame.Rect((self.apple.position[0] * GRID_SIZE, self.apple.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.surface, self.apple.color, r)

    def draw_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.surface.blit(score_text, (10, 10))

    def check_collision(self):
        if self.snake.get_head_position() in self.snake.positions[1:]:
            return True
        return False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                    self.snake.turn((0, -1))
                elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                    self.snake.turn((0, 1))
                elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                    self.snake.turn((-1, 0))
                elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                    self.snake.turn((1, 0))

    def check_eat_apple(self):
        if self.snake.get_head_position() == self.apple.position:
            self.snake.grow_snake()
            self.apple.respawn()
            self.score += 1
            if self.score % 5 == 0:
                self.change_snake_color()

    def change_snake_color(self):
        colors = [GREEN, BLUE, YELLOW]
        new_color = random.choice(colors)
        self.snake.change_color(new_color)

    def check_game_over(self):
        if self.check_collision():
            self.game_over = True

    def reset_game(self):
        self.snake.reset()
        self.apple.respawn()
        self.score = 0
        self.game_over = False

    def run(self):
        while True:
            self.handle_input()
            if self.game_over:
                self.surface.fill(BLACK)
                game_over_text = self.font.render('Game Over! Press R to restart', True, WHITE)
                self.surface.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
                pygame.display.update()
                self.reset_game()
                while self.game_over:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                self.reset_game()
                                break
            else:
                self.surface.fill(BLACK)
                self.draw_snake()
                self.draw_apple()
                self.draw_score()
                self.snake.move()
                self.check_eat_apple()
                self.check_game_over()
                pygame.display.update()
                self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
