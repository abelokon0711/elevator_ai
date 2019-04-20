from enum import Enum


class DirectionState(Enum):
    IDLE = 0
    UP = 1
    DOWN = 2


class Elevator:
    def __init__(self, elevator_id, environment, current_floor=0, capacity=10):
        self.environment = environment

        if type(elevator_id) is not int:
            raise TypeError('elevator_id has to be an int')

        if not current_floor < self.environment.number_of_floors:
            raise ValueError('Floor too high')

        self.elevator_id = elevator_id
        self.current_floor = current_floor
        self.destination_floor = None
        self.capacity = capacity
        self.people_in_elevator = 0

    def go_up(self):
        if not self.current_floor < self.environment.number_of_floors:
            raise ValueError('Floor too high')

        self.current_floor += 1

    def go_down(self):
        if self.current_floor == 0:
            raise ValueError('Elevator is on floor 0')

        self.current_floor -= 1

    def getDirection(self):
        dir = self.destination_floor - self.current_floor

        if dir < 0:
            return DirectionState.DOWN
        elif dir > 0:
            return DirectionState.UP
        else:
            return DirectionState.IDLE

    def tick(self):
        pass
