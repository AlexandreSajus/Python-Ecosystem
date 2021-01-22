"""
Python-Ecosystem by Alexandre Sajus

More information at:
https://github.com/AlexandreSajus/PythonEcosystem
"""

# run.py takes care of creating the world and animating it

import numpy as np
from random import randint

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from agents import Bunny, Fox


def create_world(h, w, n_bunnies, speed_bunny_min, speed_bunny_max, visibility_bunny, gestChance_bunny,
                 gestStatus_bunny, gestNumber_bunny, age_bunny, n_foxes, speed_fox, visibility_fox, huntStatus_fox, age_fox,
                 hunger_fox, hungerThresMin_fox, hungerThresMax_fox, hungerReward_fox, maxHunger_fox, gestChance_fox,
                 gestStatus_fox, gestNumber_fox):
    """
    Creates an initial world by generating agents with their initial parameters on a h*w 2D grid
    :param h, w: size of the world (height, width)
    :type h, w: Int
    :param parameters of the agents: explained down there
    :type parameters of the agents: Int or Float
    :return: state, 2D array of size h*w with 0 if the spot is empty or the id of an agent if an agent is in the spot
    :rtype: Array
    :return: liveAgents, a dictionary with key=id_of_agent and value=agent
    :rtype: Dict
    """
    state = np.zeros((h, w))
    liveAgents = {}
    for i in range(1, n_bunnies + 1):
        x = randint(0, w - 1)
        y = randint(0, h - 1)
        state[y][x] = i
        liveAgents[i] = Bunny(
            x, y, randint(speed_bunny_min, speed_bunny_max), visibility_bunny, gestChance_bunny, gestStatus_bunny, gestNumber_bunny, age_bunny)

    for j in range(n_bunnies + 1, n_bunnies + 1 + n_foxes):
        x = randint(0, w - 1)
        y = randint(0, h - 1)
        state[y][x] = j
        liveAgents[j] = Fox(x, y, speed_fox, visibility_fox, age_fox, huntStatus_fox,
                            hunger_fox, hungerThresMin_fox, hungerThresMax_fox, hungerReward_fox, maxHunger_fox, gestChance_fox, gestStatus_fox, gestNumber_fox)

    return state, liveAgents


def update_state(state, liveAgents):
    """
    updates state according to liveAgents
    :param state: state, 2D array of size h*w with 0 if the spot is empty or the id of an agent if an agent is in the spot
    :type state: Array
    :param: liveAgents, a dictionary with key=id_of_agent and value=agent
    :type liveAgents: Dict
    :return: state, 2D array of size h*w with 0 if the spot is empty or the id of an agent if an agent is in the spot
    :rtype: Array
    """
    state = np.zeros((len(state), len(state[0])))
    for key in liveAgents:
        agent = liveAgents[key]
        x = agent.x
        y = agent.y
        state[y][x] = key
    return state


def step(t, state, liveAgents):
    """
    Asks every agent to act according to their act function
    :param t: time
    :type t: Int
    :param state: state, 2D array of size h*w with 0 if the spot is empty or the id of an agent if an agent is in the spot
    :type state: Array
    :param: liveAgents, a dictionary with key=id_of_agent and value=agent
    :type liveAgents: Dict
    :return: state, 2D array of size h*w with 0 if the spot is empty or the id of an agent if an agent is in the spot
    :rtype: Array
    """
    for key in liveAgents.copy():
        if key in liveAgents:
            agent = liveAgents[key]
            agent.act(t, state, liveAgents, age_fox)
    state = update_state(state, liveAgents)
    return state


def export(liveAgents):
    """
    Exports the coordinates of the agents in lists readable by matplotlib
    :param: liveAgents, a dictionary with key=id_of_agent and value=agent
    :type liveAgents: Dict
    :return: XBunnies, YBunnies, XFoxes, YFoxes, list of the coordinates of the agents
    :rtype: List
    """
    XBunnies = []
    YBunnies = []
    XFoxes = []
    YFoxes = []
    for key in liveAgents:
        agent = liveAgents[key]
        if isinstance(agent, Bunny):
            XBunnies.append(agent.x)
            YBunnies.append(agent.y)
        elif isinstance(agent, Fox):
            XFoxes.append(agent.x)
            YFoxes.append(agent.y)
    return XBunnies, YBunnies, XFoxes, YFoxes


def count(liveAgents):
    """
    counts living bunnies and foxes and the average bunny speed (for natural selection )
    :param: liveAgents, a dictionary with key=id_of_agent and value=agent
    :type liveAgents: Dict
    :return: liveBunnies, liveFoxes, avgSpeed
    :rtype: Int or Float
    """
    liveBunnies = 0
    liveFoxes = 0
    speed = 0
    for key in liveAgents:
        agent = liveAgents[key]
        if isinstance(agent, Bunny):
            liveBunnies += 1
            speed += agent.speed
        else:
            liveFoxes += 1
    return liveBunnies, liveFoxes, speed/max(liveBunnies, 0.1)


