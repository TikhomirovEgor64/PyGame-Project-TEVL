import pygame
import random

WindowSize = (720, 480)
class SnakeGame:
    def __init__(self, window_size=(720, 480), tside=30, fps=5):
        pygame.init()
        self.window_size = window_size
        self.tside = tside
        self.msize = (window_size[0] // tside, window_size[1] // tside)
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption('Змейка')
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.font_gameover = pygame.font.SysFont("Liberation Serif", 52)
        self.start_pos = (self.msize[0] // 2, self.msize[1] // 2)
        self.snake = [self.start_pos]
        self.direction = 0 # 0: right, 1: down, 2: left, 3: up
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.fruit = self.generate_fruit_position()
        self.running = True
        self.game_over = False
        

pygame.display.set_caption('Змейка')
    def generate_fruit_position(self):
        return random.randint(0, self.msize[0] - 1), random.randint(0, self.msize[1] - 1)

screen = pygame.display.set_mode(WindowSize)
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_d and self.direction != 2:
                        self.direction = 0
                    if event.key == pygame.K_s and self.direction != 3:
                        self.direction = 1
                    if event.key == pygame.K_a and self.direction != 0:
                        self.direction = 2
                    if event.key == pygame.K_w and self.direction != 1:
                        self.direction = 3
                else:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()

TSide = 30
MSize = WindowSize[0] // TSide, WindowSize[1] // TSide
    def reset_game(self):
        self.game_over = False
        self.snake = [self.start_pos]
        self.fruit = self.generate_fruit_position()
        self.fps = 5
        self.direction = 0
    
    def draw_snake(self):
        for x, y in self.snake:
            pygame.draw.rect(self.screen, "green", (x * self.tside, y * self.tside, self.tside - 1, self.tside - 1))
    
    def draw_fruit(self):
      pygame.draw.rect(self.screen, "blue", (self.fruit[0] * self.tside, self.fruit[1] * self.tside, self.tside - 1, self.tside - 1))

start_pos = MSize[0] // 2, MSize[1] // 2
snake = [start_pos]
z = True
direction = 0
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
fruit = random.randint(0, MSize[0] - 1), random.randint(0, MSize[1] - 1)
FPS = 5
clock = pygame.time.Clock()
pygame.font.init()
font_gameover = pygame.font.SysFont("Liberation Serif", 52)
run = True
while run:
    clock.tick(FPS)
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if z:
                if event.key == pygame.K_d and direction != 2:
                    direction = 0
                if event.key == pygame.K_s and direction != 3:
                    direction = 1
                if event.key == pygame.K_a and direction != 0:
                    direction = 2
                if event.key == pygame.K_w and direction != 1:
                    direction = 3
    def move_snake(self):
        new_pos = self.snake[0][0] + self.directions[self.direction][0], self.snake[0][1] + self.directions[self.direction][1]
        if not (0 <= new_pos[0] < self.msize[0] and 0 <= new_pos[1] < self.msize[1]) or new_pos in self.snake:
            self.game_over = True
        else:
            self.snake.insert(0, new_pos)
            if new_pos == self.fruit:
                self.fps += 1
                self.fruit = self.generate_fruit_position()
            else:
                if event.key == pygame.K_SPACE:
                    z = True
                    snake = [start_pos]
                    fruit = random.randint(0, MSize[0] - 1), random.randint(0, MSize[1] - 1)
                    FPS = 5
                        
                self.snake.pop(-1)

    [pygame.draw.rect(screen, "green", (x * TSide, y * TSide, TSide - 1, TSide - 1)) for x, y in snake]
    pygame.draw.rect(screen, "blue", (fruit[0] * TSide, fruit[1] * TSide, TSide - 1, TSide - 1))
    def draw_gameover_screen(self):
        text = self.font_gameover.render("SORRY, GAME OVER", True, "white")
        self.screen.blit(text, (self.window_size[0] // 2 - text.get_width() // 2, self.window_size[1] // 2 - 40))
    
    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.screen.fill("black")
            self.handle_input()

    if z:
        new_pos = snake[0][0] + directions[direction][0], snake[0][1] + directions[direction][1]
        if not (0 <= new_pos[0] < MSize[0] and 0 <= new_pos[1] < MSize[1]) or new_pos in snake:
            z = False
        else:
            snake.insert(0, new_pos)
            if new_pos == fruit:
                FPS += 1
                fruit = random.randint(0, MSize[0] - 1), random.randint(0, MSize[1] - 1)
            if not self.game_over:
              self.draw_snake()
              self.draw_fruit()
              self.move_snake()
            else:
                snake.pop(-1)
    else:
        text = font_gameover.render("SORRY, GAME OVER", True, "white")
        screen.blit(text, (WindowSize[0] // 2 - text.get_width() // 2, WindowSize[1] // 2 - 40))
                 
    pygame.display.flip()
              self.draw_gameover_screen()
              
            pygame.display.flip()
        pygame.quit()
