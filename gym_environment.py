import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np

import pyglet
from pyglet import gl


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
        self.screen_width = 600
        self.screen_height = 400

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(
                self.screen_width, self.screen_height)
            self.transform = rendering.Transform()

            floor_padding = (self.screen_height - 100) / self.floor_num
            boxwidth = floor_padding/1.5
            boxheight = floor_padding
            l, r, t, b = -boxwidth/2, boxwidth/2, boxheight-boxwidth/2, -boxwidth/2
            box = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            self.boxtrans = rendering.Transform(
                (self.screen_width/2 + boxwidth, (self.state[0] * floor_padding - 30) + 40))
            box.add_attr(self.boxtrans)
            box.set_color(.4, .4, .4)

            for i in range(self.floor_num):
                start = self.floor_num * (i+1) + self.elevator_limit
                stop = start + self.floor_limit

                for j in range(int(start), int(stop)):
                    if j != 0:
                        print('ok')

            self.viewer.add_geom(box)

            win = self.viewer.window
            win.switch_to()
            win.dispatch_events()

            win.clear()
            t = self.transform
            self.score_label = pyglet.text.Label('HELLO WORLD', font_size=36,
                                                 x=20, y=self.screen_height*2.5/40.00, anchor_x='left', anchor_y='center', color=(0, 0, 0, 255))
            pixel_scale = 1
            if hasattr(win.context, '_nscontext'):
                pixel_scale = win.context._nscontext.view(
                ).backingScaleFactor()  # pylint: disable=protected-access
            VP_W = int(pixel_scale * self.screen_width)
            VP_H = int(pixel_scale * self.screen_height)

            gl.glViewport(0, 0, VP_W, VP_H)
            t.enable()
            self.render_floors()
            t.disable()

            self.render_indicators(self.screen_width, self.screen_height)

            win.flip()
            return self.viewer.isopen

    def render_floors(self):
        PLAYFIELD = 2000
        gl.glBegin(gl.GL_QUADS)
        gl.glColor4f(1, 1, 1, 1.0)
        gl.glVertex3f(-PLAYFIELD, +PLAYFIELD, 0)
        gl.glVertex3f(+PLAYFIELD, +PLAYFIELD, 0)
        gl.glVertex3f(+PLAYFIELD, -PLAYFIELD, 0)
        gl.glVertex3f(-PLAYFIELD, -PLAYFIELD, 0)

        floor_padding = (self.screen_height - 100) / self.floor_num
        for floor in range(self.floor_num+1):
            gl.glColor4f(0, 0, 0, 1)
            gl.glVertex3f(self.screen_width, 50 + floor_padding * floor, 0)
            gl.glVertex3f(self.screen_width, 50 + floor_padding * floor + 1, 0)
            gl.glVertex3f(self.screen_width/2, 50 +
                          floor_padding * floor + 1, 0)
            gl.glVertex3f(self.screen_width/2, 50 + floor_padding * floor, 0)
        gl.glEnd()

    def render_indicators(self, W, H):
        gl.glBegin(gl.GL_QUADS)
        gl.glColor4f(1, 1, 1, 1)
        gl.glVertex3f(W/2, 0, 0)
        gl.glVertex3f(W/2, H, 0)
        gl.glVertex3f(0, H, 0)
        gl.glVertex3f(0, 0, 0)
        gl.glEnd()
        self.score_label.text = "%04i" % 0
        self.score_label.draw()

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
