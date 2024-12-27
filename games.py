import os
import pygame


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


class Window:
    def get_coord(self, mouse_pos):
        return mouse_pos[0], mouse_pos[1]

    
class Main(Window):
    def draw_window(self):
        screen.fill((153, 255, 153))
        
        pygame.draw.rect(screen, (255, 0, 0), (250, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        games = font.render('Игры', True, (255, 0, 0))
        screen.blit(games, (320, 280))
        
        pygame.draw.rect(screen, (255, 0, 0), (650, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        rules = font.render('Правила игр', True, (255, 0, 0))
        screen.blit(rules, (665, 280))
        
        pygame.display.flip()

    def open_new_window(self):
        global window
        if 250 < x < 500 and 250 < y < 350:
            window = Games()
            pygame.display.set_caption('Игры')
            window.draw_window()
        elif 650 < x < 900 and 250 < y < 350:
            window = Rules()
            pygame.display.set_caption('Правила игр')
            window.draw_window()


class Games(Window):
    def draw_window(self):
        screen.fill((153, 255, 153))
        
        pygame.draw.rect(screen, (255, 0, 0), (250, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        games = font.render('Бильярд', True, (255, 0, 0))
        screen.blit(games, (300, 280))

        all_sprites = pygame.sprite.Group()
        home = pygame.sprite.Sprite()
        home.image = pygame.transform.scale(load_image('home.png'), (50, 50))
        home.rect = home.image.get_rect()
        home.rect.x = 20
        home.rect.y = 20
        all_sprites.add(home)
        all_sprites.draw(screen)
        
        pygame.display.flip()

    def open_new_window(self):
        global window
        if 20 < x < 70 and 20 < y < 70:
            window = Main()
            pygame.display.set_caption('Главная')
            window.draw_window()
        elif 250 < x < 500 and 250 < y < 350:
            window = Billiard()
            pygame.display.set_caption('Бильярд')
            window.draw_window()


class Rules(Window):
    def draw_window(self):
        screen.fill((153, 255, 153))
        
        pygame.draw.rect(screen, (255, 0, 0), (250, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        games = font.render('Бильярд', True, (255, 0, 0))
        screen.blit(games, (300, 280))

        all_sprites = pygame.sprite.Group()
        home = pygame.sprite.Sprite()
        home.image = pygame.transform.scale(load_image('home.png'), (50, 50))
        home.rect = home.image.get_rect()
        home.rect.x = 20
        home.rect.y = 20
        all_sprites.add(home)
        all_sprites.draw(screen)
        
        pygame.display.flip()

    def open_new_window(self):
        global window
        if 20 < x < 70 and 20 < y < 70:
            window = Main()
            pygame.display.set_caption('Главная')
            window.draw_window()


class Billiard(Window):
    def draw_window(self):
        screen.fill((153, 255, 153))
        
        all_sprites = pygame.sprite.Group()
        
        home = pygame.sprite.Sprite()
        home.image = pygame.transform.scale(load_image('home.png'), (50, 50))
        home.rect = home.image.get_rect()
        home.rect.x = 20
        home.rect.y = 20
        all_sprites.add(home)

        arrow = pygame.sprite.Sprite()
        arrow.image = pygame.transform.scale(load_image('arrow.png'), (50, 50))
        arrow.rect = arrow.image.get_rect()
        arrow.rect.x = 20
        arrow.rect.y = 90
        all_sprites.add(arrow)

        billiard_table = pygame.sprite.Sprite()
        billiard_table.image = pygame.transform.scale(load_image('billiard_table.png'), (750, 450))
        billiard_table.rect = billiard_table.image.get_rect()
        billiard_table.rect.x = 200
        billiard_table.rect.y = 150
        all_sprites.add(billiard_table)
        
        all_sprites.draw(screen)
        
        pygame.display.flip()

    def open_new_window(self):
        global window
        if 20 < x < 70 and 20 < y < 70:
            window = Main()
            pygame.display.set_caption('Главная')
            window.draw_window()
        elif 20 < x < 70 and 90 < y < 140:
            window = Games()
            pygame.display.set_caption('Игры')
            window.draw_window()

    
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
                x, y = window.get_coord(event.pos)
                window.open_new_window()
    pygame.quit()
