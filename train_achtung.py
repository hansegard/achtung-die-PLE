import gym
import gym_achtung

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

def main():
    env = gym.make("AchtungDieKurveSmallGrid-v0")
    env = DummyVecEnv([lambda: env])

    model = DQN(MlpPolicy,env,gamma=0.99,exploration_fraction=0.1,learning_rate=0.001, verbose=1)
    model.learn(total_timesteps=90000,log_interval=10)
    model.save("03")

if __name__ == '__main__':
    main()
