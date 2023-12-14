# ECE 547 Group Project

import numpy as np
import matplotlib.pyplot as plt

from PacketClass import Link


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


def showLandscape(traj1, traj2, positions, figID: int):
    # Set field size in miles
    L = 1.75 * np.sqrt(2) + 1
    W = 0.5 + 1.75 / np.sqrt(2) + 1.25 + 6 / 8 + 1
    # Extract x, y coordinates
    x0 = positions[:, 0]
    y0 = positions[:, 1]
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
    plt.plot(x0, y0, 'r+', x1, y1, 'k-', x2, y2, 'b--')
    plt.xlim((0, L))
    plt.ylim((0, W))
    ax = plt.gca()
    ax.set_aspect('equal')
    plt.xlabel('X [mile]')
    plt.ylabel('Y [mile]')
    plt.title('Landscape of the field')
    plt.show()


def plotPacketArrivals(data, figNum: int):
    markerTypes = ['.', '+', 'x', 'o', '^']
    myLegends = ['Static Edge Computer 1',
                 'Static Edge Computer 2', 'Static Edge Computer 3',
                 'Static Edge Computer 4', 'Static Edge Computer 5']
    skipList = [5, 6]
    numAgt = data.shape[0]
    numStep = data.shape[1]
    timeStamp = np.linspace(0, numStep-1, numStep)
    fig, axs = plt.subplots(5, 1, sharex='all')
    for k in range(0, numAgt):
        if k in skipList:
            continue
        axs[k].stem(timeStamp, data[k, :])
        axs[k].legend([myLegends[k]])
    plt.xlabel('Time')
    plt.ylabel('Packet arrivals')
    plt.show()


def saveSimulationFrame(figID, coord, links: list[Link]):
    # Set field size in miles
    L = 1.75 * np.sqrt(2) + 1
    W = 0.5 + 1.75 / np.sqrt(2) + 1.25 + 6 / 8 + 1
    # Fetch coordinates
    x = []
    y = []
    for xy in coord:
        x.append(xy[0])
        y.append(xy[1])
    fig = plt.figure(23)
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(x, y, 'r.')
    for lnk in links:
        if lnk.keep(2):
            ax.plot(lnk.x, lnk.y, 'b-')
    ax.set_xlim(0, L)
    ax.set_ylim(0, W)
    ax.set_xlabel('X [mile]')
    ax.set_ylabel('Y [mile]')
    ax.set_aspect('equal')
    fileName_str = r'F:\Sim\S' + str(figID)
    plt.savefig(fileName_str)

def plotQueueLen(data, figNum: int):
    markerTypes = ['.', '+', 'x', 'o', '^', '-', '--']
    myLegends = ['Static Edge Computer 1',
                 'Static Edge Computer 2', 'Static Edge Computer 3',
                 'Static Edge Computer 4', 'Static Edge Computer 5']
    skipList = [5, 6]
    numAgt = data.shape[0]
    numStep = data.shape[1]
    timeStamp = np.linspace(0, numStep-1, numStep)
    fig, axs = plt.subplots(5, 1, sharex='all')
    for k in range(0, numAgt):
        if k in skipList:
            continue
        axs[k].plot(timeStamp, data[k, :], markerTypes[k])
        axs[k].legend([myLegends[k]])
    plt.xlabel('Time')
    plt.ylabel('Queue Length')
    plt.show()
