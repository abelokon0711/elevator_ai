
class Person:
    def __init__(self, destination_floor, weight=0):
        if type(destination_floor) is not int:
            raise TypeError('destination_floor has to be an int')

        self.destination_floor = destination_floor
