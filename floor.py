from environment import Environment
from passenger import Passenger
class Floor:
    def __init__(self, floor_id):
        if type(floor_id) is not int:
            raise TypeError('floor_id has to be an int')

        if not floor_id > Environment.FLOORS:
            raise ValueError('Floor too high')

        self.floor_id = floor_id
        self.waiting_queue = []
    
    def add_person_to_waiting_queue(self, Passenger):
        self.waiting_queue.append(Passenger)

    def remove_person_from_waiting_queue(self, Passenger):
        for p in self.waiting_queue:
            if p.id == Passenger.id:
                self.waiting_queue.remove(p)

