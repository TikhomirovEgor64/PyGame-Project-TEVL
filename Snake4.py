import pygame
import random

class SnakeGame:
    def __init__(self, window_size=(1150, 700), tside=30, fps=5):
        pygame.init()
        self.window_size = window_size
        self.tside = tside
        self.msize = (window_size[0] // tside, window_size[1] // tside)
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption('Змейка для двух игроков')
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.font_gameover = pygame.font.SysFont("Liberation Serif", 52)
        self.start_pos1 = (self.msize[0] // 4, self.msize[1] // 2)  # Позиция для первого игрока
        self.start_pos2 = (self.msize[0] * 3 // 4, self.msize[1] // 2)  # Позиция для второго игрока
        self.snake1 = [self.start_pos1]
        self.snake2 = [self.start_pos2]
        self.direction1 = 0
        self.direction2 = 0
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.fruit = self.generate_fruit_position()
        self.running = True
        self.game_over = False

    def generate_fruit_position(self):
        return random.randint(0, self.msize[0] - 1), random.randint(0, self.msize[1] - 1)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if not self.game_over:
                    # Управление первым игроком (A, W, S, D)
                    if event.key == pygame.K_d and self.direction1 != 2:
                        self.direction1 = 0
                    if event.key == pygame.K_s and self.direction1 != 3:
                        self.direction1 = 1
                    if event.key == pygame.K_a and self.direction1 != 0:
                        self.direction1 = 2
                    if event.key == pygame.K_w and self.direction1 != 1:
                        self.direction1 = 3

                    # Управление вторым игроком (стрелки)
                    if event.key == pygame.K_RIGHT and self.direction2 != 2:
                        self.direction2 = 0
                    if event.key == pygame.K_DOWN and self.direction2 != 3:
                        self.direction2 = 1
                    if event.key == pygame.K_LEFT and self.direction2 != 0:
                        self.direction2 = 2
                    if event.key == pygame.K_UP and self.direction2 != 1:
                        self.direction2 = 3
                else:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake1 = [self.start_pos1]
        self.snake2 = [self.start_pos2]
        self.fruit = self.generate_fruit_position()
        self.fps = 5
        self.direction1 = 0
        self.direction2 = 0

    def draw_snake(self):
        for x, y in self.snake1:
            pygame.draw.rect(self.screen, "purple", (x * self.tside, y * self.tside, self.tside - 1, self.tside - 1))
        for x, y in self.snake2:
            pygame.draw.rect(self.screen, "red", (x * self.tside, y * self.tside, self.tside - 1, self.tside - 1))

    def draw_fruit(self):
        pygame.draw.rect(self.screen, "blue", (self.fruit[0] * self.tside, self.fruit[1] * self.tside, self.tside - 1, self.tside - 1))

    def move_snake(self):
        # Движение первого игрока
        new_pos1 = self.snake1[0][0] + self.directions[self.direction1][0], self.snake1[0][1] + self.directions[self.direction1][1]
        if not (0 <= new_pos1[0] < self.msize[0] and 0 <= new_pos1[1] < self.msize[1]) or new_pos1 in self.snake1 or new_pos1 in self.snake2:
            self.game_over = True
        else:
            self.snake1.insert(0, new_pos1)
            if new_pos1 == self.fruit:
                self.fps += 1
                self.fruit = self.generate_fruit_position()
            else:
                self.snake1.pop(-1)

        # Движение второго игрока
        new_pos2 = self.snake2[0][0] + self.directions[self.direction2][0], self.snake2[0][1] + self.directions[self.direction2][1]
        if not (0 <= new_pos2[0] < self.msize[0] and 0 <= new_pos2[1] < self.msize[1]) or new_pos2 in self.snake2 or new_pos2 in self.snake1:
            self.game_over = True
        else:
            self.snake2.insert(0, new_pos2)
            if new_pos2 == self.fruit:
                self.fps += 1
                self.fruit = self.generate_fruit_position()
            else:
                self.snake2.pop(-1)

    def draw_gameover_screen(self):
        text = self.font_gameover.render("SORRY, GAME OVER", True, "white")
        self.screen.blit(text, (self.window_size[0] // 2 - text.get_width() // 2, self.window_size[1] // 2 - 40))

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.screen.fill((153, 255, 153))
            self.handle_input()

            if not self.game_over:
                self.draw_snake()
                self.draw_fruit()
                self.move_snake()
            else:
                self.draw_gameover_screen()

            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
