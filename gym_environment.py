import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
import pyglet
from pyglet import gl
from pyglet.gl import *


class ElevatorEnv(gym.Env):
    def __init__(self):
        self.elevator_num = 1
        self.elevator_limit = 10
        self.floor_num = 5
        self.floor_limit = 10
        self.waiting_passangers = 0

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Discrete(
            self.elevator_num * self.elevator_limit * self.floor_num ** self.floor_limit)

        self.seed(10)
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(
            action), "%r (%s) invalid" % (action, type(action))
        state = self.state
        current_floor = state[1]

        reward = 0
        if action == 0:
            current_floor -= 1
        elif action == 1:
            current_floor += 1
        elif action == 2:
            passengers_in_elevator_num = 0
            # indices to iterate over for passengers in the elevator
            # state[i] equals passenger destination
            for i in range(1, self.elevator_limit + 1):
                if state[i] == 0:
                    continue
                if state[i] == current_floor:
                    state[i] = 0
                    reward += 10
                    self.waiting_passangers -= 1
                else:
                    passengers_in_elevator_num += 1

            # indices to iterate over for passengers waiting on the current floor
            # state[i] equals passenger destination
            start = self.floor_num * current_floor + self.elevator_limit
            stop = start + self.floor_limit
            for i in range(int(start), int(stop)):
                if state[i] == 0:
                    continue

                # if elevator capacity is at max
                if passengers_in_elevator_num == self.elevator_limit:
                    reward = -10

                for j in range(start, start + (self.elevator_limit - passengers_in_elevator_num)):
                    for k in range(1, self.elevator_limit + 1):
                        if state[k] == 0:
                            # move passenger into elevator
                            state[k] = state[j]

        if reward == 0:
            reward = -1

        done = False
        if self.waiting_passangers == 0:
            done = True
            reward += 40

        return np.array(self.state), reward, done, {}

    def reset(self):
        # set here waiting_passangers
        self.state = np.zeros(1 + self.elevator_limit +
                              self.floor_num * self.floor_limit)

        # here index is 51
        self.state[1 + self.elevator_limit +
                   (self.floor_num - 1) * self.floor_limit] = 1

        self.waiting_passangers = 1
        self.steps_beyond_done = None
        return np.array(self.state)

    def render(self, mode='human'):
        screen_width = 600
        screen_height = 400

        floor_padding = (screen_height - 100) / self.floor_num

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)
            self.score_label = pyglet.text.Label('0000', font_size=72, font_name="Times New Roman",
                                                 x=screen_width, y=screen_height, anchor_x='left', anchor_y='center',
                                                 color=(0, 0, 0, 255))

            # render floors
            for i in range(self.floor_num):
                track = rendering.Line(
                    (screen_width/2, 50 + floor_padding * i), (screen_width, 50 + floor_padding * i))
                track.set_color(0, 0, 0)
                self.viewer.add_geom(track)

            track = rendering.Line(
                (screen_width/2, 50 + floor_padding * self.floor_num), (screen_width, 50 + floor_padding * self.floor_num))
            track.set_color(0, 0, 0)
            self.viewer.add_geom(track)

            boxwidth = floor_padding/1.5
            boxheight = floor_padding
            l, r, t, b = -boxwidth/2, boxwidth/2, boxheight-boxwidth/2, -boxwidth/2
            box = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            self.boxtrans = rendering.Transform(
                (screen_width/2 + boxwidth, (self.state[0] * floor_padding - 30) + 40))
            box.add_attr(self.boxtrans)
            box.set_color(.4, .4, .4)

            self.transform = rendering.Transform()

            self.viewer.add_geom(box)

            win = self.viewer.window
            win.switch_to()
            win.dispatch_events()
            win.clear()

            self.score_label.draw()

        if self.state is None:
            return None

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
