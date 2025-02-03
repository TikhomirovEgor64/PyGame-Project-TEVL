import pygame
import sys

class Cell:
    def __init__(self):
        self.symbol = None

class Board:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.cells = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]

    def reset(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.cells[row][col].symbol = None

    def check_win(self, row, col):
        symbol = self.cells[row][col].symbol
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Направления: вертикально, горизонтально, по диагонали

        for d in directions:
            count = 1  # Учитываем текущий символ

            # Проверка в одном направлении
            r, c = row, col
            while 0 <= r + d[0] < self.grid_size and 0 <= c + d[1] < self.grid_size and self.cells[r + d[0]][c + d[1]].symbol == symbol:
                count += 1
                r += d[0]
                c += d[1]

            # Проверка в противоположном направлении
            r, c = row, col
            while 0 <= r - d[0] < self.grid_size and 0 <= c - d[1] < self.grid_size and self.cells[r - d[0]][c - d[1]].symbol == symbol:
                count += 1
                r -= d[0]
                c -= d[1]

            if count >= 5:  # Проверяем, есть ли 5 в ряд
                return True
        return False

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 800
        self.grid_size = 15
        self.cell_size = self.width // self.grid_size
        self.line_width = 15

        # Цвета
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Крестики-нолики 5 в ряд")

        self.board = Board(self.grid_size)
        self.current_player = "X"

    def draw_board(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, self.black, (x, 0), (x, self.height), self.line_width)
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, self.black, (0, y), (self.width, y), self.line_width)

    def draw_symbols(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.board.cells[row][col].symbol == "X":
                    pygame.draw.circle(self.screen, self.red, (col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2), self.cell_size // 2 - self.line_width)
                elif self.board.cells[row][col].symbol == "O":
                    # Рисуем крестик
                    start_pos1 = (col * self.cell_size + self.line_width, row * self.cell_size + self.line_width)
                    end_pos1 = (col * self.cell_size + self.cell_size - self.line_width, row * self.cell_size + self.cell_size - self.line_width)
                    start_pos2 = (col * self.cell_size + self.cell_size - self.line_width, row * self.cell_size + self.line_width)
                    end_pos2 = (col * self.cell_size + self.line_width, row * self.cell_size + self.cell_size - self.line_width)
                    pygame.draw.line(self.screen, self.blue, start_pos1, end_pos1, self.line_width)
                    pygame.draw.line(self.screen, self.blue, start_pos2, end_pos2, self.line_width)

    def run(self):
        while True:
            self.screen.fill((153, 255, 153))
            self.draw_board()
            self.draw_symbols()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    col = mouse_x // self.cell_size
                    row = mouse_y // self.cell_size

                    if self.board.cells[row][col].symbol is None:
                        self.board.cells[row][col].symbol = self.current_player

                        if self.board.check_win(row, col):
                            font = pygame.font.SysFont(None, 55)
                            text = font.render(f"Игрок {self.current_player} проиграл!", True, "white")
                            self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 40))
                            pygame.display.flip()
                            pygame.time.delay(2000)  # Задержка перед сбросом игры
                            self.board.reset()
                        else:
                            self.current_player = "O" if self.current_player == "X" else "X"

            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
