class Floor:
    def __init__(self, environment, floor_id):
        self.environment = environment
        if type(floor_id) is not int:
            raise TypeError('floor_id has to be an int')

        if floor_id > self.environment.number_of_floors:
            raise ValueError('Floor too high')

        self.floor_id = floor_id
        self.waiting_queue = []
        self.passengers_at_target_list = []

    def add_person_to_waiting_queue(self, passenger):
        self.waiting_queue.append(passenger)

    def remove_first_person_from_waiting_queue(self, passenger):
        self.waiting_queue.pop(0)

    def add_passenger_to_target_list(self, passenger):
        self.passengers_at_target_list.append(passenger)

    def tick(self):
        pass
