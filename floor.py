from environment import Environment

class Floor:
    def __init__(self, floor_id):
        if type(floor_id) is not int:
            raise TypeError('floor_id has to be an int')

        if not floor_id > Environment.FLOORS:
            raise ValueError('Floor too high')

        self.floor_id = floor_id
        self.waitingQueue = 0

