from random import randint, random
from math import sqrt, inf
from copy import deepcopy


def distance(agent1, agent2):
    return max(sqrt((agent1.x - agent2.x)**2 + (agent1.y - agent2.y)**2), 0.1)


def unitVector(agent1, agent2):
    d = distance(agent1, agent2)
    return ((agent2.x - agent1.x)/d, (agent2.y - agent1.y)/d)


def legalMove(move, state):
    yMax = len(state)
    xMax = len(state[0])
    if move[0] < 0 or move[0] >= xMax:
        return False
    if move[1] < 0 or move[1] >= yMax:
        return False
    return True


def moveTowards(agent, agentT, state, direction):
    u = unitVector(agent, agentT)
    xU = u[0]
    yU = u[1]
    if abs(xU) >= abs(yU):
        if xU > 0:
            xU = 1*direction
        else:
            xU = -1*direction
        move = (agent.x + xU, agent.y)
        if legalMove(move, state):
            (agent.x, agent.y) = move
        else:
            randomMovement(agent, state)
    else:
        if yU > 0:
            yU = 1*direction
        else:
            yU = -1*direction
        move = (agent.x, agent.y + yU)
        if legalMove(move, state):
            (agent.x, agent.y) = move
        else:
            randomMovement(agent, state)


def randomMovement(agent, state):
    r = randint(0, 3)
    x = agent.x
    y = agent.y
    moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    move = moves[r]
    if legalMove(move, state):
        (agent.x, agent.y) = move
    else:
        randomMovement(agent, state)


def detectPrey(agent, liveAgents, animal):
    minPrey = None
    minDist = inf
    minKey = None
    for key in liveAgents:
        prey = liveAgents[key]
        if prey != agent:
            if isinstance(prey, animal):
                dist = distance(agent, prey)
                if dist <= agent.visibility and dist < minDist:
                    minPrey = prey
                    minDist = dist
                    minKey = key
    return minPrey, minKey


class bunny:
    def __init__(self, x, y, speed, visibility, gestChance, gestStatus, gestNumber):
        self.x = x
        self.y = y
        self.speed = speed
        self.visibility = visibility
        self.gestChance = gestChance
        self.gestStatus = gestStatus
        self.gestNumber = gestNumber

    def act(self, t, state, liveAgents):
        if t % self.speed == 0:
            minFox, minFKey = detectPrey(self, liveAgents, fox)
            if minFox != None:
                moveTowards(self, minFox, state, -1)
            elif self.gestStatus == 0:
                self.gestStatus = int(random() < self.gestChance)
                randomMovement(self, state)
            else:
                minPrey, minKey = detectPrey(self, liveAgents, bunny)
                if minPrey != None:
                    moveTowards(self, minPrey, state, 1)
                    if self.x == minPrey.x and self.y == minPrey.y:
                        self.gestStatus = 0
                        maxKey = 0
                        for key in liveAgents:
                            if key > maxKey:
                                maxKey = key
                        for i in range(self.gestNumber):
                            liveAgents[maxKey + i + 1] = deepcopy(self)

                else:
                    randomMovement(self, state)


class fox:
    def __init__(self, x, y, speed, visibility):
        self.x = x
        self.y = y
        self.speed = speed
        self.visibility = visibility

    def act(self, t, state, liveAgents):
        if t % self.speed == 0:
            minPrey, minKey = detectPrey(self, liveAgents, bunny)
            if minPrey != None:
                moveTowards(self, minPrey, state, 1)
                if self.x == minPrey.x and self.y == minPrey.y:
                    liveAgents.pop(minKey, None)
