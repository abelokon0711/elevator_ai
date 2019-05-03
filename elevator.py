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
        self.passenger_in_elevator = []

    def is_passenger_waiting_on_current_floor(self):
        if len(self.environment.floors[self.current_floor].waiting_queue) > 0:
            return True
        else:
            return False

    def is_elevator_empty(self):
        if len(self.passenger_in_elevator) == 0:
            return True
        else:
            return False

    def is_elevator_full(self):
        if len(self.passenger_in_elevator) == self.capacity:
            return True
        else:
            return False

    def add_passenger_from_current_floor_to_elevator(self):
        if self.is_passenger_waiting_on_current_floor:
            self.passenger_in_elevator.append(
                    self.environment.floors[
                        self.current_floor].waiting_queue[0])
            self.environment.floors[
                    self.current_floor
                    ].remove_first_person_from_waiting_queue()

    def transfer_passenger_from_elevator_to_current_floor(self):
        if not self.is_elevator_empty:
            for p in self.passenger_in_elevator:
                if p.destination_floor == self.current_floor:
                    self.environment.floors[
                            self.current_floor
                            ].add_passenger_to_target_list(p)
                    self.passenger_in_elevator.remove(p)

    def go_up(self):
        if self.current_floor >= self.environment.number_of_floors:
            return
            #raise ValueError('Floor too high')
        self.current_floor += 1

    def go_down(self):
        if self.current_floor == 0:
            return
            #raise ValueError('Elevator is on floor 0')

        self.current_floor -= 1

    def getDirection(self):
        dir = self.destination_floor - self.current_floor

        if dir < 0:
            return DirectionState.DOWN
        elif dir > 0:
            return DirectionState.UP
        else:
            return DirectionState.IDLE

    def getCurrentFloor(self):
        return self.current_floor

    def tick(self):
        pass
