# ECE 547 Group Project
# Python 3.11.3
# NumPy 1.24.3

import itertools

import numpy as np
import matplotlib.pyplot as plt
from FixedSensor import FieldSensor_class
from TractorClass import tractor_class
from DroneClass import drone_class
from Visualizer import showTrajectories

numFixedAgents = 5
numSimulationSteps = 100

# Set field size in miles
L = 1.75 * np.sqrt(2) + 1
W = 0.5 + 1.75 / np.sqrt(2) + 1.25 + 6 / 8 + 1

# Set up data containers
agents: list = []

# Introduce field sensors
fixedAgentPositions = np.genfromtxt('fixed_agents_coord_list.csv', delimiter=',')

for k in range(0, numFixedAgents):
    x1 = fixedAgentPositions[k, 0]
    y1 = fixedAgentPositions[k, 1]
    agents.append(FieldSensor_class(x1, y1))

# Print info of all field sensors
print('Coordinates of all field sensors:')
for fix in agents:
    fix.dispCoordinates()

# Introduce a tractor
tractor = tractor_class('tractor1_trajectory.csv')
tractor.loadTrajectory()
agents.append(tractor)

# Introduce a scouting drone
drone = drone_class('drone1_trajectory.csv')
drone.loadTrajectory()
agents.append(drone)

traj1 = tractor.trajectory
traj2 = drone.trajectory
showTrajectories(traj1, traj2, 1)

# Now the Earth begins turning
for k in range(0, numSimulationSteps):
    print(f'Step {k+1}:')
    tractor.move()
    drone.move()
    count = 0
    for agt in list(itertools.combinations(agents, 2)):
        count += 1
        print(count)
