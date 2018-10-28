import gym
import gym_achtung
import os

import numpy as np
import time
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

NOOFITERATIONS = 50

def main():

    human_score_prev = 0
    env = gym.make("AchtungDieKurveHumanPlayer-v0")
    env = DummyVecEnv([lambda: env])

    model = DQN.load("trained_agents/11.pkl",env)

    obs = env.reset()
    action, _states = model.predict(obs)
    iteration = 0
    tick = 0
    scores = []
    max_score = 0

    while True:
        obs, rewards, dones, score = env.step(action)
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
        env.render()
    print('Mean score over {} iterations: {}'.format(NOOFITERATIONS,np.mean(scores)))
def print_score(score):
    os.system('cls' if os.name == 'nt' else 'clear')
    str = "AI Score: {} Human Score: {}"
    print(str.format(score[0],score[1]))
    if score[0] >= winning_score:
        print('The AI won!')
        return True
    elif score[1] >= winning_score:
        print('You won!')
        return True
    time.sleep(0.5)
    return False
if __name__ == '__main__':
    main()
