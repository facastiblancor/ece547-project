import numpy as np


class Packet:
    sourceAddr: int
    destinationAddr: int
    payloadSize: int
    waited: int

    def __init__(self, src, dest, plSize, age=0):
        self.waited = age
        self.sourceAddr = src
        self.destinationAddr = dest
        self.payloadSize = plSize

    def updateTime(self):
        self.waited += 1

    def getWaitingTime(self) -> int:
        return self.waited


class Link:
    x = None
    y = None

    def __init__(self, x1, y1, x2, y2):
        self.x = [x1, x2]
        self.y = [y1, y2]

    def distance(self):
        temp1 = np.diff(self.x)
        temp1 *= temp1
        temp2 = np.diff(self.y)
        temp2 *= temp2
        return np.sqrt(temp1 + temp2)

    def keep(self, ths) -> bool:
        l = self.distance()
        if l <= ths:
            return True
        else:
            return False
