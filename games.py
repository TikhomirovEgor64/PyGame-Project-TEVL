import os
import pygame
from math import sin, cos, radians
from random import choice, randint


def load_image(name):
    fullname = os.path.join('images', name)
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
                    elif 250 < x < 500 and 50 < y < 150:
                        window = Tanks()
                        pygame.display.set_caption('Танчики')
                        window.draw_window()
                        self.running = False
                        

class SpritesTankGame(pygame.sprite.Sprite):
    def __init__(self, im, x, y, all_sprites, size, tank=0, cor=0, flag=False, possib1=0, possib2=0):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image(im), size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tank = tank
        self.cor = cor
        self.flag = flag
        self.possib1 = possib1
        self.possib2 = possib2


class BulletsSprites(SpritesTankGame):
    def update(self, *args):
        if self.cor // 90 % 4 == 0:
            self.rect.x += 10
        elif self.cor // 90 % 4 == 1:
            self.rect.y += 10
        elif self.cor // 90 % 4 == 2:
            self.rect.x -= 10
        elif self.cor // 90 % 4 == 3:
            self.rect.y -= 10

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

        if self_rect.colliderect(tank2) and self.tank == 1 and not window.defence2:
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
            
            window.new_part()

        if self_rect.colliderect(tank1) and self.tank == 2 and not window.defence1:
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

            window.new_part()

        window.update_window()


class SpecialBullets(SpritesTankGame):
    def update(self, *args):
        if self.cor // 90 % 4 == 0:
            self.rect.x += 10
        elif self.cor // 90 % 4 == 1:
            self.rect.y += 10
        elif self.cor // 90 % 4 == 2:
            self.rect.x -= 10
        elif self.cor // 90 % 4 == 3:
            self.rect.y -= 10

        if pygame.sprite.spritecollide(self, window.strong_bloks, dokill=False) or\
           pygame.sprite.spritecollide(self, window.weak_bloks, dokill=False) or\
           self.rect.x < 175 or self.rect.x > 965 or self.rect.y < 50 or self.rect.y > 640:
            self.kill()

        for i in pygame.sprite.spritecollide(self, window.weak_bloks, dokill=False):
            i.kill()

        for i in pygame.sprite.spritecollide(self, window.strong_bloks, dokill=False):
            i.kill()
            
        self_rect = pygame.Rect(self.rect.x, self.rect.y, 25, 50)
        tank1 = pygame.Rect(window.tank_map.tank1.rect.x, window.tank_map.tank1.rect.y, 25, 25)
        tank2 = pygame.Rect(window.tank_map.tank2.rect.x, window.tank_map.tank2.rect.y, 25, 25)

        if self_rect.colliderect(tank2) and self.tank == 1:
            if window.defence2:
                window.score1 += 1
            else:
                window.score1 += 2

            window.defence2 = False
            
            x, y = window.tank_map.tank2.rect.x, window.tank_map.tank2.rect.y
            self.kill()
            window.tank_map.tank2.kill()
            
            boom_sprite = pygame.sprite.Group()
            block = SpritesTankGame('boom.png', x - 12, y - 12, boom_sprite, (50, 50))
            
            window.update_window()
            boom_sprite.draw(screen)
            pygame.display.flip()

            pygame.time.delay(2000)
            
            window.new_part()

        if self_rect.colliderect(tank1) and self.tank == 2:
            if window.defence1:
                window.score2 += 1
            else:
                window.score2 += 2

            window.defence1 = False
            
            x, y = window.tank_map.tank1.rect.x, window.tank_map.tank1.rect.y
            self.kill()
            window.tank_map.tank1.kill()

            boom_sprite = pygame.sprite.Group()
            block = SpritesTankGame('boom.png', x - 12, y - 12, boom_sprite, (50, 50))
            
            window.update_window()
            boom_sprite.draw(screen)
            pygame.display.flip()

            pygame.time.delay(1500)
            
            window.new_part()

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


class Blue_Star(SpritesTankGame):
    pass


class Red_Star(SpritesTankGame):
    pass
                    
        
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
        self.tank1 = TanksSprites('tank1.png', 300, 475, self.tanks_sprites, (25, 25), possib1=0, possib2=0)
        self.tank2 = TanksSprites('tank2.png', 850, 175, self.tanks_sprites, (25, 25), possib1=0, possib2=0)

        self.first_x = 300
        self.first_y = 475
        self.second_x = 850
        self.second_y = 175

        self.bullets_sprites = pygame.sprite.Group()


