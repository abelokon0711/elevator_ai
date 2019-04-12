class Elevator:
    def __init__(self, floor):
        self.floor = floor

    def goUp(self):
        self.floor += 1

    def goDown(self):
        if(self.floor > 0): 
            self.floor -= 1
