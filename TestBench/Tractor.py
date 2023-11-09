# ECE 547 Group Project

import numpy as np


class tractor:
    posIndx: int
    trajectoryFileName: str
    trajectory = None

    def __init__(self, trajFile):
        self.posIndx = 0
        self.trajectoryFileName = trajFile

    def loadTrajectory(self):
        self.trajectory = np.genfromtxt(self.trajectoryFileName, delimiter=',')