class Tanks(Windows):
    def new_part(self):
        possib11 = window.tank_map.tank1.possib1
        possib12 = window.tank_map.tank1.possib2
        possib21 = window.tank_map.tank2.possib1
        possib22 = window.tank_map.tank2.possib2
            
        window.tank_map = TankMap1()
        window.strong_bloks = window.tank_map.strong_bloks_sprites
        window.weak_bloks = window.tank_map.weak_bloks_sprites
        window.tanks = window.tank_map.tanks_sprites

        window.tank_map.tank1.possib1 = possib11
        window.tank_map.tank1.possib2 = possib12
        window.tank_map.tank2.possib1 = possib21
        window.tank_map.tank2.possib2 = possib22

        window.first_x = window.tank_map.first_x
        window.first_y = window.tank_map.first_y
        window.second_x = window.tank_map.second_x
        window.second_y = window.tank_map.second_y

        window.cor1 = 0
        window.cor2 = 180

        window.timer1 = 0
        window.timer2 = 0
            
    def update_window(self):
        screen.fill((153, 255, 153))
        pygame.draw.rect(screen, (255, 204, 0), (175, 50, 800, 600), 0)
        
        help_sprites.draw(screen)
        window.strong_bloks.draw(screen)
        window.weak_bloks.draw(screen)

        if window.defence1:
            pygame.draw.circle(screen, (0, 0, 255), (window.tank_map.tank1.rect.x + 12, window.tank_map.tank1.rect.y + 12), 20, 2)

        if window.defence2:
            pygame.draw.circle(screen, (0, 0, 255), (window.tank_map.tank2.rect.x + 12, window.tank_map.tank2.rect.y + 12), 20, 2)

        window.tanks.draw(screen)
        window.tank_map.bullets_sprites.draw(screen)

        window.blue_stars.draw(screen)
        window.red_stars.draw(screen)

        pygame.draw.rect(screen, (255, 0, 0), (35, 270, 90, 70), 2)
        font = pygame.font.Font(None, 70)
        games = font.render(str(window.score1), True, (255, 0, 0))
        screen.blit(games, (45, 280))

        pygame.draw.rect(screen, (255, 0, 0), (1000, 270, 90, 70), 2)
        font = pygame.font.Font(None, 70)
        games = font.render(str(window.score2), True, (255, 0, 0))
        screen.blit(games, (1010, 280))

        pygame.draw.rect(screen, (255, 0, 0), (400, 10, 100, 35), 2)
        font = pygame.font.Font(None, 40)
        games = font.render(str(window.time / 100), True, (255, 0, 0))
        screen.blit(games, (410, 15))
        
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

        self.blue_stars = pygame.sprite.Group()
        self.red_stars = pygame.sprite.Group()

        self.stars_class = {'blue_star.png': (Blue_Star, self.blue_stars), 'red_star.png': (Red_Star, self.red_stars)}

        self.defence1 = False
        self.defence2 = False
        
        self.cor1 = 0
        self.cor2 = 180

        self.timer1 = 0
        self.timer2 = 0

        self.time = 12000

        self.running = True

        self.update_window()

    def check_stars(self, tank):
        for i in window.blue_stars:
            star = pygame.Rect(i.rect.x, i.rect.y, 25, 25)
            if self.self_rect.colliderect(star):
                i.kill()
                tank.possib1 += 150
        for i in window.red_stars:
            star = pygame.Rect(i.rect.x, i.rect.y, 25, 25)
            if self.self_rect.colliderect(star):
                i.kill()
                tank.possib2 += 1

    def draw_defence(self):
        if window.tank_map.tank1.possib1 and window.defence1:
            window.tank_map.tank1.possib1 -= 1
            if window.tank_map.tank1.possib1 == 0:
                window.defence1 = False
            self.update_window()
        if window.tank_map.tank2.possib1 and window.defence2:
            window.tank_map.tank2.possib1 -= 1
            if window.tank_map.tank2.possib1 == 0:
                window.defence2 = False
            self.update_window()

    def tanks_moving(self):
        clock.tick(30)
        gr1 = pygame.sprite.Group()
        gr2 = pygame.sprite.Group()
        gr1.add(window.tank_map.tank1)
        gr2.add(window.tank_map.tank2)
        if window.tank_map.tank1.flag:
            window.tank_map.tank1.rect.x = window.first_x + cos(radians(window.cor1)) * 5
            window.tank_map.tank1.rect.y = window.first_y + sin(radians(window.cor1)) * 5

            if pygame.sprite.spritecollide(window.tank_map.tank1, window.strong_bloks, dokill=False) or\
                pygame.sprite.spritecollide(window.tank_map.tank1, window.weak_bloks, dokill=False) or\
                pygame.sprite.spritecollide(window.tank_map.tank1, gr2, dokill=False) or\
                window.tank_map.tank1.rect.x < 175 or window.tank_map.tank1.rect.x > 950 or\
                window.tank_map.tank1.rect.y < 50 or window.tank_map.tank1.rect.y > 625:
                window.tank_map.tank1.rect.x = window.first_x
                window.tank_map.tank1.rect.y = window.first_y
            else:
                window.first_x += cos(radians(window.cor1)) * 5
                window.first_y += sin(radians(window.cor1)) * 5

            self.self_rect = pygame.Rect(window.tank_map.tank1.rect.x, window.tank_map.tank1.rect.y, 25, 25)
            self.check_stars(window.tank_map.tank1)
            
        if window.tank_map.tank2.flag:
            window.tank_map.tank2.rect.x = window.second_x + cos(radians(window.cor2)) * 5
            window.tank_map.tank2.rect.y = window.second_y + sin(radians(window.cor2)) * 5

            if pygame.sprite.spritecollide(window.tank_map.tank2, window.strong_bloks, dokill=False) or\
                pygame.sprite.spritecollide(window.tank_map.tank2, window.weak_bloks, dokill=False) or\
                pygame.sprite.spritecollide(window.tank_map.tank2, gr1, dokill=False) or\
                window.tank_map.tank2.rect.x < 175 or window.tank_map.tank2.rect.x > 950 or\
                window.tank_map.tank2.rect.y < 50 or window.tank_map.tank2.rect.y > 625:
                window.tank_map.tank2.rect.x = window.second_x
                window.tank_map.tank2.rect.y = window.second_y
            else:
                window.second_x += cos(radians(window.cor2)) * 5
                window.second_y += sin(radians(window.cor2)) * 5

            self.self_rect = pygame.Rect(window.tank_map.tank2.rect.x, window.tank_map.tank2.rect.y, 25, 25)
            self.check_stars(window.tank_map.tank2)
        window.update_window()

    def run(self):
        global running
        global window
        while self.running:
            self.time -= 1
            if self.time % 200 == 0 and self.time != 0:
                file = choice(['blue_star.png', 'red_star.png'])
                star_sprite = self.stars_class[file][0](file, randint(175, 950), randint(50, 625), self.stars_class[file][1], (25, 25))
                window.update_window()
            self.tank_map.bullets_sprites.update()
            self.blue_stars.update()
            self.red_stars.update()
            self.tanks_moving()
            self.draw_defence()
            for event in pygame.event.get():
                self.tanks.update(event)
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False
                    pygame.time.delay(1)
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
                    if event.key == pygame.K_1:
                        if self.timer1 <= 0 and window.tank_map.tank1.possib2 > 0:
                            if window.cor1 // 90 % 4 == 0:
                                bullet = SpecialBullets('special_bullet1.png', window.tank_map.tank1.rect.x + 30, window.tank_map.tank1.rect.y - 12, self.tank_map.bullets_sprites, (25, 50), cor=window.cor1, tank=1)
                            elif window.cor1 // 90 % 4 == 1:
                                bullet = SpecialBullets('special_bullet2.png', window.tank_map.tank1.rect.x - 12, window.tank_map.tank1.rect.y + 30, self.tank_map.bullets_sprites, (50, 25), cor=window.cor1, tank=1)
                            elif window.cor1 // 90 % 4 == 2:
                                bullet = SpecialBullets('special_bullet3.png', window.tank_map.tank1.rect.x - 5, window.tank_map.tank1.rect.y - 12, self.tank_map.bullets_sprites, (25, 50), cor=window.cor1, tank=1)
                            elif window.cor1 // 90 % 4 == 3:
                                bullet = SpecialBullets('special_bullet4.png', window.tank_map.tank1.rect.x - 12, window.tank_map.tank1.rect.y - 15, self.tank_map.bullets_sprites, (50, 25), cor=window.cor1, tank=1)
                            window.tank_map.tank1.possib2 -= 1
                            window.update_window()
                    if event.key == pygame.K_0:
                        if self.timer2 <= 0 and window.tank_map.tank2.possib2 > 0:
                            if window.cor2 // 90 % 4 == 0:
                                bullet = SpecialBullets('special_bullet1.png', window.tank_map.tank2.rect.x + 30, window.tank_map.tank2.rect.y - 12, self.tank_map.bullets_sprites, (25, 50), cor=window.cor2, tank=2)
                            elif window.cor2 // 90 % 4 == 1:
                                bullet = SpecialBullets('special_bullet2.png', window.tank_map.tank2.rect.x - 12, window.tank_map.tank2.rect.y + 30, self.tank_map.bullets_sprites, (50, 25), cor=window.cor2, tank=2)
                            elif window.cor2 // 90 % 4 == 2:
                                bullet = SpecialBullets('special_bullet3.png', window.tank_map.tank2.rect.x - 5, window.tank_map.tank2.rect.y - 12, self.tank_map.bullets_sprites, (25, 50), cor=window.cor2, tank=2)
                            elif window.cor2 // 90 % 4 == 3:
                                bullet = SpecialBullets('special_bullet4.png', window.tank_map.tank2.rect.x -12, window.tank_map.tank2.rect.y - 15, self.tank_map.bullets_sprites, (50, 25), cor=window.cor2, tank=2)
                            window.tank_map.tank2.possib2 -= 1
                            window.update_window()
                    if event.key == pygame.K_2 and window.tank_map.tank1.possib1:
                        self.defence1 = True
                    if event.key == pygame.K_3:
                        self.defence1 = False
                    if event.key == pygame.K_9 and window.tank_map.tank2.possib1:
                        self.defence2 = True
                    if event.key == pygame.K_8:
                        self.defence2 = False
                        
                            
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
        games = font.render('Танчики', True, (255, 0, 0))
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
                        window = Tanks()
                        pygame.display.set_caption('Танчики')
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
