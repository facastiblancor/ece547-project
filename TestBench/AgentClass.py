# E547 Group Project

import numpy as np
from PacketClass import Packet


class Agent:
    mobility: bool
    trajectoryFileName: str
    posIndx: int
    len_trajectory: int

    id: int
    address: int
    queueLen: int
    coverRangeRadius: float
    speed: float
    timeoutCriteria: int

    trajectory = None
    neighbors: list
    queueingBuffer: list[Packet]
    # NOTE: the following data members are for ambient random process ONLY
    # the agent has no access to those results in its operation
    others = None

    def __init__(self, mobile: bool, name: int, rng: float):
        self.id = name
        self.posIndx = 0
        self.queueLen = 0
        self.mobility = mobile
        self.address = self.id + 1
        self.len_trajectory = 0
        self.coverRangeRadius = rng
        self.timeoutCriteria = 30
        self.neighbors = []
        # Init ambient data members
        self.others = [1, 2, 3, 4, 5, 6, 7]
        for ad in self.others:
            if ad == self.address:
                self.others.remove(ad)
                break

    def setPosition(self, x, y):
        if self.mobility:
            return
        self.trajectory = np.zeros(2, dtype=float)
        self.trajectory[0] = x
        self.trajectory[1] = y

    def loadTrajectory(self, trajFile: str):
        if not self.mobility:
            print('This agent is fixed in the field.')
            return
        self.trajectoryFileName = trajFile
        self.trajectory = np.genfromtxt(self.trajectoryFileName, delimiter=',')
        self.len_trajectory = self.trajectory.shape[0]

    def move(self):
        if not self.mobility:
            return
        self.posIndx += 1
        if self.posIndx >= self.len_trajectory:
            self.posIndx = 0

    def position(self) -> tuple:
        if self.mobility:
            x = self.trajectory[self.posIndx, 0]
            y = self.trajectory[self.posIndx, 1]
        else:
            x = self.trajectory[0]
            y = self.trajectory[1]
        return x, y

    def r(self) -> float:
        return self.coverRangeRadius

    def clearPreviousNeighborhood(self):
        self.neighbors.clear()

    def addNeighbor(self, neighborAddr):
        self.neighbors.append(neighborAddr)

    def collectPackets(self, numPackets):
        pld_len = 30
        random_index = round(np.random.uniform(0, 6))
        random_addr = self.others[random_index]
        for k in range(0, numPackets):
            self.queueingBuffer.append(Packet(self.address, random_addr, pld_len))

    def dropTimeoutPackets(self):
        indx = 0
        for pkt in self.queueingBuffer:
            if pkt.getWaitingTime() >= self.timeoutCriteria:
                self.queueingBuffer.pop(indx)
            else:
                pkt.updateTime()
                indx += 1
