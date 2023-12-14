# ECE 547 Group Project
# Python 3.11.3
# NumPy 1.24.3

import itertools

import numpy as np
from AgentClass import Agent
from Visualizer import showTrajectories, showLandscape
from Visualizer import plotPacketArrivals, saveSimulationFrame
from Visualizer import plotQueueLen, plotQueueLen_saveFrame
from PacketClass import Packet, Link

ENABLE_ROUTING: bool = True
EXPORT_IMAGES: bool = False
topology_snapshot_directory: str = r'F:\Sim\S'
queueStatus_snapshot_directory: str = r'F:\Sim1\S'

numSimulationSteps: int = 100

rng1 = 1.0
rng2 = 1.0
rng3 = 1.0

# Set field size in miles
L = 1.75 * np.sqrt(2) + 1
W = 0.5 + 1.75 / np.sqrt(2) + 1.25 + 6 / 8 + 1

# Set up data containers
agents: list[Agent] = []

# Introduce field sensors
fixedAgentPositions = np.genfromtxt('fixed_agents_coord_list.csv', delimiter=',')
numFixedAgents = fixedAgentPositions.shape[0]
for k in range(0, numFixedAgents):
    agents.append(Agent(mobile=False, name=k, rng=rng1))
    x1 = fixedAgentPositions[k, 0]
    y1 = fixedAgentPositions[k, 1]
    agents[k].setPosition(x1, y1)

# Print info of all field sensors
print('Coordinates of all field sensors:')
for fix in agents:
    print(fix.position())

# Introduce a tractor
agents.append(Agent(mobile=True, name=5, rng=rng2, stepSize=5))
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
    temp1: float = (coord1[0] - coord2[0]) ** 2
    temp2: float = (coord1[1] - coord2[1]) ** 2
    dist: float = np.sqrt(temp1 + temp2)
    return dist


def evaluateConnectivity(dist, r1, r2) -> bool:
    return dist <= np.min([r1, r2])


# Pre-generate packets to arrive at each agent (Poisson arrival)
arr_rate = 1.0
arrivals = np.zeros((numAgents, numSimulationSteps), dtype=int)
temp = np.zeros(numSimulationSteps)
for k in range(0, numAgents):
    temp = np.random.poisson(arr_rate, numSimulationSteps)
    arrivals[k, :] = temp[:]

plotPacketArrivals(arrivals, 3)

# Runtime data and containers
skipList = [5, 6]
queueLen = np.zeros((numAgents, numSimulationSteps), dtype=int)
totalNumPackets: int = 0
numACK: int = 0
numDroppedPackets: int = 0
positions = np.zeros((numAgents, 2), dtype=float)
runtime_data_rec = np.zeros((numSimulationSteps, 3), dtype=int)
links: list[Link] = []


def transmitPackets(tx: Agent) -> tuple:
    m_ack: int = 0
    m_drp: int = 0
    m_k = 0
    for indx in tx.sendRequestList:
        if indx < 0 or indx >= tx.queueLen:
            continue
        pkt: Packet = tx.queueingBuffer[indx]
        rx = address2index(tx.nextStopList[m_k])
        key = agents[rx].receivePacket(pkt.sourceAddr, pkt.destinationAddr, pkt.payloadSize)
        if key == 1:
            m_ack += 1
        elif key == -1:
            m_drp += 1
        m_k += 1
    tx.completeTransmission()
    return m_ack, m_drp


# Now the Earth begins turning
for k in range(0, numSimulationSteps):
    print(f'Step{k+1}', end='')
    # Move mobile agents
    for agt in agents:
        if agt.mobility:
            agt.move()
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
    if EXPORT_IMAGES:
        saveSimulationFrame(k, positions, links, topology_snapshot_directory)
    # Simulate packet arrival at each agent
    n = 0
    for agt in agents:
        timeout = 0
        overflow = 0
        if n not in skipList:
            overflow = agt.collectPackets(arrivals[n, k])
            totalNumPackets += arrivals[n, k]
            timeout = agt.dropTimeoutPackets()
        numDroppedPackets += timeout
        numDroppedPackets += overflow
        n += 1
    if ENABLE_ROUTING:
        # Execute routing policy
        for agt in agents:
            agt.route()
            print('.', end='')
        # Transmit packets according to send requests
        for agt in agents:
            temp = transmitPackets(agt)
            numACK += temp[0]
            numDroppedPackets += temp[1]
            print('|', end='')
    # Record runtime data history
    n = 0
    for agt in agents:
        queueLen[n, k] = agt.queueLen
        n += 1
    runtime_data_rec[k, 0] = totalNumPackets
    runtime_data_rec[k, 1] = numACK
    runtime_data_rec[k, 2] = numDroppedPackets
    if EXPORT_IMAGES:
        plotQueueLen_saveFrame(queueLen, k, queueStatus_snapshot_directory)
    print(';')
plotQueueLen(queueLen, 4)
np.savetxt('runtime_data.csv', runtime_data_rec, delimiter=',')
print(f'Success: {numACK}/{totalNumPackets}.')
