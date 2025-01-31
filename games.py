import os
import pygame
from math import sin, cos, radians


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


help_sprites = pygame.sprite.Group()

home = pygame.sprite.Sprite()
home.image = pygame.transform.scale(load_image('home.png'), (50, 50))
home.rect = home.image.get_rect()
home.rect.x = 20
home.rect.y = 20
help_sprites.add(home)

arrow = pygame.sprite.Sprite()
arrow.image = pygame.transform.scale(load_image('arrow.png'), (50, 50))
arrow.rect = arrow.image.get_rect()
arrow.rect.x = 20
arrow.rect.y = 90
help_sprites.add(arrow)

billiard_sprites = pygame.sprite.Group()
        
ball_sprites = pygame.sprite.Group()


class Windows:
    def get_coord(self, mouse_pos):
        return mouse_pos[0], mouse_pos[1]


class Main(Windows):
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

        self.running = True


    def run(self):
        global running
        global window
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = window.get_coord(event.pos)
                    if 250 < x < 500 and 250 < y < 350:
                        window = Games()
                        pygame.display.set_caption('Игры')
                        window.draw_window()
                        self.running = False
                        break
                    elif 650 < x < 900 and 250 < y < 350:
                        window = Rules()
                        pygame.display.set_caption('Правила игр')
                        window.draw_window()
                        self.running = False
                        break


