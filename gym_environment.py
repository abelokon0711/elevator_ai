import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
import copy
import queue

import pyglet
from pyglet import gl


class ElevatorEnv(gym.Env):
    def __init__(self):
        self.elevator_num = 1
        self.elevator_limit = 10
        self.floor_num = 5
        self.floor_limit = 10
        self.waiting_passangers = 0

        #Index where passenger slots starts
        self.passenger_start_index = self.elevator_num
        #Index where first slot of first floor starts  
        self.floor_start_index =  (self.elevator_num + (self.elevator_limit*self.elevator_num))

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Discrete(
            self.elevator_num * self.elevator_limit *
            self.floor_num**self.floor_limit)

        self.observation_space = spaces.Discrete(
            self.elevator_num
            + (self.elevator_num * self.elevator_limit)
            + (self.floor_limit*self.floor_num)
        )

        self.stateQueue = queue.Queue(maxsize=4)

        self.seed(10)
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    # returns true if any passanger is destinated to a upper floor and how many
    def passengerToUpperFloor(self, state, current_floor):
        count = 0
        # TODO code müsste für mehraufzüge angepasst werden
        for i in range(self.passenger_start_index, self.passenger_start_index+self.elevator_limit):
            if state[i] > current_floor:
                count += 1
        return (count > 0), count

    # returns true if any passanger is destinated to a lower floor and how many
    def passengerToLowerFloor(self, state, current_floor):
        count = 0
        # TODO code müsste für mehraufzüge angepasst werden
        for i in range(self.passenger_start_index, self.passenger_start_index+self.elevator_limit):
            if state[i] < current_floor:
                count += 1
        return (count > 0), count

    # returns true if any passanger is waiting at a upper floor and how many
    def passangerAtUpperFloor(self, state, current_floor):
        count = 0
        next_floor_index = self.floor_start_index + ((current_floor-1)*self.floor_limit) + self.floor_limit 
        last_floor_index = self.floor_start_index + (self.floor_num*self.floor_limit)

        for i in range(next_floor_index, last_floor_index):
            if state[i] != 0:
                count +=1
        return (count > 0), count
    
     # returns true if any passanger is waiting at a upper floor and how many
    def passangerAtLowerFloor(self, state, current_floor):
        count = 0
        previous_floor_last_index = self.floor_start_index + ((current_floor-1)*self.floor_limit) 

        for i in range(self.floor_start_index, previous_floor_last_index):
            if state[i] != 0:
                count +=1
        return (count > 0), count

    def passangerAtFloor(self, state, floor):
        count = 0
        current_floor_index = self.floor_start_index + ((floor -1)*self.floor_limit)

        for i in range(current_floor_index, current_floor_index+self.floor_limit):
            if state[i] != 0:
                count += 1
        return (count > 0), count

    def passengerInElevator(self, state):
        count = 0
        for i in range(self.elevator_num, self.elevator_limit):
            if state[i] != 0:
                count += 1
        return (count > 0), count

    # kick out passengers that wanted to get to this floor
    def unloadPassenger(self, state, floor):
        count = 0
        for i in range(self.passenger_start_index, self.passenger_start_index+self.elevator_limit):
            if state[i] == floor:
                state[i] = 0
                count += 1
        return (count > 0), count

    def nextPassengerSlot(self, state):
        index = -1
        for i in range(self.passenger_start_index, self.passenger_start_index+self.elevator_limit):
            if state[i] == 0:
                index = i 
                break
        return index
            
    
    # Load passengers from given floor
    # Returns True if atleast a passenger was laoded, how many where loaded, and how many where left at the floor
    def loadPassenger(self, state, floor):
        passengers_before_loading = self.passangerAtFloor(state, floor)[1]
        loaded_passengers = 0
        current_floor_index = self.floor_start_index + ((floor -1)*self.floor_limit)
        for i in range(current_floor_index, current_floor_index+self.floor_limit):
            if state[i] != 0:    
                free_slot = self.nextPassengerSlot(state)
                if free_slot != -1:
                    state[free_slot] = state[i]
                    state[i] = 0
                    loaded_passengers += 1
                elif free_slot == -1:
                    break
        return (loaded_passengers > 0), loaded_passengers, (passengers_before_loading - loaded_passengers)
        

    def nextState(self, action):
        assert self.action_space.contains(
            action), "%r (%s) invalid" % (action, type(action))
        state = copy.copy(self.state)
        current_floor = int(state[0])
        
        reward = 0
        if action == 0:
            if state[0] == 1:
                reward -= 1000000
            else:
                # check if there is reason to go a floor up
                # is there a passenger waiting at a lower a floor?
                passenger_at_lower_floors, num_passenger_at_lower_floor = self.passangerAtLowerFloor(state, current_floor)

                # is a passanger inside the elevator destinated to an upper floor?
                passenger_to_lower_floors, num_passenger_to_lower_floor = self.passengerToLowerFloor(state, current_floor)

                # shit action m8
                if not passenger_at_lower_floors and not passenger_to_lower_floors:
                    reward -= 100

                if num_passenger_at_lower_floor > 0:
                    reward += 1
                
                if num_passenger_to_lower_floor > 0:
                    reward += 2

                state[0] -= 1
        elif action == 1:
            if state[0] == self.floor_num:
                reward -= 1000000
            else:
                # check if there is reason to go a floor up

                # is there a passenger waiting at a higher a floor?
                passenger_at_upper_floors, num_passenger_at_upper_floor = self.passangerAtUpperFloor(state, current_floor)

                # is a passanger inside the elevator destinated to an upper floor?
                passenger_to_upper_floors, num_passenger_to_upper_floor = self.passengerToUpperFloor(state, current_floor)

                # shit action m8
                if not passenger_at_upper_floors and not passenger_to_upper_floors:
                    reward -= 100
                
                if num_passenger_at_upper_floor > 0:
                    reward += 1
                if num_passenger_to_upper_floor > 0:
                    reward += 2

                state[0] += 1
        elif action == 2:
            # Are there any passengers in the elevator that want to leave?
            passengers_left = False
            num_passengers_left = 0
            #print("Passengers in Elevator",self.passengerInElevator(state))
            if self.passengerInElevator(state)[0]:
                passengers_left, num_passengers_left = self.unloadPassenger(state, current_floor)
                # reward -= self.passengerInElevator(state)[1]*1
                #print("Passengers left Elevator", passengers_left, num_passengers_left)
                #print("Passengers in Elevator now",self.passengerInElevator(state))
            

            # Check if there are any people waiting at this floor
            passengers_entered = False
            num_passengers_entered = 0            
            num_passenger_left_at_floor = 0
            if self.passangerAtFloor(state, current_floor)[0]:
                #print("Passengers at floor", self.passangerAtFloor(state,current_floor)[1])
                passengers_entered, num_passengers_entered, num_passenger_left_at_floor = self.loadPassenger(state, current_floor)
                #print("Passengers entered Elevator", passengers_entered, num_passengers_entered)
                #print("Passengers left at floor", num_passenger_left_at_floor)
                #print("Passengers in Elevator now",self.passengerInElevator(state))

            if passengers_entered == False and passengers_left == False:
                reward = -1000
                #print("No one left or entered")

            reward += num_passengers_left*10
            reward += num_passengers_entered*5
            reward -= num_passenger_left_at_floor


        done = False
        if self.waiting_passangers == 0:
            done = True
            reward += 400
        return state, reward, done, {}

    def eval(self, action):
        state, reward, done, obj = self.nextState(action)
        return np.array(state), reward, done, obj

    def step(self, action):
        state, reward, done, obj = self.nextState(action)
        self.state = state

        # Push first in queue out and add new state as last in queue
        if self.stateQueue.full():
            self.stateQueue.get()
        self.stateQueue.put(copy.copy(self.state))

        # If queue full start checking for oscillation
        if self.stateQueue.full():
            queueList = np.asarray(list(self.stateQueue.queue))
            if not np.array_equal(queueList[0], queueList[1]): 
                if np.array_equal(queueList[0], queueList[2]) and np.array_equal(queueList[1], queueList[3]):
                    reward -= 1000000

        return np.array(state), reward, done, obj

    def reset(self):
        # set here waiting_passangers
        self.state = np.zeros(1 + self.elevator_limit +
                              self.floor_num * self.floor_limit)

        # initial elevator position
        self.state[0] = 1

        # here index is 51
        self.waiting_passangers = 20
        for i in range(self.waiting_passangers):

            # self.state[1 + self.elevator_limit +
            #         (self.floor_num - 1) * self.floor_limit] = 1

            random_floor = int(self.np_random.uniform(1, self.floor_num + 1))
            random_destination = int(
                self.np_random.uniform(1, self.floor_num + 1))

            while random_floor == random_destination:
                random_destination = int(
                    self.np_random.uniform(1, self.floor_num + 1))

            stockwerk_index = int(1 + self.elevator_limit + ((random_floor - 1) *
                                                             self.floor_limit))
            for k in range(0,  self.floor_limit):
                if self.state[stockwerk_index+k] == 0:
                    self.state[stockwerk_index+k] = random_destination
                    break
        self.steps_beyond_done = None
        return np.array(self.state)

    def render(self, mode='human'):
        from gym.envs.classic_control import rendering
        self.screen_width = 600
        self.screen_height = 400

        if self.viewer is None:

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
