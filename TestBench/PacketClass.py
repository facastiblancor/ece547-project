class Packet:
    sourceAddr: int
    destinationAddr: int
    payloadSize: int
    waited: int

    def __init__(self, src, dest, plSize):
        self.waited = 0
        self.sourceAddr = src
        self.destinationAddr = dest
        self.payloadSize = plSize

    def updateTime(self):
        self.waited += 1

    def getWaitingTime(self) -> int:
        return self.waited
