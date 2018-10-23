import logging
import os, sys
import numpy as np
import gym
from gym.wrappers import Monitor
from agentStuff import DQNAgent
import matplotlib.pyplot as plt

import gym_achtung


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    env = gym.make('AchtungDieKurve-v1' if len(sys.argv)<2 else sys.argv[1])


    # Initializations
    num_actions = env.action_space.n
    obs_dim     = env.observation_space.shape[0] * env.observation_space.shape[1] * 3

    # Choose agent. Choose wisely.
    agent = DQNAgent(state_size=obs_dim, action_size=num_actions)


    outdir = '/Users/erikbohnsack/Code/achtung-die-PLE/tmp'
    env = Monitor(env, directory=outdir, force=True)
    env.seed(0)

    episode_count = 10000
    reward = 0
    done = False

    fitnessValues = np.zeros(episode_count)

    for i in range(episode_count):
        state = env.reset()
        state = np.reshape(state, [1, obs_dim])

        fitness = 0

        while True:
            env.render()

            # Decide action
            action = agent.act(state)

            # Take action
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, obs_dim])
            fitness += reward

            # Remember the previous state, action, reward, and done
            agent.remember(state, action, reward, next_state, done)

            # make next_state the new current state for the next frame.
            state = next_state

            if done:
                # print the score and break out of the loop
                print("episode: {}/{}, reward: {}".format(i, episode_count, fitness))
                fitnessValues[i] = fitness
                break
            # train the agent with the experience of the episode
        agent.replay(8)

    plt.plot(fitnessValues)
    plt.ylabel('Fitness')
    plt.xlabel('Epoch')
    plt.show()

    # Dump result info to disk
    env.close()

    logger.info("Successfully ran training")