# Initialization of the variables
w = 50  # width of world
h = 50  # height of world
n_bunnies = 100  # number of bunnies
speed_bunny_max = 9  # maximum bunny speed (for natural selection study)
speed_bunny_min = 2  # minimum bunny speed (for natural selection study)
visibility_bunny = 10  # vision range of bunnies
gestChance_bunny = 0.0008  # chance to want to reproduce for bunnies
# reproduction status (0 for don't want to reproduce, 1 elsewise)
gestStatus_bunny = 0
gestNumber_bunny = 3  # bunnies created per reproduction
# bunny age (age decreases over time. If age reaches 0, the agent dies)
age_bunny = 5000
n_foxes = 6  # number of initial foxes
speed_fox = 4  # fox speed
visibility_fox = 100  # vision range of foxes
age_fox = 800  # fox age
huntStatus_fox = 0  # hunting status (0 not on the hunt, 1 elsewise)
# hunger of foxes (hunger decreases over time, If hunger reaches 0, the agent dies)
hunger_fox = 250
# if hunger goes under this threshold, the agent starts hunting
hungerThresMin_fox = 350
hungerThresMax_fox = 450  # if hunger goes over this threshold, the agent stops hunting
hungerReward_fox = 150  # hunger reward per bunny kill
maxHunger_fox = 500  # hunger max limit
gestChance_fox = 0.0004  # chance to want to reproduce for foxes
# reproduction status for bunnies (0 for don't want to reproduce, 1 elsewise)
gestStatus_fox = 0
gestNumber_fox = 1  # foxes created per reproduction

# Change the font size for matplotlib
size = 8
small_size = 6
plt.rc('font', size=size)          # controls default text sizes
plt.rc('axes', titlesize=size)     # fontsize of the axes title
plt.rc('axes', labelsize=small_size)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=small_size)    # fontsize of the tick labels
plt.rc('ytick', labelsize=small_size)    # fontsize of the tick labels
plt.rc('legend', fontsize=small_size)    # legend fontsize
plt.rc('figure', titlesize=small_size)

# Setting up the plots
fig = plt.figure()
ax1 = plt.subplot(221, title="Ecosystem (blue=bunny; red=fox)",
                  xlabel="x (-)", ylabel="y (-)")
plt.xlim(0, w)
plt.ylim(0, h)
bunnies, = ax1.plot([], [], 'bo', ms=3)
foxes, = ax1.plot([], [], 'ro', ms=3)


# Plot to study the evolution of average speed of bunnies over time, for natural selection study
ax2 = plt.subplot(224, title="Average speed of bunnies over time (red=fox speed)",
                  xlabel="time (-)", ylabel="speed (less is faster) (-)")
plt.xlim(0, 5000)
plt.ylim(7, 2)
plt.plot([0, 5000], [speed_fox, speed_fox], color='r')
speedData, = ax2.plot([], [])


ax3 = plt.subplot(222, title="Population over time",
                  xlabel="time (-)", ylabel="population (-)")
plt.xlim(0, 5000)
plt.ylim(0, 200)
popBunnyData, = ax3.plot([], [])
popFoxData, = ax3.plot([], [], color='r')

fig.tight_layout(pad=1.5)


def init():
    """initialize animation"""
    bunnies.set_data([], [])
    foxes.set_data([], [])
    popBunnyData.set_data([], [])
    popFoxData.set_data([], [])
    speedData.set_data([], [])
    return bunnies, foxes, popBunnyData, popFoxData, speedData,


# Create a new world
(state, liveAgents) = create_world(w, h, n_bunnies,
                                   speed_bunny_min, speed_bunny_max, visibility_bunny, gestChance_bunny, gestStatus_bunny,
                                   gestNumber_bunny, age_bunny, n_foxes, speed_fox, visibility_fox, age_fox, huntStatus_fox,
                                   hunger_fox, hungerThresMin_fox, hungerThresMax_fox, hungerReward_fox, maxHunger_fox,
                                   gestChance_fox, gestStatus_fox, gestNumber_fox)
t = 0  # time
T = []
popBunnyList = []
popFoxList = []
speedList = []

# Animation function


def animate(_):
    global t, state, liveAgents
    state = step(t, state, liveAgents)  # execute a step
    t += 1  # increment time
    T.append(t)  # time list for matplotlib

    totalCount = count(liveAgents)
    popBunnyList.append(totalCount[0])  # update the number of live bunnies
    popFoxList.append(totalCount[1])  # update the number of live foxes
    speedList.append(totalCount[2])  # update the average speed of bunnies
    # export the positions of the agents for matplotlib
    (Xbunnies, Ybunnies, XFoxes, YFoxes) = export(liveAgents)

    # Set data for animation
    bunnies.set_data(Xbunnies, Ybunnies)
    foxes.set_data(XFoxes, YFoxes)
    popBunnyData.set_data(T, popBunnyList)
    popFoxData.set_data(T, popFoxList)
    speedData.set_data(T, speedList)

    return bunnies, foxes, popBunnyData, popFoxData, speedData,


# Animation
ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=5, blit=True, init_func=init)

plt.show()
