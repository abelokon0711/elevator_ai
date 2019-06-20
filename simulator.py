import argparse
import gym
from time import sleep

from gym.envs.registration import register, make
from numpy import loadtxt


def main(parse_args=True, episode_to_load=1, playback_speed_factor=10, end_episode=1):
    episodes = []
    if parse_args:
        parser = argparse.ArgumentParser(
            description='Replay training process.')
        parser.add_argument('episode', metavar='N', type=int,
                            help='episode to be replayed')
        parser.add_argument('--speed', type=float, default=1,
                            help='the multiplier of the simulation')
        parser.add_argument('--end_episode', type=int, default=1,
                            help='if given, episodes will be played consecutively up until end_episode')
        args = parser.parse_args()
        episode_to_load = args.episode
        playback_speed_factor = args.speed
        if args.end_episode is not None:
            end_episode = args.end_episode

    for i in range(episode_to_load, end_episode + 1):
        episodes.append(
            loadtxt(
                "./results/observations_episode_"
                + str(i)
                + ".txt", delimiter=','))

    env = gym.make('Elevator-v0')
    env.reset()
    for index, loaded_episode in enumerate(episodes):
        print('showing episode', index)
        for state in loaded_episode:
            env.state = state
            if not state[1:].any():
                continue
            print(state)
            env.render()
            sleep(1/playback_speed_factor)
    env.close()


# If started with `python3 simulator.py`
if __name__ == "__main__":
    register(
        id='Elevator-v0',
        entry_point='gym_environment:ElevatorEnv',
    )
    main(parse_args=True)
# If started from main.py
else:
    main(parse_args=False)
