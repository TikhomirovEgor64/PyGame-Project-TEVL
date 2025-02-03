import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 1150, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
FPS = 30
INITIAL_SPEED = 7  # Начальная скорость шарика
MAX_SPEED = 20     # Максимальная скорость шарика

class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.geekRect = pygame.Rect(posx, posy, width, height)

    def display(self):
        pygame.draw.rect(screen, self.color, self.geekRect)

    def update(self, yFac):
        self.posy += self.speed * yFac

        if self.posy <= 0:
            self.posy = 0
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height

        self.geekRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        font = pygame.font.Font(None, 36)
        text = font.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        screen.blit(text, textRect)

    def getRect(self):
        return self.geekRect

class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.firstTime = 1

    def display(self):
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.xFac *= -1
        self.firstTime = 1
        self.speed = INITIAL_SPEED  # Сброс скорости на начальную

    def hit(self):
        self.xFac *= -1
        # Увеличиваем скорость шарика при столкновении с ракеткой
        self.speed += 1
        if self.speed > MAX_SPEED:
            self.speed = MAX_SPEED

    def getRect(self):
        return pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)

def main():
    running = True

    geek1 = Striker(20, HEIGHT // 2 - 50, 10, 100, 10, (139, 0, 255))
    geek2 = Striker(WIDTH - 30, HEIGHT // 2 - 50, 10, 100, 10, (139, 0, 255))
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, INITIAL_SPEED, (255, 0, 0))

    listOfGeeks = [geek1, geek2]

    geek1Score, geek2Score = 0, 0
    geek1YFac, geek2YFac = 0, 0

    while running:
        screen.fill((153, 255, 153))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    geek2YFac = -1
                if event.key == pygame.K_DOWN:
                    geek2YFac = 1
                if event.key == pygame.K_w:
                    geek1YFac = -1
                if event.key == pygame.K_s:
                    geek1YFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    geek2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    geek1YFac = 0

        for geek in listOfGeeks:
            if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                ball.hit()

        geek1.update(geek1YFac)
        geek2.update(geek2YFac)
        point = ball.update()

        if point == -1:
            geek1Score += 1
            ball.reset()  # Сброс шарика и его скорости
        elif point == 1:
            geek2Score += 1
            ball.reset()  # Сброс шарика и его скорости

        geek1.display()
        geek2.display()
        ball.display()

        geek1.displayScore("Geek_1: ", geek1Score, 100, 20, BLACK)
        geek2.displayScore("Geek_2: ", geek2Score, WIDTH - 100, 20, BLACK)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
    pygame.quit()
