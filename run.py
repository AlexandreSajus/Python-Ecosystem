import numpy as np
from random import randint

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from agents import bunny, fox


def createWorld(h, w, n_bunnies, speed_bunny_min, speed_bunny_max, visibility_bunny, gestChance_bunny, gestStatus_bunny, gestNumber_bunny, n_foxes, speed_fox, visibility_fox):
    state = np.zeros((h, w))
    liveAgents = {}
    for i in range(1, n_bunnies + 1):
        x = randint(0, w - 1)
        y = randint(0, h - 1)
        state[y][x] = i
        liveAgents[i] = bunny(
            x, y, randint(speed_bunny_min, speed_bunny_max), visibility_bunny, gestChance_bunny, gestStatus_bunny, gestNumber_bunny)

    for j in range(n_bunnies + 1, n_bunnies + 1 + n_foxes):
        x = randint(0, w - 1)
        y = randint(0, h - 1)
        state[y][x] = j
        liveAgents[j] = fox(x, y, speed_fox, visibility_fox)

    return state, liveAgents


def updateState(state, liveAgents):
    state = np.zeros((len(state), len(state[0])))
    for key in liveAgents:
        agent = liveAgents[key]
        x = agent.x
        y = agent.y
        state[y][x] = key
    return state


def step(t, state, liveAgents):
    for key in liveAgents.copy():
        if key in liveAgents:
            agent = liveAgents[key]
            agent.act(t, state, liveAgents)
    state = updateState(state, liveAgents)
    return state


def export(liveAgents):
    XBunnies = []
    YBunnies = []
    XFoxes = []
    YFoxes = []
    for key in liveAgents:
        agent = liveAgents[key]
        if isinstance(agent, bunny):
            XBunnies.append(agent.x)
            YBunnies.append(agent.y)
        elif isinstance(agent, fox):
            XFoxes.append(agent.x)
            YFoxes.append(agent.y)
    return XBunnies, YBunnies, XFoxes, YFoxes


def count(liveAgents):
    liveBunnies = 0
    liveFoxes = 0
    speed = 0
    for key in liveAgents:
        agent = liveAgents[key]
        if isinstance(agent, bunny):
            liveBunnies += 1
            speed += agent.speed
        else:
            liveFoxes += 1
    return liveBunnies, liveFoxes, speed/liveBunnies


w = 50
h = 50
n_bunnies = 60
speed_bunny_max = 9
speed_bunny_min = 4
visibility_bunny = 10
gestChance_bunny = 0.004
gestStatus_bunny = 0
gestNumber_bunny = 3
n_foxes = 8
speed_fox = 5
visibility_fox = 50

SIZE = 8
plt.rc('font', size=SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SIZE)    # legend fontsize
plt.rc('figure', titlesize=SIZE)

fig = plt.figure()
ax1 = plt.subplot(221, title="Ecosystem (blue=bunny; red=fox)",
                  xlabel="x (-)", ylabel="y (-)")
plt.xlim(0, w)
plt.ylim(0, h)
bunnies, = ax1.plot([], [], 'bo', ms=3)
foxes, = ax1.plot([], [], 'ro', ms=3)
ax2 = plt.subplot(222, title="Average speed of bunnies over time (red=fox speed)",
                  xlabel="time (-)", ylabel="speed (less is faster) (-)")
plt.xlim(0, 3000)
plt.ylim(8, 4)
plt.plot([0, 5000], [speed_fox, speed_fox], color='r')
speedData, = ax2.plot([], [])
ax3 = plt.subplot(224, title="Bunny population over time",
                  xlabel="time (-)", ylabel="population (-)")
plt.xlim(0, 3000)
plt.ylim(0, 500)
popData, = ax3.plot([], [])

fig.tight_layout(pad=1.5)


def init():
    """initialize animation"""
    bunnies.set_data([], [])
    foxes.set_data([], [])
    speedData.set_data([], [])
    popData.set_data([], [])
    return bunnies, foxes, speedData,


(state, liveAgents) = createWorld(w, h, n_bunnies,
                                  speed_bunny_min, speed_bunny_max, visibility_bunny, gestChance_bunny, gestStatus_bunny, gestNumber_bunny, n_foxes, speed_fox, visibility_fox)
t = 0
T = []
speedList = []
popList = []


def animate(i):
    global t, state, liveAgents
    state = step(t, state, liveAgents)
    t += 1
    T.append(t)
    totalCount = count(liveAgents)
    speedList.append(totalCount[2])
    popList.append(totalCount[0])
    print(t, count(liveAgents))
    (Xbunnies, Ybunnies, XFoxes, YFoxes) = export(liveAgents)
    bunnies.set_data(Xbunnies, Ybunnies)
    foxes.set_data(XFoxes, YFoxes)
    speedData.set_data(T, speedList)
    popData.set_data(T, popList)
    return bunnies, foxes, speedData, popData


ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=10, blit=True, init_func=init)

plt.show()
