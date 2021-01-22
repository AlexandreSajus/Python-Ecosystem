"""
Python-Ecosystem by Alexandre Sajus

More information at:
https://github.com/AlexandreSajus/PythonEcosystem

agents.py takes care of managing the behaviour of the animals
"""


from random import randint, random
from math import sqrt, inf
from copy import deepcopy


def distance(agent1, agent2):
    """
    Measures the distance between two agents
    :param agent1, agent2: an animal, bunny or fox
    :type agent1, agent2: Object
    :return: distance
    :rtype: Float
    """
    return max(sqrt((agent1.x - agent2.x)**2 + (agent1.y - agent2.y)**2), 0.1)


def unit_vector(agent1, agent2):
    """
    Returns the unit vector from agent1 to agent2
    :param agent1, agent2: an animal, bunny or fox
    :type agent1, agent2: Object
    :return: unit vector (x, y)
    :rtype: Tuple
    """
    d = distance(agent1, agent2)
    return (agent2.x - agent1.x)/d, (agent2.y - agent1.y)/d


def legal_move(move, state):
    """
    Checks if the move is possible and is not out of bounds
    :param move: next potential position for an agent (x, y)
    :type move: Tuple
    :param state: state, 2D array of size h*w with 0 if the spot is empty or the id of an agent if an agent is in the spot
    :type state: Array
    :return: True if the move is legal, False elsewise
    :rtype: Bool
    """
    yMax = len(state)
    xMax = len(state[0])
    return 0 <= move[0] < xMax and 0 <= move[1] < yMax


def move_towards(agent, agentT, state, direction):
    """
    Move agent towards agentT. If the move is illegal, move randomly
    :param agent, agentT: an animal, fox or bunny
    :type agent, agentT: Object
    :param state: state, 2D array of size h*w with 0 if the spot is empty or the id of an agent if an agent is in the spot
    :type state: Array
    :param direction: 1 if agent wants to move towards agentT, -1 if agent wants to run away from agentT
    :type direction: int
    """
    xU, yU = unit_vector(agent, agentT)
    if abs(xU) >= abs(yU):
        if xU > 0:
            xU = 1*direction
        else:
            xU = -1*direction
        move = (agent.x + xU, agent.y)
        if legal_move(move, state):
            (agent.x, agent.y) = move
        else:
            random_movement(agent, state)
    else:
        if yU > 0:
            yU = 1*direction
        else:
            yU = -1*direction
        move = (agent.x, agent.y + yU)
        if legal_move(move, state):
            (agent.x, agent.y) = move
        else:
            random_movement(agent, state)


def random_movement(agent, state):
    """
    Move randomly where it is legal to move
    :param agent: an animal, fox or bunny
    :type agent: Object
    :param state: state, 2D array of size h*w with 0 if the spot is empty or the id of an agent if an agent is in the spot
    :type state: Array
    """
    r = randint(0, 3)
    x = agent.x
    y = agent.y
    moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    move = moves[r]
    if legal_move(move, state):
        (agent.x, agent.y) = move
    else:
        random_movement(agent, state)


def detect_prey(agent, liveAgents, animal):
    """
    Detects if agent can see an instance of type animal in his visibility range
    :param agent: an animal, fox or bunny
    :type agent: Object
    :param: liveAgents, a dictionary with key=id_of_agent and value=agent
    :type liveAgents: Dict
    :param: animal: fox or bunny class
    :type: animal: Class
    """
    minPrey = None
    minDist = inf
    minKey = None
    for key, prey in liveAgents.items():
        if prey != agent and isinstance(prey, animal):
            dist = distance(agent, prey)
            if minDist > dist <= agent.visibility:
                minPrey = prey
                minDist = dist
                minKey = key
    return minPrey, minKey


class Animal:
    def __init__(self, x, y, speed, visibility, gestChance, gestStatus, gestNumber, age):
        self.x = x
        self.y = y
        self.speed = speed
        self.visibility = visibility
        self.gestChance = gestChance
        self.gestStatus = gestStatus
        self.gestNumber = gestNumber
        self.age = age


