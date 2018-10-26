import random
import sys
import time
import numpy as np
import pygame
import pygame.gfxdraw
from gym_achtung.envs.achtungplayer import AchtungPlayer


from math import *
from pygame.locals import *

SPEED = 10       # frames per second setting
WINWIDTH = 452  # width of the program's window, in pixels
WINHEIGHT = 452  # height in pixels
RADIUS = 4       # radius of the circles
PLAYERS = 1      # number of players

BG_COLOR = (25, 25, 25)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
P1COLOUR = RED
P2COLOUR = GREEN
P3COLOUR = BLUE


def main():
    # main loop
    global FPS_CLOCK, SCREEN, DISPLAYSURF, MY_FONT
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('FarBy!')

    while True:
        rungame()
        gameover()

def rungame():
    iterating = True
    while iterating:
        SCREEN.fill(BG_COLOR)
        player = AchtungPlayer(WHITE, WINWIDTH, WINHEIGHT, RADIUS)
        run = True
        while run:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.angle -= 15
                if player.angle <= 0:
                    player.angle += 360
            if keys[pygame.K_RIGHT]:
                player.angle += 15
                if player.angle >= 360:
                    player.angle -= 360
            player.move()
            if collision(player.x,player.y):
                run = False
            player.draw(SCREEN)

def collision(x,y,skip=False):
    collide_check = False
    try:
        x_check = (x < 0) or \
                  (x > WINWIDTH)
        y_check = (y < 0) or \
                  (y > WINHEIGHT)

        collide_check = SCREEN.get_at((x, y)) != BG_COLOR
    except IndexError:
        x_check = (x < 0) or (x > WINWIDTH)
        y_check = (y < 0) or (y > WINHEIGHT)
    if skip:
        collide_check = False
    return any([x_check, y_check, collide_check])

if __name__ == '__main__':
    main()
