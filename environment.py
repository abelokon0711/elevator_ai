import math
# import numpy as np
from elevator import Elevator
from passenger import Passenger
from floor import Floor
from generator import Generator


class Environment:

    # ELEVATOR CONFIGS
    FLOOR_TIME = 4  # time to move one floor
    ELEVATOR_CAPACITY = 10
    TICKS_NEEDED_TO_GENERATE_PASSENGER = 20
    PASSENGERS_TO_BE_GENERATED = 2

    # LISTS

    def __init__(self, floors=6, elevators=2):
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

    def add_passenger(self, p):
        self.all_passengers.append(p)
        self.floors[p.start_floor].waiting_queue.append(
            p)  # Add passanger to floor waiting queue

    def get_Highest_id(self):
        return len(self.all_passengers)

    def get_clock(self):
        return self.clock

    def collect_state(self):
        pass

    def tick(self):
        # TODO: Send current state to Agent
        self.generator.tick()
        self.elevators[0].go_up()
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
