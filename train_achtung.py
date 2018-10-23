import gym
import gym_achtung

from baselines import deepq


def main():
    env = gym.make("AchtungDieKurve-v1")
    act = deepq.learn(
        env,
        network='mlp',
        lr=1e-3,
        total_timesteps=100000,
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
        print_freq=10
    )
if __name__ == '__main__':
    main()
