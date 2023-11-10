# ECE 547 Group Project

import numpy as np


class tractor_class:
    posIndx: int
    trajectoryFileName: str
    numSteps: int
    trajectory = None

    def __init__(self, trajFile: str):
        self.posIndx = 0
        self.trajectoryFileName = trajFile
        self.numSteps = 0

    def loadTrajectory(self):
        self.trajectory = np.genfromtxt(self.trajectoryFileName, delimiter=',')
        self.numSteps = self.trajectory.shape[0]

    def move(self):
        self.posIndx += 1
        if self.posIndx >= self.numSteps:
            self.posIndx = 0

    def position(self) -> tuple:
        x = self.trajectory[self.posIndx, 0]
        y = self.trajectory[self.posIndx, 1]
        return x, y
