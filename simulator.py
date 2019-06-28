import argparse
import gym
from time import sleep

from gym.envs.registration import register, make
from numpy import loadtxt


def main(parse_args=True, episode_to_load=1, playback_speed_factor=10, end_episode=1):
    episodes = []
    actions = []
    rewards = []
    if parse_args:
        parser = argparse.ArgumentParser(
            description='Replay training process.')
        parser.add_argument('folder', metavar='N', type=str,
                        help='Folder to check for episodes')
        parser.add_argument('episode', metavar='N', type=int,
                            help='episode to be replayed')
        parser.add_argument('--speed', type=float, default=1,
                            help='the multiplier of the simulation')
        parser.add_argument('--end_episode', type=int, default=1,
                            help='if given, episodes will be played consecutively up until end_episode')
        args = parser.parse_args()
        episode_to_load = args.episode
        playback_speed_factor = args.speed
        execution_folder = args.folder
        if args.end_episode is not None:
            end_episode = args.end_episode

    for i in range(episode_to_load, end_episode + 1):
        path_observations = "results/"+ execution_folder+"/observations_episode_"+ str(i) + ".txt"
        episodes.append(loadtxt(path_observations, delimiter=','))

        path_actions = "results/"+ execution_folder+"/actions_episode_"+ str(i) + ".txt"
        actions.append(loadtxt(path_actions, delimiter=','))

        path_rewards = "results/"+ execution_folder+"/rewards_episode_"+ str(i) + ".txt"
        rewards.append(loadtxt(path_rewards, delimiter=','))

    env = gym.make('Elevator-v0')
    env.elevator_num = 2
    env.reset()
    for index, loaded_episode in enumerate(episodes):
        print('Episode', index)
        for i in range(0, len(loaded_episode)):
            env.state = loaded_episode[i]
            print("Step", i)
            print("Action:",actions[index][i],"Reward:",rewards[index][i])
            print(env.state)
            if not loaded_episode[i][1:].any():
                continue
            env.render(episode=index,step=i)
            sleep(1/playback_speed_factor)
        # for state in loaded_episode:
        #     env.state = state
        #     if not state[1:].any():
        #         continue
        #     #print(state)
        #     env.render()
        #     sleep(1/playback_speed_factor)
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
