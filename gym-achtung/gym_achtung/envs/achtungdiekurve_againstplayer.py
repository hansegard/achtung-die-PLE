from gym_achtung.envs.achtungdiekurve import AchtungDieKurve
from gym_achtung.envs.achtungplayer import AchtungDieKurvePlayer
import pygame

WINWIDTH = 1280  # width of the program's window, in pixels
WINHEIGHT = 576  # height in pixels

RADIUS = 2
GREEN = (0, 255, 0)

class AchtungDieKurveAgainstPlayer(AchtungDieKurve):
    def __init__(self):
        self.winwidth = WINWIDTH
        self.winheight = WINHEIGHT
        self.human_init()
        super().__init__()

    def human_init(self):
        self.humanplayer = AchtungPlayer(GREEN, self.winwidth, self.winheight, RADIUS)
        self.human_alive = True

    def _handle_human_player_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.humanplayer.angle -= 10
            if self.humanplayer.angle <= 0:
                self.humanplayer.angle += 360
        if keys[pygame.K_RIGHT]:
            self.humanplayer.angle += 10
            if self.humanplayer.angle >= 360:
                self.humanplayer.angle -= 360

    def __step(self, dt):
        """
            Perform one step of game emulation with human against AI
        """
        dt /= 1000.0

        self.ticks += 1
        self._handle_player_events()
        self.score += self.rewards["tick"]
        self.player.update()
        self.player.draw(self.screen)

        if self.human_alive:
            self._handle_human_player_events()
            self.humanplayer.update()
            self.player.draw(self.screen)
            if self.collision(self.humanplayer.x,self.humanplayer.y,self.humanplayer.skip):
                self.human_alive = False

        if self.collision(self.player.x,self.player.y,self.player.skip):
            self.lives = -1

        if self.lives <= 0.0:
            self.score += self.rewards["loss"]

    def reset(self):
        self.human_init()
        super().reset()
