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
            self.elevator_num * self.elevator_limit *
            self.floor_num**self.floor_limit)

        self.observation_space = spaces.Discrete(
            self.elevator_num
            + (self.elevator_num * self.elevator_limit)
            + (self.floor_limit*self.floor_num)
        )

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

        reward = 0
        if action == 0:
            if state[0] == 1:
                reward -= 100
            else:
                state[0] -= 1
        elif action == 1:
            if state[0] == self.floor_num:
                reward -= 100
            else:
                state[0] += 1
        elif action == 2:
            current_floor = state[0]
            passengers_in_elevator_num = 0
            passengers_entered = False
            passengers_left = False
            # indices to iterate over for passengers in the elevator
            # state[i] equals passenger destination
            for i in range(1, self.elevator_limit + 1):
                if state[i] == 0:
                    continue
                if state[i] == current_floor:
                    state[i] = 0
                    reward += 10
                    self.waiting_passangers -= 1
                    passengers_left = True
                else:
                    passengers_in_elevator_num += 1
            # passengers_in_elevator_num = amount of passengers that did not leave elevator

            # indices to iterate over for passengers waiting on the current floor
            # state[i] equals passenger destination
            start = (current_floor * self.floor_limit) + 1
            stop = start + self.floor_limit
            for i in range(int(start), int(stop)):
                print(i)
                if state[i] == 0:
                    continue

                # if elevator capacity is at max
                if passengers_in_elevator_num == self.elevator_limit:
                    reward = -10

                for j in range(
                        int(start),
                        int(stop)):
                    for k in range(1, self.elevator_limit):
                        if state[k] == 0:
                            # move passenger into elevator
                            state[k] = state[j]
                            state[j] = 0
                            passengers_entered = True

            if passengers_entered == False and passengers_left == False:
                reward = -10

        if reward == 0:
            reward = -1

        done = False
        if self.waiting_passangers == 0:
            done = True
            reward += 40
        self.state = state
        return np.array(state), reward, done, {}

    def reset(self):
        # set here waiting_passangers
        self.state = np.zeros(1 + self.elevator_limit +
                              self.floor_num * self.floor_limit)

        # initial elevator position
        self.state[0] = 1

        # here index is 51
        # self.state[1 + self.elevator_limit +
        #           (self.floor_num - 1) * self.floor_limit] = 1

        random_floor = int(self.np_random.uniform(1, self.floor_num + 1))
        random_destination = int(self.np_random.uniform(1, self.floor_num + 1))

        while random_floor == random_destination:
            random_destination = int(
                self.np_random.uniform(1, self.floor_num + 1))

        self.state[int(1 + self.elevator_limit + (random_floor - 1) *
                       self.floor_limit)] = random_destination

        self.waiting_passangers = 1
        self.steps_beyond_done = None
        return np.array(self.state)

    def render(self, mode='human'):
        self.screen_width = 600
        self.screen_height = 400

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(self.screen_width,
                                           self.screen_height)
            self.transform = rendering.Transform()

            self.floor_padding = (self.screen_height - 100) / self.floor_num
            boxwidth = self.floor_padding / 1.5
            boxheight = self.floor_padding
            l, r, t, b = -boxwidth / 2, boxwidth / 2, boxheight - boxwidth / 2, -boxwidth / 2
            box = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            self.boxtrans = rendering.Transform(
                (self.screen_width / 2 + boxwidth,
                 (self.state[0] * self.floor_padding - 30) + 40))
            box.add_attr(self.boxtrans)
            box.set_color(.4, .4, .4)

            for i in range(self.floor_num):
                start = self.floor_num * (i + 1) + self.elevator_limit
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
            self.score_label = pyglet.text.Label('HELLO WORLD',
                                                 font_size=36,
                                                 x=20,
                                                 y=self.screen_height * 2.5 /
                                                 40.00,
                                                 anchor_x='left',
                                                 anchor_y='center',
                                                 color=(0, 0, 0, 255))
            pixel_scale = 1
            if hasattr(win.context, '_nscontext'):
                pixel_scale = win.context._nscontext.view().backingScaleFactor(
                )  # pylint: disable=protected-access
            VP_W = int(pixel_scale * self.screen_width)
            VP_H = int(pixel_scale * self.screen_height)

            gl.glViewport(0, 0, VP_W, VP_H)

            t.enable()
            self.render_floors()
            self.render_indicators(self.screen_width, self.screen_height)
            self.render_elevators()
            t.disable()

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

        # increase range by one to add line on the top
        for floor in range(self.floor_num + 1):
            gl.glColor4f(0, 0, 0, 1)
            gl.glVertex3f(self.screen_width, 50 + self.floor_padding * floor,
                          0)
            gl.glVertex3f(self.screen_width,
                          50 + self.floor_padding * floor + 1, 0)
            gl.glVertex3f(self.screen_width / 2,
                          50 + self.floor_padding * floor + 1, 0)
            gl.glVertex3f(self.screen_width / 2,
                          50 + self.floor_padding * floor, 0)
        gl.glEnd()

    def render_indicators(self, W, H):
        gl.glBegin(gl.GL_QUADS)
        gl.glColor4f(1, 1, 1, 1)
        gl.glVertex3f(W / 2, 0, 0)
        gl.glVertex3f(W / 2, H, 0)
        gl.glVertex3f(0, H, 0)
        gl.glVertex3f(0, 0, 0)
        gl.glEnd()

        for floor in range(self.floor_num):
            position_x = 20
            position_y = 50 + (self.floor_padding) * \
                floor + (self.floor_padding/2)

            start = floor * self.floor_limit + self.elevator_limit + 1
            stop = start + self.floor_limit
            waiting_passangers_floor = 0
            for i in range(int(start), int(stop)):
                if self.state[i] > 0:
                    waiting_passangers_floor += 1

            score_label = pyglet.text.Label('Warteschlange: ' +
                                            str(waiting_passangers_floor),
                                            font_size=14,
                                            x=position_x,
                                            y=position_y,
                                            anchor_x='left',
                                            anchor_y='center',
                                            color=(0, 0, 0, 255))
            score_label.draw()

    def render_elevators(self):
        elevator_width = 50
        gl.glBegin(gl.GL_QUADS)
        for i in range(self.elevator_num):
            current_floor = self.state[i] - 1
            gl.glColor4f(0.3, 0.3, 0.3, 1)
            gl.glVertex3f(self.screen_width / 2 + elevator_width,
                          50 + self.floor_padding * current_floor, 0)
            gl.glVertex3f(
                self.screen_width / 2 + elevator_width,
                50 + self.floor_padding * current_floor + self.floor_padding,
                0)
            gl.glVertex3f(
                self.screen_width / 2,
                50 + self.floor_padding * current_floor + self.floor_padding,
                0)
            gl.glVertex3f(self.screen_width / 2,
                          50 + self.floor_padding * current_floor, 0)
        gl.glEnd()

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
