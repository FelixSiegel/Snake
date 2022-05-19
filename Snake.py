import pygame
from sys import exit
from random import randint
from time import time

# Game Settings
WIDTH = 600
HEIGHT = 400
TILESIZE = 10
FPS = 30
GAMEOVER = False
PAUSE = False

# Init Pygame
pygame.init()
pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# pygame.mouse.set_visible(False)

def debug(message, pos=(5, 5), color=(255, 255, 255), size=10, centered = False):
    """Function that render a given message to screen (usefull for debug ingame)"""
    font = pygame.font.SysFont("liberationserif", size)
    text = font.render(str(message), True, color)
    if centered:
        center = [WIDTH//2-text.get_width()//2, HEIGHT//2-text.get_height()//2]
        pos = center
    screen.blit(text, pos)

def new_apple():
    new_pos = (randint(0, WIDTH//TILESIZE-1)*TILESIZE, randint(0, HEIGHT//TILESIZE-1)*TILESIZE)
    while new_pos in snake[0]:
        new_pos = (randint(0, WIDTH)%TILESIZE, randint(0, HEIGHT)%TILESIZE)
    return new_pos

# Game Variables
INTERVAL = 0.6 # time wait until next locomotion
DIRECTIONS = {"DOWN": (0, TILESIZE),
              "UP":   (0, -TILESIZE),
              "LEFT": (-TILESIZE, 0),
              "RIGHT":(TILESIZE, 0)
              }
cur_direction, new_direction = "RIGHT", "RIGHT"
snake = [(130, 80), (120, 80), (110, 80)]
apple = new_apple()
eaten = False
level = 1

pRect = pygame.draw.rect # shortcut for Rectangle-function of PyGame

previousTime = time()

# Game Loop
while True:
    for event in pygame.event.get():  # cheking for events
        if event.type == pygame.QUIT:  # if the user close the Window
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and cur_direction != "RIGHT":
                new_direction = "LEFT"
            if event.key == pygame.K_RIGHT and cur_direction != "LEFT":
                new_direction = "RIGHT"
            if event.key == pygame.K_DOWN and cur_direction != "UP":
                new_direction = "DOWN"
            if event.key == pygame.K_UP and cur_direction != "DOWN":
                new_direction = "UP"

    if not GAMEOVER:
        if not PAUSE:
            # Clear all (fill black) at begin of draw
            screen.fill("black")
            # draw apple
            pRect(screen, (255, 0, 0), (apple[0], apple[1], TILESIZE, TILESIZE), border_radius=5)
            for e in snake: # draw snake
                pRect(screen, (0, 255, 0), (e[0], e[1], TILESIZE, TILESIZE), border_radius=2)

            # every 600ms -> Fortbewegung
            if time() - previousTime >= INTERVAL:
                # check if Snake eat the Apple
                if snake[0] == apple:
                    eaten = True

                if eaten:
                    apple = new_apple()
                    INTERVAL -= 0.05
                    level += 1

                cur_direction = new_direction
                snake.insert(0, (snake[0][0]+DIRECTIONS[cur_direction][0], \
                                snake[0][1]+DIRECTIONS[cur_direction][1]))
                # check for die
                if snake[0] in snake[1:] or \
                   snake[0][0]<0 or snake[0][0] >=WIDTH or \
                   snake[0][1]<0 or snake[0][1] >= HEIGHT:
                   GAMEOVER = True
                   debug("GAME OVER", color = (255, 0, 0), size=40, centered = True)
                if not eaten:
                    snake.pop() # letztes Element löschen

                eaten = False
                previousTime = time()

            debug(f"{round(clock.get_fps())} fps")
            debug(f"Level {level}", pos=(5, 20))

            pygame.display.update()
            clock.tick(FPS)
