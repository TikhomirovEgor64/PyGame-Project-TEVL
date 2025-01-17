import os
import pygame


ball_sprites = pygame.sprite.Group()
start_billiard = True






move_billiard_ball = False
billiard_coord = (0, 0)

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


class Ball(pygame.sprite.Sprite):
    def __init__(self, im, x, y, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image(im), (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flag = False
        self.mov = False
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.change_x = 0
        self.change_y = 0
        self.time = 0

    def update(self, *args):
        if args[0].type == pygame.MOUSEBUTTONDOWN and isinstance(window, Billiard) and self.rect.collidepoint(args[0].pos):
            self.x1, self.y1 = args[0].pos
            self.flag = True
        if args[0].type == pygame.MOUSEBUTTONUP and isinstance(window, Billiard) and self.flag:
            self.x2, self.y2 = args[0].pos
            self.mov = True
            self.time = 200
            self.flag = False
        if self.mov and self.time:
            vx = self.x2 - self.x1
            vy = self.y2 - self.y1
            v = (vx ** 2 + vy ** 2) ** 0.5
            new_x, new_y = -vx / v * 20, -vy / v * 20
            if (self.rect.x + new_x < 235 or self.rect.x + new_x > 895) and (self.rect.y + new_y < 190 or self.rect.y + new_y > 555):
                if self.change_x and self.change_y:
                    self.change_x = -self.change_x
                    self.change_y = -self.change_y
                else:
                    self.change_x = -new_x
                    self.change_y = -new_y
            elif self.rect.x + new_x < 235 or self.rect.x + new_x > 895:
                if self.change_x and self.change_y:
                    self.change_x = -self.change_x
                    self.change_y = self.change_y
                else:
                    self.change_x = -new_x
                    self.change_y = new_y
            elif self.rect.y + new_y < 190 or self.rect.y + new_y > 555:
                if self.change_x and self.change_y:
                    self.change_x = self.change_x
                    self.change_y = -self.change_y
                else:
                    self.change_x = new_x
                    self.change_y = -new_y
            else:
                if self.change_x and self.change_y:
                    self.change_x = self.change_x
                    self.change_y = self.change_y
                else:
                    self.change_x = new_x
                    self.change_y = new_y
            
            self.rect = self.rect.move(self.change_x, self.change_y)
            window.draw_window()

            self.time -= 1

            for i in ball_sprites:
                if pygame.sprite.collide_rect(i, self) and i != self:
                    print(i)
                    self.mov = False
                    i.mov = True
                    i.x1 = self.x1
                    i.x2 = self.x2
                    i.y1 = self.y1
                    i.y2 = self.y2
                    i.change_x = self.change_x
                    i.change_y = self.change_y
                    i.time = self.time

            if self.time == 0:
                for i in ball_sprites:
                    i.flag = False
                    i.mov = False
                    i.x1 = 0
                    i.y1 = 0
                    i.x2 = 0
                    i.y2 = 0
                    i.change_x = 0
                    i.change_y = 0
                    i.time = 0

        
class Billiard(Window):
    def draw_window(self):
        global start_billiard
        
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

        global ball_sprites

        images = ['red_ball.png', 'white_ball.png', 'white_ball.png', 'white_ball.png',
                  'white_ball.png', 'white_ball.png', 'white_ball.png', 'white_ball.png',
                  'white_ball.png', 'white_ball.png', 'white_ball.png', 'white_ball.png',
                  'white_ball.png', 'white_ball.png', 'white_ball.png', 'white_ball.png']

        if start_billiard:
            x = [385, 665, 691, 691,
                 717, 717, 717, 743,
                 743, 743, 743, 769,
                 769, 769, 769, 769]

            y = [360, 360, 346, 373,
                 334, 360, 386, 320,
                 346, 373, 399, 308,
                 334, 360, 386, 412]

            for i in range(16):
                ball = Ball(images[i], x[i], y[i], ball_sprites)
            start_billiard = False
        
        
        all_sprites.draw(screen)
        ball_sprites.draw(screen)
        
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

    fps = 10000000000000000000
    clock = pygame.time.Clock()

    window = Main()
    window.draw_window()
    
    running = True
    while running:
        for event in pygame.event.get():
            ball_sprites.update(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = window.get_coord(event.pos)
                window.open_new_window()
                print(event.pos)
        clock.tick(fps)
    pygame.quit()
