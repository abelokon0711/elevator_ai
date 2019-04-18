
class Passenger:

    def __init__(self, id, start_floor, destination_floor, weight=0):
        if type(destination_floor) is not int:
            raise TypeError('destination_floor has to be an int')

        self.id = id
        self.start_floor = start_floor
        self.destination_floor = destination_floor
        self.boarded = False
        self.direction = None
