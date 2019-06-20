import numpy as np
import sys
import argparse
import pyglet
from pyglet import gl
import gym
from gym.envs.registration import registry, register, make, spec
from time import sleep


def main(parse_args=True, episode_to_load=0, playback_speed_factor=10):
    if parse_args:
        parser = argparse.ArgumentParser(description='Replay training process.')
        parser.add_argument('episode', metavar='N', type=int,
                            help='episode to be replayed')
        parser.add_argument('--speed', type=float, default=1,
                            help='the replay speed in ')
        args = parser.parse_args()
        episode_to_load = args.episode
        playback_speed_factor = args.speed

    loaded_episode = np.loadtxt("./results/observations_episode_" + str(episode_to_load) + ".txt", delimiter=',')

    #print(loaded_episode)
    env = gym.make('Elevator-v0')
    env.reset()
    for state in loaded_episode:
        env.state = state
        print(state)
        env.render()
        sleep(1/playback_speed_factor)
    env.close()

if __name__ == "__main__":
    register(
        id='Elevator-v0',
        entry_point='gym_environment:ElevatorEnv',
    )
    main(parse_args=True)
else:
    main(parse_args=False)