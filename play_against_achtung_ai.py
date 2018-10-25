import gym
import gym_achtung

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

def main():
    env = gym.make("AchtungDieKurveAgainstPlayer-v0")
    env = DummyVecEnv([lambda: env])

    model = DQN.load("04.pkl",env)

    obs = env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render()
if __name__ == '__main__':
    main()
