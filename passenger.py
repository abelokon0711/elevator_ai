from random import randint

# implement https://uinames.com/ API


class Passenger:

    def __init__(self, environment, weight=0):
        self.environment = environment
        self.id = self.environment.get_Highest_id() + 1
        self.start_floor = randint(0, self.environment.number_of_floors - 1)
        self.destination_floor = randint(
            0, self.environment.number_of_floors - 1)
        if self.start_floor == self.destination_floor:
            self.destination_floor = (
                self.destination_floor + 1) % self.environment.number_of_floors

    def tick(self):
        pass
