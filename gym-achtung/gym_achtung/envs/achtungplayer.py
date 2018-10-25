import numpy as np
import random
import pygame
import pygame.gfxdraw

SKIP_PROBABILITY = 0.05

class AchtungPlayer:

    def __init__(self, color, win_width, win_height,body_radius=2):
        self.color = color
        self.radius = body_radius
        self.score = 0
        self.skip = False
        # generates random position and direction
        self.x = random.randrange(win_width - 3*win_width/4, win_width - win_width/4)
        self.y = random.randrange(win_height - 3*win_height/4, win_height - win_height/4)
        self.angle = random.randrange(0, 350, 10)

    def move(self):
        # computes current movement
        self.x += int(np.round(self.radius * 1.9 * np.cos(np.deg2rad(self.angle))))
        self.y += int(np.round(self.radius * 1.9 * np.sin(np.deg2rad(self.angle))))

    def draw(self, screen):
        if self.skip:
            self.skip = False
        elif np.random.rand() < SKIP_PROBABILITY:
            self.skip = True
        else:
            #pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
            pygame.gfxdraw.aacircle(screen, self.x, self.y, self.radius, self.color)
            pygame.gfxdraw.filled_circle(screen, self.x, self.y, self.radius, self.color)
    def update(self):
        self.move()
