import gym
from gym.envs.registration import registry, register, make, spec

register(
    id='Elevator-v0',
    entry_point='gym_environment:ElevatorEnv',
    max_episode_steps=200,
    reward_threshold=25.0,
)

env = gym.make('Elevator-v0')
for i_episode in range(50):
    observation = env.reset()
    for t in range(1000):
        env.render()
        print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)

        if done:
            print("Episode finished after {} timesteps".format(t + 1))
            break
env.close()
