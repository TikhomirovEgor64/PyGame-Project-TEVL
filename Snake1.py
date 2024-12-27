import pygame
import random

WindowSize = (720, 480)

pygame.display.set_caption('Змейка')

screen = pygame.display.set_mode(WindowSize)

TSide = 30
MSize = WindowSize[0] // TSide, WindowSize[1] // TSide

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
            else:
                if event.key == pygame.K_SPACE:
                    z = True
                    snake = [start_pos]
                    fruit = random.randint(0, MSize[0] - 1), random.randint(0, MSize[1] - 1)
                    FPS = 5
                        

    [pygame.draw.rect(screen, "green", (x * TSide, y * TSide, TSide - 1, TSide - 1)) for x, y in snake]
    pygame.draw.rect(screen, "blue", (fruit[0] * TSide, fruit[1] * TSide, TSide - 1, TSide - 1))

    if z:
        new_pos = snake[0][0] + directions[direction][0], snake[0][1] + directions[direction][1]
        if not (0 <= new_pos[0] < MSize[0] and 0 <= new_pos[1] < MSize[1]) or new_pos in snake:
            z = False
        else:
            snake.insert(0, new_pos)
            if new_pos == fruit:
                FPS += 1
                fruit = random.randint(0, MSize[0] - 1), random.randint(0, MSize[1] - 1)
            else:
                snake.pop(-1)
    else:
        text = font_gameover.render("SORRY, GAME OVER", True, "white")
        screen.blit(text, (WindowSize[0] // 2 - text.get_width() // 2, WindowSize[1] // 2 - 40))
                 
    pygame.display.flip()
