import gym
import gym_achtung
import time
import numpy as np

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

NOOFITERATIONS = 100

def main():
    env = gym.make("AchtungDieKurveSmallGrid-v0")
    env = DummyVecEnv([lambda: env])

    model = DQN.load("trained_agents/09.pkl",env)

    obs = env.reset()
    iteration = 0
    tick = 0
    scores = []
    max_score = 0
    while True:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        tick += 0.01
        if dones:
            iteration += 1
            scores.append(tick)
            if tick > max_score:
                max_score = tick
            print('Iteration: {}, Score: {}, Max score: {}'.format(iteration, tick,max_score))
            if iteration == NOOFITERATIONS:
                break
            tick = 0
        #env.render()
    print('Mean score over {} iterations: {}'.format(NOOFITERATIONS,np.mean(scores)))
if __name__ == '__main__':
    main()
