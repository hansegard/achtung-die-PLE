import gym
import gym_achtung

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

def main():
    env = gym.make("AchtungDieKurveBigGrid-v0")
    env = DummyVecEnv([lambda: env])

    model = DQN(MlpPolicy,env,render=False,buffer_size=25000,gamma=0.99,exploration_fraction=0.3,
    exploration_final_eps = 0.005,learning_rate=0.0005, verbose=1,learning_starts=1000)
    model.learn(total_timesteps=1000000,log_interval=1000)
    model.save("11")

if __name__ == '__main__':
    main()
