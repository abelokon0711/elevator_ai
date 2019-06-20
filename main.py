import gym
import os
from time import sleep

import numpy
from gym.envs.registration import registry, register, make, spec

TRAIN_AGENT = True
ENABLE_GRAPHICS = True
EPISODES = 500
STEPS_PER_EPISODE = 1000
DIMENSIONS = 61

register(
    id='Elevator-v0',
    entry_point='gym_environment:ElevatorEnv',
)

observationz = numpy.zeros((EPISODES, STEPS_PER_EPISODE, DIMENSIONS))

if TRAIN_AGENT:
    """Training the agent"""
    print('Training started')
    env = gym.make('Elevator-v0')
    for i_episode in range(EPISODES):
        observation = env.reset()
        for t in range(STEPS_PER_EPISODE):
            observationz[i_episode][t] = numpy.copy(observation)
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)

            if done:
                break
        print("Episode {} of {} finished after {} timesteps".format(i_episode, EPISODES, t + 1))
    env.close()

    print("Training finished.\n")

    print("Writing states to files")
    for i in range(EPISODES):
        numpy.savetxt('results/observations_episode_' + str(i) + '.txt',
                    observationz[i], delimiter=',')
    print("Saved data")

if ENABLE_GRAPHICS:
    """Visualize episode zero"""
    import simulator