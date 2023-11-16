# ECE 547 Group Project
# Python 3.11.3
# NumPy 1.24.3

import itertools

import numpy as np
import matplotlib.pyplot as plt
from AgentClass import Agent
from Visualizer import showTrajectories

numFixedAgents = 5
numSimulationSteps = 10

# Set field size in miles
L = 1.75 * np.sqrt(2) + 1
W = 0.5 + 1.75 / np.sqrt(2) + 1.25 + 6 / 8 + 1

# Set up data containers
agents: list[Agent] = []

# Introduce field sensors
fixedAgentPositions = np.genfromtxt('fixed_agents_coord_list.csv', delimiter=',')
for k in range(0, numFixedAgents):
    agents.append(Agent(mobile=False, name=k, rng=2.0))
for k in range(0, numFixedAgents):
    x1 = fixedAgentPositions[k, 0]
    y1 = fixedAgentPositions[k, 1]
    agents[k].setPosition(x1, y1)

# Print info of all field sensors
print('Coordinates of all field sensors:')
for fix in agents:
    print(fix.position())

# Introduce a tractor
agents.append(Agent(mobile=True, name=5, rng=2.0))
agents[5].loadTrajectory('tractor1_trajectory.csv')

# Introduce a scouting drone
agents.append(Agent(mobile=True, name=6, rng=1.0))
agents[6].loadTrajectory('drone1_trajectory.csv')
numAgents = len(agents)

traj1 = agents[5].trajectory
traj2 = agents[6].trajectory
showTrajectories(traj1, traj2, 1)


def findDistance(agent1: Agent, agent2: Agent) -> float:
    coord1 = agent1.position()
    coord2 = agent2.position()
    dist = np.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[0] - coord2[1]) ** 2)
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

# Now the Earth begins turning
for k in range(0, numSimulationSteps):
    print(f'Step {k+1}:', end='')
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
    # Simulate packet arrival at each agent
    for agt in agents:
        agt.collectPackets(arrivals[agt.id, k])
        agt.dropTimeoutPackets()


