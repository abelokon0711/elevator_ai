from random import randint

# implement https://uinames.com/ API


class Passenger:


    def __init__(self, environment,  start_floor = None, destination_floor = None, weight=0):
        self.environment = environment
        self.id = self.environment.get_Highest_id() + 1
        if start_floor is not None:
            self.start_floor = start_floor
        else:
            self.start_floor = randint(0, self.environment.number_of_floors - 1)

        if destination_floor is not None:
            self.destination_floor = destination_floor
        else:
            self.destination_floor = randint(
                0, self.environment.number_of_floors - 1)

        if self.start_floor == self.destination_floor:
            self.destination_floor = (
                self.destination_floor + 1) % self.environment.number_of_floors

    def tick(self):
        pass
