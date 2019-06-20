import gym
import numpy
import os

from gym.envs.registration import registry, register, make, spec

register(
    id='Elevator-v0',
    entry_point='gym_environment:ElevatorEnv',
)

observationz = numpy.zeros((50, 1000, 61))

env = gym.make('Elevator-v0')
for i_episode in range(50):
    observation = env.reset()
    for t in range(1000):
        # env.render()
        observationz[i_episode][t] = numpy.copy(observation)
        action = env.action_space.sample()
        # print(action)
        observation, reward, done, info = env.step(action)
        print(observation[0])

        if done:
            print("Episode finished after {} timesteps".format(t + 1))
            break
env.close()

# Write observationz to file
for i in range(50):
    numpy.savetxt('results/observations_episode_' + str(i) + '.txt',
                  observationz[i], delimiter=',')
