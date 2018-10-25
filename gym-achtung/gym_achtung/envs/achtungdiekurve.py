import pygame
import sys
import time

from gym import spaces
import gym
from pygame.constants import KEYDOWN, KEYUP, K_F15
from pygame.constants import K_w, K_a, K_s, K_d
import numpy as np
from gym_achtung.envs.achtungplayer import AchtungPlayer

RADIUS = 4      # radius of the circles
NOOFBEAMS = 9 # must be un-even!

WHITE = (255, 255, 255)
BG_COLOR = (25, 25, 25)

class AchtungDieKurve(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}
    """
    Parameters
    ----------
    width : int
        Screen width.

    height : int
        Screen height, recommended to be same dimension as width.


    """

    def __init__(self,fps=30, frame_skip=1, num_steps=1,
                 force_fps=True, add_noop_action=True, rng=24):

        self.actions = {
            "left": K_a,
            "right": K_d,
        }

        self.score = 0.0  # required.
        self.lives = 0  # required. Can be 0 or -1 if not required.
        self.ticks = 0
        self.previous_score = 0
        self.frame_count = 0
        self.fps = fps
        self.frame_skip = frame_skip
        self.num_steps = num_steps
        self.force_fps = force_fps
        self.viewer = None
        self.add_noop_action = add_noop_action
        self.last_action = []
        self.action = []
        self.screen_dim = (self.winwidth, self.winheight)  # width and height
        self.allowed_fps = None  # fps that the game is allowed to run at.
        self.NOOP = K_F15  # the noop key
        self.rng = None
        self._action_set = self.getActions()
        self.action_space = spaces.Discrete(len(self._action_set))
        self.observation_space = spaces.Box(low=0,high=1024,shape=(3+NOOFBEAMS,))

        self.rewards = {    # TODO: take as input
                    "positive": 1.0,
                    "negative": -1.0,
                    "tick": 0.01,
                    "loss": 0,
                    "win": 5.0
                }

        self._setup()
        self.init()

    def _setup(self):
        """
        Setups up the pygame env, the display and game clock.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.getScreenDims())
        self.clock = pygame.time.Clock()

    def getActions(self):
        """
        Gets the actions the game supports. Optionally inserts the NOOP
        action if PLE has add_noop_action set to True.

        Returns
        --------

        list of pygame.constants
            The agent can simply select the index of the action
            to perform.

        """
        actions = self.actions
        if isinstance(actions, dict):
            actions = actions.values()

        actions = list(actions)

        if self.add_noop_action:
            actions.append(self.NOOP)

        return actions

    def _handle_player_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if key == self.actions["left"]:
                    self.player.angle -= 10
                    if self.player.angle <= 0:
                        self.player.angle += 360

                if key == self.actions["right"]:
                    self.player.angle += 10
                    if self.player.angle >= 360:
                        self.player.angle -= 360

    def setAction(self, action, last_action):
        """
        Pushes the action to the pygame event queue.
        """
        if action is None:
            action = self.NOOP

        if last_action is None:
            last_action = self.NOOP

        kd = pygame.event.Event(KEYDOWN, {"key": action})
        ku = pygame.event.Event(KEYUP, {"key": last_action})

        pygame.event.post(kd)
        pygame.event.post(ku)

    def _setAction(self, action):
        """
            Instructs the game to perform an action if its not a NOOP
        """

        if action is not None:
            self.setAction(action, self.last_action)

        self.last_action = action

    def act(self, action):
        """
        Perform an action on the game. We lockstep frames with actions.
        If act is not called the game will not run.

        Parameters
        ----------

        action : int
            The index of the action we wish to perform. The index usually
            corresponds to the index item returned by getActionSet().

        Returns
        -------

        int
            Returns the reward that the agent has accumlated while performing the action.

        """
        return sum(self._oneStepAct(action) for i in range(self.frame_skip))

    def _oneStepAct(self, action):
        """
        Performs an action on the game. Checks if the game is over
        or if the provided action is valid based on the allowed action set.
        """

        if self.game_over():
            return 0.0

        if action not in self.getActions():
            action = self.NOOP

        self._setAction(action)
        for i in range(self.num_steps):
            time_elapsed = self._tick()
            self._step(time_elapsed)

        self.frame_count += self.num_steps

        return self._getReward()

    def _getReward(self):
        """
        Returns the reward the agent has gained as the difference between the last action and the current one.
        """
        reward = self.getScore() - self.previous_score
        self.previous_score = self.getScore()

        return reward

    def getFrameNumber(self):
        """
        Gets the current number of frames the agent has seen
        since PLE was initialized.

        Returns
        --------

        int

        """

        return self.frame_count

    def _tick(self):
        """
        Calculates the elapsed time between frames or ticks.
        """
        if self.force_fps:
            return 1000.0 / self.fps
        else:
            return self.tick(self.fps)

    def tick(self, fps):
        """
        This sleeps the game to ensure it runs at the desired fps.
        """
        return self.clock.tick_busy_loop(fps)

    def adjustRewards(self, rewards):
        """

        Adjusts the rewards the game gives the agent

        Parameters
        ----------
        rewards : dict
            A dictonary of reward events to float rewards. Only updates if key
            matches those specificed in the init function.

        """
        for key in rewards.keys():
            if key in self.rewards:
                self.rewards[key] = rewards[key]

    def getGameState(self):
        """

        Returns
        -------

        dict
            * x position.
            * y position.

            See code for structure.
        """
        state = np.array([self.player.x/self.winwidth, self.player.y/self.winheight, self.player.angle])
        return np.append(state,self.get_beam())

    def get_beam(self):
        beam = []
        looking_angle = -90
        angle_stepsize = 180/(NOOFBEAMS-1)
        for beam_direction in range(NOOFBEAMS):
            angle = self.player.angle + looking_angle
            ping = False
            step = RADIUS
            while not ping:
                step += 1
                x_pos = int(np.round(self.player.x + step*np.cos(np.deg2rad(angle))))
                y_pos = int(np.round(self.player.y + step*np.sin(np.deg2rad(angle))))
                if self.collision(x_pos,y_pos):
                    beam.append(np.sqrt((x_pos - self.player.x)**2
                     + (y_pos - self.player.y)**2))
                    ping = True
            looking_angle += angle_stepsize
        return np.array(beam)

    def getScreenDims(self):
        """
        Gets the screen dimensions of the game in tuple form.

        Returns
        -------
        tuple of int
            Returns tuple as follows (width, height).

        """
        return self.screen_dim

    def getScore(self):
        return self.score

    def game_over(self):
        return self.lives == -1

    def setRNG(self, rng):
        """
        Sets the rng for games.
        """

        if self.rng is None:
            self.rng = rng

    def init(self):
        """
            Starts/Resets the game to its inital state
        """
        self.player = AchtungPlayer(WHITE, self.winwidth, self.winheight, RADIUS)
        self.screen.fill(BG_COLOR)
        self.score = 0
        self.ticks = 0
        self.lives = 1

    def collision(self,x,y,skip=False):
        collide_check = False
        try:
            x_check = (x < 0) or \
                      (x > self.winwidth)
            y_check = (y < 0) or \
                      (y > self.winheight)

            collide_check = self.screen.get_at((x, y)) != BG_COLOR
        except IndexError:
            x_check = (x < 0) or (x > self.winwidth)
            y_check = (y < 0) or (y > self.winheight)
        if skip:
            collide_check = False
        return any([x_check, y_check, collide_check])

    def _step(self, dt):
        """
            Perform one step of game emulation.
        """
        dt /= 1000.0

        self.ticks += 1
        self._handle_player_events()
        self.score += self.rewards["tick"]
        self.player.update()

        if self.collision(self.player.x,self.player.y,self.player.skip):
            self.lives = -1

        if self.lives <= 0.0:
            self.score += self.rewards["loss"]

        self.player.draw(self.screen)

    def step(self, a):
        reward = self.act(self._action_set[a])
        state = self.getGameState()
        terminal = self.game_over()
        return state, reward, terminal, {}

    def reset(self):
        self.last_action = []
        self.action = []
        self.previous_score = 0.0
        self.init()
        state = self.getGameState()
        return state

    def render(self, mode='human', close=False):
        pygame.display.update()

    def seed(self, seed):
        rng = np.random.RandomState(seed)
        self.rng = rng
        self.init()
