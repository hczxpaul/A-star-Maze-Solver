__author__ = "Chaozhang Huang"


class Node(object):
    """
    # deprecated Node

    """
    def __init__(self, x=None, y=None, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

    def get_xy(self):
        return self.x, self.y

class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.v = 0

    def __lt__(self, other):
        return True

def get_cost(graph, fromNode, toNode):

    # index 0 = x, index 1 = y
    x1 = fromNode.x
    y1 = fromNode.y
    x2 = toNode.x
    y2 = toNode.y
    weight = 0
    import math
    # moving diagonally
    if abs(x2-x1) + abs(y2-y1) == 2:
        # add cost of fromNode
        if graph[y1][x1] == 0:
            return 999999
        elif graph[y1][x1] == 1:
            weight += math.sqrt(2)/2
        elif graph[y1][x1] == 2:
            weight += math.sqrt(8)/2
        elif graph[y1][x1] == 'a':  #can not move with highway diagonally
            return 999999
        elif graph[y1][x1] == 'b':
            return 999999
        # add cost of toNode
        if graph[y2][x2] == 0:
            return 999999
        elif graph[y2][x2] == 1:
            weight += math.sqrt(2)/2
        elif graph[y2][x2] == 2:
            weight += math.sqrt(8)/2
        elif graph[y2][x2] == 'a':  #can not move with highway diagonally
            return 999999
        elif graph[y2][x2] == 'b':
            return 999999

    # moving vertical or horizontally
    elif abs(x2-x1) + abs(y2-y1) == 1:
        # add cost of fromNode
        if graph[y1][x1] == 0:
            return 999999
        elif graph[y1][x1] == 1:
            weight += 0.5
        elif graph[y1][x1] == 2:
            weight += 1
        elif graph[y1][x1] == 'a':
            weight += 0.125
        elif graph[y1][x1] == 'b':
            weight += 0.25
        # add cost of toNode
        if graph[y2][x2] == 0:
            return 999999
        elif graph[y2][x2] == 1:
            weight += 0.5
        elif graph[y2][x2] == 2:
            weight += 1
        elif graph[y2][x2] == 'a':
            weight += 0.125
        elif graph[y2][x2] == 'b':
            weight += 0.25
    # from == to
    else:
        return 999999

    return weight

def get_curr_cost(graph, curr):

    x1 = curr.x
    y1 = curr.y
    weight = 0
    if graph[y1][x1] == 0:
        return 999999
    elif graph[y1][x1] == 1:
        weight += 0.5
    elif graph[y1][x1] == 2:
        weight += 1
    elif graph[y1][x1] == 'a':
        weight += 0.125
    elif graph[y1][x1] == 'b':
        weight += 0.25
    return weight


def get_neighbors(node):
    neighbors = []
    x = node.x
    y = node.y

    if x != 0 and x != 159 and y != 0 and y != 119:  #normal case, 8 neighbors
        neighbors.append(Node(x, y + 1, node))
        neighbors.append(Node(x, y - 1, node))
        neighbors.append(Node(x - 1, y + 1, node))
        neighbors.append(Node(x - 1, y, node))
        neighbors.append(Node(x - 1, y - 1, node))
        neighbors.append(Node(x + 1, y + 1, node))
        neighbors.append(Node(x + 1, y, node))
        neighbors.append(Node(x + 1, y - 1, node))
    elif x == 0:
        if y == 0:  # 3 neighbors
            neighbors.append(Node(x, y + 1, node))
            neighbors.append(Node(x + 1, y, node))
            neighbors.append(Node(x + 1, y + 1, node))
        elif y == 119:  # 3 neighbors
            neighbors.append(Node(x, y - 1, node))
            neighbors.append(Node(x + 1, y, node))
            neighbors.append(Node(x + 1, y - 1, node))
        else:   # 5 neighbors
            neighbors.append(Node(x, y + 1, node))
            neighbors.append(Node(x, y - 1, node))
            neighbors.append(Node(x + 1, y + 1, node))
            neighbors.append(Node(x + 1, y, node))
            neighbors.append(Node(x + 1, y - 1, node))
    elif x == 159:
        if y == 0:  # 3 neighbors
            neighbors.append(Node(x - 1, y, node))
            neighbors.append(Node(x, y + 1, node))
            neighbors.append(Node(x - 1, y + 1, node))
        elif y == 119:  # 3 neighbors
            neighbors.append(Node(x, y - 1, node))
            neighbors.append(Node(x - 1, y, node))
            neighbors.append(Node(x - 1, y - 1, node))
        else:   # 5 neighbors
            neighbors.append(Node(x, y + 1, node))
            neighbors.append(Node(x, y - 1, node))
            neighbors.append(Node(x - 1, y + 1, node))
            neighbors.append(Node(x - 1, y, node))
            neighbors.append(Node(x - 1, y - 1, node))
    elif y == 0:
        neighbors.append(Node(x, y + 1, node))
        neighbors.append(Node(x + 1, y + 1, node))
        neighbors.append(Node(x + 1, y, node))
        neighbors.append(Node(x - 1, y + 1, node))
        neighbors.append(Node(x - 1, y, node))
    elif y == 119:
        neighbors.append(Node(x, y - 1, node))
        neighbors.append(Node(x - 1, y, node))
        neighbors.append(Node(x - 1, y - 1, node))
        neighbors.append(Node(x + 1, y, node))
        neighbors.append(Node(x + 1, y - 1, node))

    return neighbors


'''
def get_neighbors(node):
    neighbors = []
    x = node.x
    y = node.y

    if x != 0 and x != 9 and y != 0 and y != 9:  #normal case, 8 neighbors
        neighbors.append(Node(x, y + 1, node))
        neighbors.append(Node(x, y - 1, node))
        neighbors.append(Node(x - 1, y + 1, node))
        neighbors.append(Node(x - 1, y, node))
        neighbors.append(Node(x - 1, y - 1, node))
        neighbors.append(Node(x + 1, y + 1, node))
        neighbors.append(Node(x + 1, y, node))
        neighbors.append(Node(x + 1, y - 1, node))
    elif x == 0:
        if y == 0:  # 3 neighbors
            neighbors.append(Node(x, y + 1, node))
            neighbors.append(Node(x + 1, y, node))
            neighbors.append(Node(x + 1, y + 1, node))
        elif y == 9:  # 3 neighbors
            neighbors.append(Node(x, y - 1, node))
            neighbors.append(Node(x + 1, y, node))
            neighbors.append(Node(x + 1, y - 1, node))
        else:   # 5 neighbors
            neighbors.append(Node(x, y + 1, node))
            neighbors.append(Node(x, y - 1, node))
            neighbors.append(Node(x + 1, y + 1, node))
            neighbors.append(Node(x + 1, y, node))
            neighbors.append(Node(x + 1, y - 1, node))
    elif x == 9:
        if y == 0:  # 3 neighbors
            neighbors.append(Node(x - 1, y, node))
            neighbors.append(Node(x, y + 1, node))
            neighbors.append(Node(x - 1, y + 1, node))
        elif y == 9:  # 3 neighbors
            neighbors.append(Node(x, y - 1, node))
            neighbors.append(Node(x - 1, y, node))
            neighbors.append(Node(x - 1, y - 1, node))
        else:   # 5 neighbors
            neighbors.append(Node(x, y + 1, node))
            neighbors.append(Node(x, y - 1, node))
            neighbors.append(Node(x - 1, y + 1, node))
            neighbors.append(Node(x - 1, y, node))
            neighbors.append(Node(x - 1, y - 1, node))
    elif y == 0:
        neighbors.append(Node(x, y + 1, node))
        neighbors.append(Node(x + 1, y + 1, node))
        neighbors.append(Node(x + 1, y, node))
        neighbors.append(Node(x - 1, y + 1, node))
        neighbors.append(Node(x - 1, y, node))
    elif y == 9:
        neighbors.append(Node(x, y - 1, node))
        neighbors.append(Node(x - 1, y, node))
        neighbors.append(Node(x - 1, y - 1, node))
        neighbors.append(Node(x + 1, y, node))
        neighbors.append(Node(x + 1, y - 1, node))

    return neighbors
'''




