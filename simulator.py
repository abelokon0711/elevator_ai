import numpy as np
import sys
import argparse
import pyglet
from pyglet import gl
import gym
from gym.envs.registration import registry, register, make, spec
from time import sleep

register(
    id='Elevator-v0',
    entry_point='gym_environment:ElevatorEnv',
)

parser = argparse.ArgumentParser(description='Replay training process.')
parser.add_argument('episode', metavar='N', type=int,
                    help='episode to be replayed')
parser.add_argument('--speed', type=float, default=1,
                    help='the replay speed in ')

args = parser.parse_args()
loaded_episode = np.loadtxt("./results/observations_episode_" + str(args.episode) + ".txt", delimiter=',')

#print(loaded_episode)
env = gym.make('Elevator-v0')
env.reset()
for state in loaded_episode:
    env.state = state
    print(state)
    env.render()
    sleep(args.speed)
env.close()