class Bunny(Animal):
    """
    Bunny class, its variables are explained in run.py
    """

    def act(self, t, state, liveAgents, age_bunny):
        """
        act controls the behavior of the agent at every step of the simulation
        """
        self.age -= 1  # decrease the age (if age reaches 0, the agent dies)
        if self.age == 0:  # kill the agent if age reaches O
            for key, agent in liveAgents.items():
                if agent == self:
                    liveAgents.pop(key, None)
                    break
        # the agent can only act on some values of t (time), the frequency of these values are defined by speed
        if t % self.speed == 0:
            # check for foxes in the area
            minFox, minFKey = detect_prey(self, liveAgents, Fox)
            if minFox is not None:  # if there is a fox, run away
                move_towards(self, minFox, state, -1)
            elif self.gestStatus == 0:  # if there is no fox and the agent doesn't want to reproduce, move randomly
                # random chance to want to reproduce next turn
                self.gestStatus = int(random() < self.gestChance)
                random_movement(self, state)
            else:
                # if the agent wants to reproduce, find another bunny
                minPrey, minKey = detect_prey(self, liveAgents, Bunny)
                if minPrey is not None:
                    move_towards(self, minPrey, state, 1)
                    if self.x == minPrey.x and self.y == minPrey.y:  # if a bunny has been found, reproduce
                        self.gestStatus = 0
                        maxKey = max(liveAgents)  # find an unassigned key in liveAgents for the newborns

                        for i in range(self.gestNumber):
                            # the newborns are a copy of the parent
                            liveAgents[maxKey + i + 1] = deepcopy(self)
                            # reset the age of the newborns
                            liveAgents[maxKey + i + 1].age = age_bunny

                else:  # if no partner found, move randomly
                    random_movement(self, state)


class Fox(Animal):
    """
    Fox class, its variables are explained in run.py
    """
    def __init__(self, x, y, speed, visibility, age, huntStatus, hunger, hungerThresMin, hungerThresMax, hungerReward, maxHunger,
                 gestChance, gestStatus, gestNumber):
        super(Fox, self).__init__(x, y, speed, visibility, gestChance, gestStatus, gestNumber, age)
        self.huntStatus = huntStatus
        self.hunger = hunger
        self.hungerThresMin = hungerThresMin
        self.hungerThresMax = hungerThresMax
        self.hungerReward = hungerReward
        self.maxHunger = maxHunger

    def act(self, t, state, liveAgents, age_fox):
        """
         act controls the behavior of the agent at every step of the simulation
        """
        self.age -= 1  # decrease age (if age reaches O, the agent dies)
        # decrease hunger (if hunger reaches O, the agent dies)
        self.hunger -= 1
        # hunger can't go over maxHunger
        self.hunger = min(self.maxHunger, self.hunger)
        if self.age == 0 or self.hunger == 0:  # kill the agent in case of starvation or aging
            for key, agent in liveAgents.items():
                if agent == self:
                    liveAgents.pop(key, None)
                    break
        # the agent can only act on some values of t (time), the frequency of these values are defined by speed
        if t % self.speed == 0:
            if self.huntStatus == 0:  # if not hunting
                if self.hunger <= self.hungerThresMin:  # if hunger goes under thresholdMin, go hunting
                    self.huntStatus = 1
                if self.gestStatus == 1:  # if the agent wants to reproduce, find another fox
                    minPrey, minKey = detect_prey(self, liveAgents, Fox)
                    if minPrey is not None:
                        move_towards(self, minPrey, state, 1)
                        if self.x == minPrey.x and self.y == minPrey.y:  # if another fox is found, reproduce
                            self.gestStatus = 0
                            maxKey = max(liveAgents)  # find an unassigned key for the newborns

                            for i in range(self.gestNumber):
                                # the newborns are copies of the parent
                                liveAgents[maxKey + i + 1] = deepcopy(self)
                                # reset the age of the newborns
                                liveAgents[maxKey + i + 1].age = age_fox
                elif self.gestChance > random():  # random chance to want to reproduce
                        self.gestStatus = 1
            else:  # if the agent wants to hunt
                if self.hunger >= self.hungerThresMax:  # if hunger goes over thresholdMax, stop hunting
                    self.huntStatus = 0
                minPrey, minKey = detect_prey(
                    self, liveAgents, Bunny)  # find a prey
                if minPrey is not None:
                    move_towards(self, minPrey, state, 1)
                    if self.x == minPrey.x and self.y == minPrey.y:  # if the agent is on the prey, kill the prey
                        liveAgents.pop(minKey, None)
                        self.hunger += self.hungerReward
