from gym_achtung.envs.achtungdiekurve import AchtungDieKurve
from gym_achtung.envs.achtungplayer import AchtungPlayer
import pygame
import numpy as np
import time

WINWIDTH = 452  # width of the program's window, in pixels
WINHEIGHT = 452  # height in pixels

RADIUS = 4
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BG_COLOR = (25, 25, 25)

class AchtungDieKurveHumanPlayer(AchtungDieKurve):
    def __init__(self):
        self.winwidth = WINWIDTH
        self.winheight = WINHEIGHT
        self.aiscore = 0
        self.humanscore = 0
        self.aiwon = False
        self.human_init()
        super().__init__()

    def _setup(self):
        """
        Setups up the pygame env, the display and game clock.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.getScreenDims())
        pygame.display.set_caption('Achtung AI AI score: {} Human score: {}'.format(self.aiscore,self.humanscore))
        self.clock = pygame.time.Clock()

    def human_init(self):
        self.humanplayer = AchtungPlayer(GREEN, self.winwidth, self.winheight, RADIUS)

    def init(self):
        """
            Starts/Resets the game to its inital state
        """
        self.player = AchtungPlayer(WHITE, self.winwidth, self.winheight, RADIUS)
        self.screen.fill(BG_COLOR)
        self.score = 0
        self.ticks = 0
        self.lives = 1

    def _handle_human_player_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.humanplayer.angle -= 15
            if self.humanplayer.angle <= 0:
                self.humanplayer.angle += 360
        if keys[pygame.K_RIGHT]:
            self.humanplayer.angle += 15
            if self.humanplayer.angle >= 360:
                self.humanplayer.angle -= 360

    def _step(self,dt):
        dt /= 1000.0
        time.sleep(0.02)
        self._handle_human_player_events()
        self.humanscore += self.rewards["tick"]
        self.humanplayer.update()
        if self.collision(self.humanplayer.x,self.humanplayer.y,self.humanplayer.skip):
            self.lives = -1
            self.aiwon = True
        self.humanplayer.draw(self.screen)
        self.ticks += 1

        self._handle_player_events()
        self.score += self.rewards["tick"]
        self.player.update()

        if self.collision(self.player.x,self.player.y,self.player.skip):
            pass
            #self.lives = -1

        if self.lives <= 0.0:
            self.score += self.rewards["loss"]

        #self.player.draw(self.screen)

    def step(self, a):
        reward = self.act(self._action_set[a])
        state = self.getGameState()
        terminal = self.game_over()
        return state, reward, terminal, {}

    def ai_won(self):
        self.aiwon = True
        self.aiscore += 1
        self.reset()

    def reset(self):
        print(self.humanscore)
        self.humanscore = 0
        self.human_init()
        self.aiwon = False
        super().reset()
