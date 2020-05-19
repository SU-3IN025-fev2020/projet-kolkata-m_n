import heapq


class Node:
    def __init__(self, state, g, father, states):
        self.state = state
        self.g = g
        self.father = father
        self.states = states  # 0 goal, 1 wall ,

    def isGoal(self):

        if self.state == self.states[0]:
            return True
        return False


    def isWall(self):
        if self.state in self.states[1]:
            return True
        return False


    def expand(self):
        l = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        nodes = []
        for p in l:
            self.state[1] + p[1]
            next_row = self.state[0] + p[0]
            next_col = self.state[1] + p[1]
            if (next_row, next_col) not in self.states[1] and 0 <= next_row <= 20 and 0 <= next_col <= 20:
                nodes.append(Node((next_row, next_col), self.g + 1, self, self.states))

        return nodes



    def key(self):
        return self.state[0] * 10 + self.state[1]

    def heuristic(self):
        return abs(self.state[0] - self.states[0][0]) + abs(self.state[1] - self.states[0][1])


def aStar(states):  # 0 init, 1 goal ,2 wall
    row, col = states[0][0], states[0][1]
    initNode = Node((row, col), 0, None, (states[1], states[2]))
    border = [(initNode.g + initNode.heuristic(), initNode)]
    reserve = {}
    current = initNode

    while len(border) > 0 and not current.isGoal():
        (minf , current) = heapq.heappop(border)
        if current.state not in reserve:
            reserve[current.state] = current.g
            newNodes = current.expand()
            for n in newNodes:
                heapq.heappush(border, (n.g + n.heuristic(), n))

    node = current
    path = []
    path.append(current.state)
    while True:
        if node.father != None :
            path.append(node.father.state)
            node = node.father
        else:
            break
    path.reverse()
    return path