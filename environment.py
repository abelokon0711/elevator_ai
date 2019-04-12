import math
import numpy as np

class Environment:
    def __init__(self):
        self.floors = np.arange(7)
        self.waitingPeople = np.zeros(7) 