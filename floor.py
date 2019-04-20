from passenger import Passenger


class Floor:
    def __init__(self, environment, floor_id):
        self.environment = environment
        if type(floor_id) is not int:
            raise TypeError('floor_id has to be an int')

        if floor_id > self.environment.number_of_floors:
            raise ValueError('Floor too high')

        self.floor_id = floor_id
        self.waiting_queue = []

    def add_person_to_waiting_queue(self, Passenger):
        self.waiting_queue.append(Passenger)

    def remove_person_from_waiting_queue(self, Passenger):
        for p in self.waiting_queue:
            if p.id == Passenger.id:
                self.waiting_queue.remove(p)

    def tick(self):
        pass
