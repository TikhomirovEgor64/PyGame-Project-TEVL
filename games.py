import os
import pygame


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


class Window:
    def get_cell(self, mouse_pos):
        return mouse_pos[0], mouse_pos[1]

    
class Main(Window):
    def draw_window(self):
        screen.fill((255, 216, 0))
        
        pygame.draw.rect(screen, (255, 0, 0), (250, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        games = font.render('Игры', True, (255, 0, 0))
        screen.blit(games, (320, 280))
        
        pygame.draw.rect(screen, (255, 0, 0), (650, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        rules = font.render('Правила игр', True, (255, 0, 0))
        screen.blit(rules, (665, 280))
        
        pygame.display.flip()


class Games(Window):
    def draw_window(self):
        screen.fill((216, 255, 0))
        
        pygame.draw.rect(screen, (255, 0, 0), (250, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        games = font.render('Игра 1', True, (255, 0, 0))
        screen.blit(games, (320, 280))
        
        pygame.draw.rect(screen, (255, 0, 0), (650, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        rules = font.render('Игра 2', True, (255, 0, 0))
        screen.blit(rules, (665, 280))

        all_sprites = pygame.sprite.Group()
        home = pygame.sprite.Sprite()
        home.image = pygame.transform.scale(load_image('home.png'), (50, 50))
        home.rect = home.image.get_rect()
        home.rect.x = 20
        home.rect.y = 20
        all_sprites.add(home)
        all_sprites.draw(screen)
        
        pygame.display.flip()


class Rules(Window):
    def draw_window(self):
        screen.fill((255, 166, 0))
        
        pygame.draw.rect(screen, (255, 0, 0), (250, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        games = font.render('Игра 1', True, (255, 0, 0))
        screen.blit(games, (320, 280))
        
        pygame.draw.rect(screen, (255, 0, 0), (650, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        rules = font.render('Игра 2', True, (255, 0, 0))
        screen.blit(rules, (665, 280))

        all_sprites = pygame.sprite.Group()
        home = pygame.sprite.Sprite()
        home.image = pygame.transform.scale(load_image('home.png'), (50, 50))
        home.rect = home.image.get_rect()
        home.rect.x = 20
        home.rect.y = 20
        all_sprites.add(home)
        all_sprites.draw(screen)
        
        pygame.display.flip()

    
if __name__ == '__main__':
    pygame.init()
    size = width, height = 1150, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Главная')
    pygame.display.flip()

    window = Main()
    window.draw_window()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = window.get_cell(event.pos)
                if 250 < x < 500 and 250 < y < 350 and isinstance(window, Main):
                    window = Games()
                    pygame.display.set_caption('Игры')
                    window.draw_window()
                if 650 < x < 900 and 250 < y < 350 and isinstance(window, Main):
                    window = Rules()
                    pygame.display.set_caption('Правила игр')
                    window.draw_window()
                if 20 < x < 70 and 20 < y < 70 and (isinstance(window, Games) or isinstance(window, Rules)):
                    window = Main()
                    pygame.display.set_caption('Главная')
                    window.draw_window()
    pygame.quit()
