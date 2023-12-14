# ECE 547 Group Project
# Python 3.11.3
# NumPy 1.24.3

import itertools

import numpy as np
import matplotlib.pyplot as plt
from AgentClass import Agent
from Visualizer import showTrajectories, showLandscape, plotPacketArrivals, saveSimulationFrame, plotQueueLen
from PacketClass import Packet, Link

EXPORT_IMAGE: bool = False

numFixedAgents = 5
numSimulationSteps = 100

rng1 = 2
rng2 = 1.7
rng3 = 1.6

# Set field size in miles
L = 1.75 * np.sqrt(2) + 1
W = 0.5 + 1.75 / np.sqrt(2) + 1.25 + 6 / 8 + 1

# Set up data containers
agents: list[Agent] = []

# Introduce field sensors
fixedAgentPositions = np.genfromtxt('fixed_agents_coord_list.csv', delimiter=',')
for k in range(0, numFixedAgents):
    agents.append(Agent(mobile=False, name=k, rng=rng1))
for k in range(0, numFixedAgents):
    x1 = fixedAgentPositions[k, 0]
    y1 = fixedAgentPositions[k, 1]
    agents[k].setPosition(x1, y1)

# Print info of all field sensors
print('Coordinates of all field sensors:')
for fix in agents:
    print(fix.position())

# Introduce a tractor
agents.append(Agent(mobile=True, name=5, rng=rng2))
agents[5].loadTrajectory('tractor1_trajectory.csv')

# Introduce a scouting drone
agents.append(Agent(mobile=True, name=6, rng=rng3))
agents[6].loadTrajectory('drone1_trajectory.csv')
numAgents = len(agents)

traj1 = agents[5].trajectory
traj2 = agents[6].trajectory
showTrajectories(traj1, traj2, 1)
showLandscape(traj1, traj2, fixedAgentPositions, 2)


def address2index(addr: int) -> int:
    errFlag = True
    indx = 0
    for agt in agents:
        if agt.address == addr:
            errFlag = False
            break
        indx += 1
    if errFlag:
        indx = -1
    return indx


def findDistance(agent1: Agent, agent2: Agent) -> float:
    coord1 = agent1.position()
    coord2 = agent2.position()
    dist = np.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[0] - coord2[1]) ** 2)
    return dist


def evaluateConnectivity(dist, r1, r2) -> bool:
    #print(f'{dist}, {r1}, {r2}')
    #return dist <= np.min([r1, r2])
    if dist <= np.min([r1, r2]) + 0.3:
        return True
    else:
        return False


# Pre-generate packets to arrive at each agent (Poisson arrival)
arr_rate = 1.0
arrivals = np.zeros((numAgents, numSimulationSteps), dtype=int)
temp = np.zeros(numSimulationSteps)
for k in range(0, numAgents):
    temp = np.random.poisson(arr_rate, numSimulationSteps)
    arrivals[k, :] = temp[:]

plotPacketArrivals(arrivals, 3)

queueLen = np.zeros((numAgents, numSimulationSteps), dtype=int)


def transmitPackets(tx: Agent):
    for indx in tx.sendRequestList:
        if indx < 0 or indx >= tx.queueLen:
            continue
        pkt: Packet = tx.queueingBuffer[indx]
        rx = address2index(pkt.destinationAddr)
        agents[rx].receivePacket(pkt.sourceAddr, pkt.destinationAddr, pkt.payloadSize)
    tx.sendRequestList.clear()


# Now the Earth begins turning
skipList = [5, 6]
positions = np.zeros((numAgents, 2), dtype=float)
links: list[Link] = []
for k in range(0, numSimulationSteps):
    # Move mobile agents
    agents[5].move()
    agents[6].move()
    # Refresh/rebuild neighborhood list for each agent
    for m in range(0, numAgents):
        agents[m].clearPreviousNeighborhood()
    for agts in list(itertools.combinations(agents, 2)):
        distance = findDistance(agts[0], agts[1])
        if evaluateConnectivity(distance, agts[0].r(), agts[1].r()):
            # Shake hand
            agts[0].addNeighbor(agts[1].address)
            agts[1].addNeighbor(agts[0].address)
    # Plot network topology
    for n in range(0, numAgents):
        coord = agents[n].position()
        positions[n, 0] = coord[0]
        positions[n, 1] = coord[1]
    links.clear()
    for agt in agents:
        for nodeAddr in agt.neighbors:
            c1 = agt.position()
            ind = address2index(nodeAddr)
            c2 = agents[ind].position()
            links.append(Link(c1[0], c1[1], c2[0], c2[1]))
    if EXPORT_IMAGE:
        saveSimulationFrame(k, positions, links)
    # Simulate packet arrival at each agent
    n = 0
    for agt in agents:
        if n not in skipList:
            agt.collectPackets(arrivals[agt.id, k])
        agt.dropTimeoutPackets()
        n += 1
    # Transmit packets according to send requests
    for agt in agents:
        transmitPackets(agt)
    # Record queue length history
    n = 0
    for agt in agents:
        queueLen[n, k] = agt.queueLen
        n += 1
plotQueueLen(queueLen, 4)
