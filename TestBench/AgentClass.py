# E547 Group Project

import numpy as np
from PacketClass import Packet


class Agent:
    mobility: bool
    trajectoryFileName: str
    posIndx: int
    step: int
    len_trajectory: int

    id: int
    address: int
    queueLen: int
    bufferSize: int
    numSentPkt: int
    numSuccessPkt: int
    coverRangeRadius: float
    speed: float
    timeoutCriteria: int

    trajectory = None
    neighbors: list
    queueingBuffer: list[Packet]
    RoutingTable = None
    sendRequestList: list[int]
    nextStopList: list[int]
    # NOTE: the following data members are for ambient random process ONLY
    # the agent has no access to those results in its operation
    others = None

    def __init__(self, mobile: bool, name: int, rng: float, stepSize: int = 1):
        numPorts = 8
        self.id = name
        self.posIndx = 0
        self.step = stepSize
        self.queueLen = 0
        self.bufferSize = 200
        self.numSentPkt = 0
        self.numSuccessPkt = 0
        self.mobility = mobile
        self.address = self.id + 1
        self.len_trajectory = 0
        self.coverRangeRadius = rng
        self.timeoutCriteria = 10
        self.neighbors = []
        self.queueingBuffer = []
        self.sendRequestList = []
        self.nextStopList = []
        # Init ambient data members
        self.others = np.array([1, 2, 3, 4, 5, 6, 7], dtype=int)
        k = 0
        for ad in self.others:
            if ad == self.address:
                self.others = np.delete(self.others, k)
                break
            k += 1
        self.RoutingTable = np.zeros((numPorts, 2), dtype=int)

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
        self.posIndx += self.step
        if self.posIndx >= self.len_trajectory:
            tempIndx = self.posIndx - self.len_trajectory
            self.posIndx = tempIndx

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
        self.neighbors = []

    def addNeighbor(self, neighborAddr):
        self.neighbors.append(neighborAddr)

    def collectPackets(self, numPackets: int) -> int:
        overflow: int = 0
        pld_len = 30
        rng = np.random.default_rng()
        random_addr = rng.choice(self.others, size=numPackets, replace=True)
        self.queueLen = len(self.queueingBuffer)
        for k in range(0, numPackets):
            if (self.queueLen + k + 1) > self.bufferSize:
                overflow = numPackets - k
                break
            self.queueingBuffer.append(Packet(self.address, random_addr[k], pld_len))
            self.queueLen += 1
        return overflow

    def dropTimeoutPackets(self) -> int:
        numDrops: int = 0
        indx = 0
        for pkt in self.queueingBuffer:
            if pkt.getWaitingTime() >= self.timeoutCriteria:
                self.queueingBuffer.pop(indx)
                self.queueLen -= 1
                numDrops += 1
            else:
                pkt.updateTime()
                indx += 1
        return numDrops

    def file_a_SendRequest(self, indx, nextStopAddr):
        self.sendRequestList.append(indx)
        self.nextStopList.append(nextStopAddr)

    def completeTransmission(self):
        print('_', end='')
        for indx in self.sendRequestList:
            if len(self.queueingBuffer) <= 0:
                break
            if indx < 0 or indx >= len(self.queueingBuffer):
                continue
            self.queueingBuffer.pop(indx)
        self.queueLen = len(self.queueingBuffer)
        self.sendRequestList.clear()
        self.nextStopList.clear()

    def receivePacket(self, srcAddr, destAddr, payloadSize) -> int:
        if destAddr == self.address:
            self.ACK(srcAddr)
            return 1
        if self.queueLen >= self.bufferSize:
            return -1
        self.queueingBuffer.append(Packet(srcAddr, destAddr, payloadSize))
        self.queueLen += 1
        return 0

    def ACK(self, senderAddr, sendACKpacket: bool = False):
        if sendACKpacket:
            self.queueingBuffer.append(Packet(self.address, senderAddr, 4))
            self.queueLen += 1
        print('*', end='')

    def generateRoutingTable(self):
        print('to be updated...')

    def BF_route(self):
        # No routing if no connection
        if len(self.neighbors) <= 0:
            return
        # Routing policy
        k = 0
        for pkt in self.queueingBuffer:
            # Skip packets that are already served
            if k in self.sendRequestList:
                k += 1
                continue
            for nbor in self.neighbors:
                # Send packets to a stranger node
                if pkt.sourceAddr != nbor:
                    self.file_a_SendRequest(k, nbor)
                    break
            k += 1

    def smart_route(self):
        # No routing if no connection
        if len(self.neighbors) <= 0:
            return
        # Routing policy
        k = 0
        for pkt in self.queueingBuffer:
            # Skip packets that are already served
            if k in self.sendRequestList:
                k += 1
                continue
            for nbor in self.neighbors:
                # Direct link
                if pkt.destinationAddr == nbor:
                    self.file_a_SendRequest(k, nbor)
                    break
            k += 1
        k = 0
        for pkt in self.queueingBuffer:
            # Skip packets that are already served
            if k in self.sendRequestList:
                k += 1
                continue
            for nbor in self.neighbors:
                # Send packets to a stranger node
                if pkt.sourceAddr != nbor:
                    self.file_a_SendRequest(k, nbor)
                    break
            k += 1
