import gym
import gym_achtung
import os

import time
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

def main():

    ai_score_prev = 0
    human_score_prev = 0
    global winning_score
    startup = True
    wehaveawinner = False
    os.system('cls' if os.name == 'nt' else 'clear')
    winning_score = int(input('Win at how many points? '))

    env = gym.make("AchtungDieKurveAgainstPlayer-v0")
    env = DummyVecEnv([lambda: env])

    model = DQN.load("trained_agents/09.pkl",env)

    obs = env.reset()
    os.system('cls' if os.name == 'nt' else 'clear')
    while not wehaveawinner:
        action, _states = model.predict(obs)
        obs, rewards, dones, score = env.step(action)
        score = score[0]
        if startup:
            print('Game starting, get ready!')
            time.sleep(3)
            print_score(score)
            startup = False
        if score[0] > ai_score_prev or score[1] > human_score_prev:
            wehaveawinner = print_score(score)
            ai_score_prev, human_score_prev = score
            time.sleep(30)
        env.render()
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
