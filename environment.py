import math
import numpy as np

class Environment:
    FLOORS = 6
    ELEVATORS = 3

    def __init__(self):
        self.floors = np.arange(7)
        self.waitingPeople = np.zeros(7)