class Games(Windows):
    def draw_window(self):
        screen.fill((153, 255, 153))
        
        pygame.draw.rect(screen, (255, 0, 0), (250, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        games = font.render('Бильярд', True, (255, 0, 0))
        screen.blit(games, (300, 280))

        pygame.draw.rect(screen, (255, 0, 0), (650, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        games = font.render('Змейка', True, (255, 0, 0))
        screen.blit(games, (700, 280))

        pygame.draw.rect(screen, (255, 0, 0), (250, 50, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        games = font.render('Танчики', True, (255, 0, 0))
        screen.blit(games, (300, 80))

        all_sprites = pygame.sprite.Group()
        home = pygame.sprite.Sprite()
        home.image = pygame.transform.scale(load_image('home.png'), (50, 50))
        home.rect = home.image.get_rect()
        home.rect.x = 20
        home.rect.y = 20
        all_sprites.add(home)
        all_sprites.draw(screen)
        
        pygame.display.flip()

        self.running = True

    def run(self):
        global running
        global window
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = window.get_coord(event.pos)
                    if 20 < x < 70 and 20 < y < 70:
                        window = Main()
                        pygame.display.set_caption('Главная')
                        window.draw_window()
                        self.running = False
                    elif 250 < x < 500 and 250 < y < 350:
                        window = Billiard()
                        pygame.display.set_caption('Бильярд')
                        window.draw_window()
                        self.running = False
                    elif 250 < x < 500 and 50 < y < 150:
                        window = Tanks()
                        pygame.display.set_caption('Танчики')
                        window.draw_window()
                        self.running = False
                    



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

            screen.fill((153, 255, 153))
            
            help_sprites.draw(screen)
            billiard_sprites.draw(screen)
            ball_sprites.draw(screen)

            pygame.display.flip()
            

            self.time -= 1

            for i in ball_sprites:
                if pygame.sprite.collide_rect(i, self) and i != self:
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

        
class Billiard(Windows):
    def draw_window(self):
        global billiard_sprites
        global ball_sprites
        self.running = True
        
        screen.fill((153, 255, 153))

        billiard_sprites = pygame.sprite.Group()
        
        billiard_table = pygame.sprite.Sprite()
        billiard_table.image = pygame.transform.scale(load_image('billiard_table.png'), (750, 450))
        billiard_table.rect = billiard_table.image.get_rect()
        billiard_table.rect.x = 200
        billiard_table.rect.y = 150
        billiard_sprites.add(billiard_table)


        images = ['red_ball.png', 'white_ball.png', 'white_ball.png', 'white_ball.png',
                  'white_ball.png', 'white_ball.png', 'white_ball.png', 'white_ball.png',
                  'white_ball.png', 'white_ball.png', 'white_ball.png', 'white_ball.png',
                  'white_ball.png', 'white_ball.png', 'white_ball.png', 'white_ball.png']

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
        
        help_sprites.draw(screen)
        billiard_sprites.draw(screen)
        ball_sprites.draw(screen)
        
        pygame.display.flip()

    def run(self):
        global running
        global window
        while self.running:
            for event in pygame.event.get():
                ball_sprites.update(event)
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = window.get_coord(event.pos)
                    if 20 < x < 70 and 20 < y < 70:
                        window = Main()
                        pygame.display.set_caption('Главная')
                        window.draw_window()
                        self.running = False
                    elif 20 < x < 70 and 90 < y < 140:
                        window = Games()
                        pygame.display.set_caption('Игры')
                        window.draw_window()
                        self.running = False


class SpritesTankGame(pygame.sprite.Sprite):
    def __init__(self, im, x, y, all_sprites, size, tank=0, cor=0, flag=False):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image(im), size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tank = tank
        self.cor = cor
        self.flag = flag


class BulletsSprites(SpritesTankGame):
    def update(self, *args):
        if self.cor // 90 % 4 == 0:
            self.rect.x += 5
        elif self.cor // 90 % 4 == 1:
            self.rect.y += 5
        elif self.cor // 90 % 4 == 2:
            self.rect.x -= 5
        elif self.cor // 90 % 4 == 3:
            self.rect.y -= 5

        if pygame.sprite.spritecollide(self, window.strong_bloks, dokill=False) or\
           self.rect.x < 175 or self.rect.x > 965 or self.rect.y < 50 or self.rect.y > 640:
            self.kill()

        if pygame.sprite.spritecollide(self, window.weak_bloks, dokill=False):
            for i in pygame.sprite.spritecollide(self, window.weak_bloks, dokill=False):
                i.kill()
            self.kill()
            
        self_rect = pygame.Rect(self.rect.x, self.rect.y, 10, 10)
        tank1 = pygame.Rect(window.tank_map.tank1.rect.x, window.tank_map.tank1.rect.y, 25, 25)
        tank2 = pygame.Rect(window.tank_map.tank2.rect.x, window.tank_map.tank2.rect.y, 25, 25)

        if self_rect.colliderect(tank2) and self.tank == 1:
            x, y = window.tank_map.tank2.rect.x, window.tank_map.tank2.rect.y
            self.kill()
            window.tank_map.tank2.kill()
            
            boom_sprite = pygame.sprite.Group()
            block = SpritesTankGame('boom.png', x - 12, y - 12, boom_sprite, (50, 50))
            
            window.update_window()
            boom_sprite.draw(screen)
            pygame.display.flip()

            pygame.time.delay(2000)

            window.score1 += 1
            
            window.tank_map = TankMap1()
            window.strong_bloks = window.tank_map.strong_bloks_sprites
            window.weak_bloks = window.tank_map.weak_bloks_sprites
            window.tanks = window.tank_map.tanks_sprites

            window.first_x = window.tank_map.first_x
            window.first_y = window.tank_map.first_y
            window.second_x = window.tank_map.second_x
            window.second_y = window.tank_map.second_y

            window.cor1 = 0
            window.cor2 = 180

            window.timer1 = 0
            window.timer2 = 0

            window.running = True

        if self_rect.colliderect(tank1) and self.tank == 2:
            x, y = window.tank_map.tank1.rect.x, window.tank_map.tank1.rect.y
            self.kill()
            window.tank_map.tank1.kill()

            boom_sprite = pygame.sprite.Group()
            block = SpritesTankGame('boom.png', x - 12, y - 12, boom_sprite, (50, 50))
            
            window.update_window()
            boom_sprite.draw(screen)
            pygame.display.flip()

            pygame.time.delay(1500)

            window.score2 += 1
            
            window.tank_map = TankMap1()
            window.strong_bloks = window.tank_map.strong_bloks_sprites
            window.weak_bloks = window.tank_map.weak_bloks_sprites
            window.tanks = window.tank_map.tanks_sprites

            window.first_x = window.tank_map.first_x
            window.first_y = window.tank_map.first_y
            window.second_x = window.tank_map.second_x
            window.second_y = window.tank_map.second_y

            window.cor1 = 0
            window.cor2 = 180

            window.timer1 = 0
            window.timer2 = 0

            window.running = True

        window.update_window()


class TanksSprites(SpritesTankGame):
    def update(self, *args):
        if args[0].type == pygame.KEYDOWN:
            if args[0].key == pygame.K_v:
                window.tank_map.tank1.flag = True
            if args[0].key == pygame.K_c:
                window.cor1 -= 45
                window.tank_map.tank1.image = pygame.transform.rotate(window.tank_map.tank1.image, window.cor1 * 2)
            if args[0].key == pygame.K_b:
                window.cor1 += 45
                window.tank_map.tank1.image = pygame.transform.rotate(window.tank_map.tank1.image, window.cor1 * 2)
            if args[0].key == pygame.K_UP:
                window.tank_map.tank2.flag = True
            if args[0].key == pygame.K_LEFT:
                window.cor2 -= 45
                window.tank_map.tank2.image = pygame.transform.rotate(window.tank_map.tank2.image, window.cor2 * 2)
            if args[0].key == pygame.K_RIGHT:
                window.cor2 += 45
                window.tank_map.tank2.image = pygame.transform.rotate(window.tank_map.tank2.image, window.cor2 * 2)
        if args[0].type == pygame.KEYUP:
            window.tank_map.tank1.flag = False
            window.tank_map.tank2.flag = False
        window.update_window()
                    
        
class TankMap1():
    def __init__(self):
        self.strong_bloks_sprites = pygame.sprite.Group()

        x = [350, 375, 400,
             450, 475, 500,
             550, 575, 600,
             650, 675, 700,
             750, 775, 800,
             500, 500, 500,
             550, 550, 550,
             600, 600, 600,
             650, 650, 650]

        y = [100, 125, 150,
             200, 225, 250,
             300, 325, 350,
             400, 425, 450,
             500, 525, 550,
             350, 375, 400,
             150, 175, 200,
             450, 475, 500,
             250, 275, 300]

        for i in range(27):
            block = SpritesTankGame('blok1.webp', x[i], y[i], self.strong_bloks_sprites, (25, 25))

        self.weak_bloks_sprites = pygame.sprite.Group()

        x = [300, 300, 300, 325,
             425, 425, 425,
             525, 525, 525,
             625, 625, 625,
             725, 725, 725,
             825, 850, 850, 850, 850]

        y = [50, 75, 100, 100,
             150, 175, 200,
             250, 275, 300,
             350, 375, 400,
             450, 475, 500,
             550, 550, 575, 600, 625]
        

        for i in range(21):
            block = SpritesTankGame('blok2.webp', x[i], y[i], self.weak_bloks_sprites, (25, 25))

        self.tanks_sprites = pygame.sprite.Group()
        self.tank1 = TanksSprites('tank1.png', 300, 475, self.tanks_sprites, (25, 25))
        self.tank2 = TanksSprites('tank2.png', 850, 175, self.tanks_sprites, (25, 25))

        self.first_x = 300
        self.first_y = 475
        self.second_x = 850
        self.second_y = 175

        self.bullets_sprites = pygame.sprite.Group()


class Tanks(Windows):
    def update_window(self):
        screen.fill((153, 255, 153))
        pygame.draw.rect(screen, (255, 204, 0), (175, 50, 800, 600), 0)
        
        help_sprites.draw(screen)
        window.strong_bloks.draw(screen)
        window.weak_bloks.draw(screen)
        window.tanks.draw(screen)
        window.tank_map.bullets_sprites.draw(screen)

        pygame.draw.rect(screen, (255, 0, 0), (35, 270, 90, 70), 2)
        font = pygame.font.Font(None, 70)
        games = font.render(str(window.score1), True, (255, 0, 0))
        screen.blit(games, (45, 280))

        pygame.draw.rect(screen, (255, 0, 0), (1000, 270, 90, 70), 2)
        font = pygame.font.Font(None, 70)
        games = font.render(str(window.score2), True, (255, 0, 0))
        screen.blit(games, (1010, 280))

        pygame.draw.rect(screen, (255, 0, 0), (400, 10, 150, 35), 2)
        font = pygame.font.Font(None, 40)
        games = font.render(str(window.time / 100), True, (255, 0, 0))
        screen.blit(games, (410, 15))

        font = pygame.font.Font(None, 40)
        games = font.render('sec', True, (255, 0, 0))
        screen.blit(games, (500, 15))
        
        pygame.display.flip()
        
    def draw_window(self):
        self.score1 = 0
        self.score2 = 0

        self.tank_map = TankMap1()
        self.strong_bloks = self.tank_map.strong_bloks_sprites
        self.weak_bloks = self.tank_map.weak_bloks_sprites
        self.tanks = self.tank_map.tanks_sprites
        

        self.first_x = self.tank_map.first_x
        self.first_y = self.tank_map.first_y
        self.second_x = self.tank_map.second_x
        self.second_y = self.tank_map.second_y

        self.cor1 = 0
        self.cor2 = 180

        self.timer1 = 0
        self.timer2 = 0

        self.time = 12000

        self.running = True

        self.update_window()

    def tanks_moving(self):
        clock.tick(60)
        if window.tank_map.tank1.flag:
            window.tank_map.tank1.rect.x = window.first_x + cos(radians(window.cor1)) * 5
            window.tank_map.tank1.rect.y = window.first_y + sin(radians(window.cor1)) * 5

            if pygame.sprite.spritecollide(window.tank_map.tank1, window.strong_bloks, dokill=False) or\
                pygame.sprite.spritecollide(window.tank_map.tank1, window.weak_bloks, dokill=False) or\
                window.tank_map.tank1.rect.x < 175 or window.tank_map.tank1.rect.x > 950 or\
                window.tank_map.tank1.rect.y < 50 or window.tank_map.tank1.rect.y > 625:
                window.tank_map.tank1.rect.x = window.first_x
                window.tank_map.tank1.rect.y = window.first_y
            else:
                window.first_x += cos(radians(window.cor1)) * 5
                window.first_y += sin(radians(window.cor1)) * 5
            
        if window.tank_map.tank2.flag:
            window.tank_map.tank2.rect.x = window.second_x + cos(radians(window.cor2)) * 5
            window.tank_map.tank2.rect.y = window.second_y + sin(radians(window.cor2)) * 5

            if pygame.sprite.spritecollide(window.tank_map.tank2, window.strong_bloks, dokill=False) or\
                pygame.sprite.spritecollide(window.tank_map.tank2, window.weak_bloks, dokill=False) or\
                window.tank_map.tank2.rect.x < 175 or window.tank_map.tank2.rect.x > 950 or\
                window.tank_map.tank2.rect.y < 50 or window.tank_map.tank2.rect.y > 625:
                window.tank_map.tank2.rect.x = window.second_x
                window.tank_map.tank2.rect.y = window.second_y
            else:
                window.second_x += cos(radians(window.cor2)) * 5
                window.second_y += sin(radians(window.cor2)) * 5
        window.update_window()

    def run(self):
        global running
        global window
        while self.running:
            self.time -= 1
            if self.tank_map.bullets_sprites:
                self.tank_map.bullets_sprites.update()
            self.tanks_moving()
            for event in pygame.event.get():
                self.tanks.update(event)
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = window.get_coord(event.pos) 
                    print(x, y)
                    if 20 < x < 70 and 20 < y < 70:
                        window = Main()
                        pygame.display.set_caption('Главная')
                        window.draw_window()
                        self.running = False
                    elif 20 < x < 70 and 90 < y < 140:
                        window = Games()
                        pygame.display.set_caption('Игры')
                        window.draw_window()
                        self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.timer1 <= 0:
                            if window.cor1 // 90 % 4 == 0:
                                bullet = BulletsSprites('red_ball.png', window.tank_map.tank1.rect.x + 30, window.tank_map.tank1.rect.y + 10, self.tank_map.bullets_sprites, (10, 10), tank=1, cor=window.cor1)
                            elif window.cor1 // 90 % 4 == 1:
                                bullet = BulletsSprites('red_ball.png', window.tank_map.tank1.rect.x + 10, window.tank_map.tank1.rect.y + 30, self.tank_map.bullets_sprites, (10, 10), tank=1, cor=window.cor1)
                            elif window.cor1 // 90 % 4 == 2:
                                bullet = BulletsSprites('red_ball.png', window.tank_map.tank1.rect.x - 5, window.tank_map.tank1.rect.y + 10, self.tank_map.bullets_sprites, (10, 10), tank=1, cor=window.cor1)
                            elif window.cor1 // 90 % 4 == 3:
                                bullet = BulletsSprites('red_ball.png', window.tank_map.tank1.rect.x + 10, window.tank_map.tank1.rect.y - 15, self.tank_map.bullets_sprites, (10, 10), tank=1, cor=window.cor1)

                            window.update_window()

                            self.timer1 = 5
                    if event.key == pygame.K_DOWN:
                        if self.timer2 <= 0:
                            if window.cor2 // 90 % 4 == 0:
                                bullet = BulletsSprites('red_ball.png', window.tank_map.tank2.rect.x + 30, window.tank_map.tank2.rect.y + 10, self.tank_map.bullets_sprites, (10, 10), tank=2, cor=window.cor2)
                            elif window.cor2 // 90 % 4 == 1:
                                bullet = BulletsSprites('red_ball.png', window.tank_map.tank2.rect.x + 10, window.tank_map.tank2.rect.y + 30, self.tank_map.bullets_sprites, (10, 10), tank=2, cor=window.cor2)
                            elif window.cor2 // 90 % 4 == 2:
                                bullet = BulletsSprites('red_ball.png', window.tank_map.tank2.rect.x - 5, window.tank_map.tank2.rect.y + 10, self.tank_map.bullets_sprites, (10, 10), tank=2, cor=window.cor2)
                            elif window.cor2 // 90 % 4 == 3:
                                bullet = BulletsSprites('red_ball.png', window.tank_map.tank2.rect.x + 10, window.tank_map.tank2.rect.y - 15, self.tank_map.bullets_sprites, (10, 10), tank=2, cor=window.cor2)

                            window.update_window()

                            self.timer2 = 5
            self.timer1 -= 1
            self.timer2 -= 1
            if self.time == 0:
                pygame.time.delay(2000)
                window = Main()
                pygame.display.set_caption('Главная')
                window.draw_window()
                self.running = False
                        
                    

class Rules(Windows):
    def draw_window(self):
        screen.fill((153, 255, 153))
        
        pygame.draw.rect(screen, (255, 0, 0), (250, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        games = font.render('Бильярд', True, (255, 0, 0))
        screen.blit(games, (300, 280))

        pygame.draw.rect(screen, (255, 0, 0), (650, 250, 250, 100), 2)
        font = pygame.font.Font(None, 50)
        games = font.render('Змейка', True, (255, 0, 0))
        screen.blit(games, (700, 280))

        all_sprites = pygame.sprite.Group()
        home = pygame.sprite.Sprite()
        home.image = pygame.transform.scale(load_image('home.png'), (50, 50))
        home.rect = home.image.get_rect()
        home.rect.x = 20
        home.rect.y = 20
        all_sprites.add(home)
        all_sprites.draw(screen)
        
        pygame.display.flip()

        self.running = True

    def run(self):
        global running
        global window
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = window.get_coord(event.pos)
                    if 20 < x < 70 and 20 < y < 70:
                        window = Main()
                        pygame.display.set_caption('Главная')
                        window.draw_window()
                        self.running = False
                    elif 250 < x < 500 and 250 < y < 350:
                        window = Billiard()
                        pygame.display.set_caption('Бильярд')
                        window.draw_window()
                        self.running = False
                        

if __name__ == '__main__':
    pygame.init()
    size = width, height = 1150, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Главная')
    pygame.display.flip()

    clock = pygame.time.Clock()

    window = Main()
    window.draw_window()
    
    running = True
    while running:
        window.run()
    pygame.quit()
