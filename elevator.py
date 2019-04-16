class Elevator:
    def __init__(self, elevator_id, floor=0, capacity=10):
        if elevator_id is not int:
            raise TypeError('elevator_id has to be an int')

        if self.floor not < Environment.FLOOR:
            raise ValueError('Floor too high')

        self.elevator_id = elevator_id
        self.floor = floor

    def go_up(self):
        if self.floor not < Environment.FLOOR
            raise ValueError('Floor too high')

        self.floor += 1

    def go_down(self):
        if self.floor == 0 :
            raise ValueError('Elevator is on floor 0')

        self.floor -= 1
