# ECE 547 Group Project
# Python 3.11.3
# NumPy 1.24.3

import numpy as np
import matplotlib.pyplot as plt
from FixedSensor import FieldSensor
from Tractor import tractor

numFixedAgents = 5

# Set field size in miles
L = 1.75 * np.sqrt(2) + 1
W = 0.5 + 1.75 / np.sqrt(2) + 1.25 + 6 / 8 + 1

# Set up data containers
fixed: list[FieldSensor] = []

# Load test bed assumption data
fixedAgentPositions = np.genfromtxt('fixed_agents_coord_list.csv', delimiter=',')

for k in range(0, numFixedAgents):
    x = fixedAgentPositions[k, 0]
    y = fixedAgentPositions[k, 1]
    fixed.append(FieldSensor(x, y))

# Print info of all field sensors
print('Coordinates of all field sensors:')
for fix in fixed:
    fix.dispCoordinates()

# Introduce a tractor
trac = tractor('tractor1_trajectory.csv')
