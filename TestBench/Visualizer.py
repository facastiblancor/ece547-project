# ECE 547 Group Project

import numpy as np
import matplotlib.pyplot as plt


def showTrajectories(traj1, traj2, figID: int):
    # Set field size in miles
    L = 1.75 * np.sqrt(2) + 1
    W = 0.5 + 1.75 / np.sqrt(2) + 1.25 + 6 / 8 + 1
    # Extract x, y coordinates
    x1 = np.zeros(traj1.shape[0])
    y1 = np.zeros(traj1.shape[0])
    x1[:] = traj1[:, 0]
    y1[:] = traj1[:, 1]
    x2 = np.zeros(traj2.shape[0])
    y2 = np.zeros(traj2.shape[0])
    x2[:] = traj2[:, 0]
    y2[:] = traj2[:, 1]
    # Plot trajectories
    plt.figure(figID)
    plt.plot(x1, y1, 'k+-', x2, y2, 'bx')
    plt.xlim((0, L))
    plt.ylim((0, W))
    ax = plt.gca()
    ax.set_aspect('equal')
    plt.xlabel('X [mile]')
    plt.ylabel('Y [mile]')
    plt.title('Landscape of the field')
    plt.show()
