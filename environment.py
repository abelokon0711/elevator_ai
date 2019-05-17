# import numpy as np
from elevator import Elevator
from floor import Floor
from generator import Generator
from passenger import Passenger
import numpy as np
from gym import utils
from gym.envs.toy_text import discrete

class Environment(discrete.DiscreteEnv):

    # ELEVATOR CONFIGS
    FLOOR_TIME = 4  # time to move one floor
    ELEVATOR_CAPACITY = 10
    TICKS_NEEDED_TO_GENERATE_PASSENGER = 20
    PASSENGERS_TO_BE_GENERATED = 2

    # LISTS

    def __init__(self, floors=7, elevators=1):
        self.generator = Generator(self)
        self.clock = 0
        self.floors = []
        self.elevators = []
        self.all_passengers = []
        self.number_of_floors = floors
        self.number_of_elevators = elevators
        for i in range(self.number_of_floors):
            self.floors.append(Floor(self, i))
        for i in range(self.number_of_elevators):
            self.elevators.append(Elevator(i, self))
            
        self.locs = locs = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6)]
        num_states = 21952
        num_rows = 1
        num_columns = 7
        max_row = num_rows - 1
        max_col = num_columns - 1
        initial_state_distrib = np.zeros(num_states)
        num_actions = 4
        P = {state: {action: []
                     for action in range(num_actions)} for state in range(num_states)}
        for row in range(num_rows):
            for col in range(num_columns):
                for pass0_idx in range(len(locs) + 1):  # +1 for being inside elevator
                    for dest0_idx in range(len(locs)):
                        for pass1_idx in range(len(locs) + 1):  # +1 for being inside elevator
                            for dest1_idx in range(len(locs)):
                                state = self.encode(row, col, pass0_idx, dest0_idx, pass1_idx, dest1_idx)
                                if (pass0_idx < 7 and pass0_idx != dest0_idx) and (pass1_idx < 7 and pass1_idx != dest1_idx):
                                    initial_state_distrib[state] += 1
                                for action in range(num_actions):
                                    # defaults
                                    new_row, new_col, new_pass0_idx, new_pass1_idx = row, col, pass0_idx, pass1_idx
                                    reward = -1 # default reward when there is no pickup/dropoff
                                    done = False
                                    elevator_loc = (row, col)

                                    if action == 0:
                                        new_col = min(col + 1, max_col)
                                    elif action == 1:
                                        new_col = max(col - 1, 0)
                                    elif action == 2:  # pickup
                                        if (pass0_idx < 7 and elevator_loc == locs[pass0_idx]):
                                            new_pass0_idx = 7
                                        if (pass1_idx < 7 and elevator_loc == locs[pass1_idx]):
                                            new_pass1_idx = 7
                                        else: # passenger not at floor
                                            reward = -10
                                    elif action == 3:  # dropoff
                                        if (elevator_loc == locs[dest0_idx]) and pass0_idx == 7:
                                            new_pass0_idx = dest0_idx
                                            if pass1_idx == dest1_idx:
                                                done = True
                                            reward = 20
                                        elif (elevator_loc in locs) and pass0_idx == 4:
                                            new_pass0_idx = locs.index(elevator_loc)
                                        elif (elevator_loc == locs[dest1_idx]) and pass1_idx == 7:
                                            new_pass1_idx = dest1_idx
                                            if pass0_idx == dest0_idx:
                                                done = True
                                            reward = 20
                                        elif (elevator_loc in locs) and pass1_idx == 4:
                                            new_pass1_idx = locs.index(elevator_loc)    
                                        else: # dropoff at wrong location
                                            reward = -10
                                    new_state = self.encode(
                                        new_row, new_col, new_pass0_idx, dest0_idx, new_pass1_idx, dest1_idx)
                                    P[state][action].append(
                                        (1.0, new_state, reward, done))
        initial_state_distrib /= initial_state_distrib.sum()
        discrete.DiscreteEnv.__init__(
            self, num_states, num_actions, P, initial_state_distrib)

    def add_passenger(self, p):
        self.all_passengers.append(p)
        self.floors[p.start_floor].add_person_to_waiting_queue(p) # Add passanger to floor waiting queue

    def get_Highest_id(self):
        return len(self.all_passengers)

    def get_clock(self):
        return self.clock

    def collect_state(self):
        pass

    def encode(self, elevator_row, elevator_col, pass0_loc, dest0_idx, pass1_loc, dest1_idx):
        # (1) 7, 8, 7, 8, 7
        i = elevator_row
        i *= 7
        i += elevator_col
        i *= 8
        i += pass0_loc
        i *= 7
        i += dest0_idx
        i *= 8
        i += pass1_loc
        i *= 7
        i += dest1_idx
        return i

    def decode(self, i):
        out = []
        out.append(i % 7)
        i = i // 7
        out.append(i % 8)
        i = i // 8
        out.append(i % 7)
        i = i // 7
        out.append(i % 8)
        i = i // 8
        out.append(i % 7)
        i = i // 7
        out.append(i)
        assert 0 <= i < 8
        return reversed(out)

    def tick(self):
        # TODO: Send current state to Agent
        # self.generator.tick()
        for elevator in self.elevators:
            elevator.tick()
        for floor in self.floors:
            floor.tick()
        for passanger in self.all_passengers:
            print("TIME: " + str(self.get_clock()))
            print("Passanger ID: " + str(passanger.id))
            print("Passanger Start Floor: " + str(passanger.start_floor))
            print("Passanger Destination Floor: " +
                  str(passanger.destination_floor))

        self.clock += 1
