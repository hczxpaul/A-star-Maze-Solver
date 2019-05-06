__author__ = "Chaozhang Huang"


from node import *
import heapq

class Abstract_Heuristic(object):
    start = None
    goal = None
    node_expanded = 0
    memreq = 0
    max_memreq = 0
    def __init__(self, graph):
        self.fringe = []
        heapq.heapify(self.fringe)
        self.visited = set()
        self.cells = []
        self.grid_height = 120  #120
        self.grid_width = 160   #160
        self.graph = graph
        self.init_graph()

    def init_graph(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                self.cells.append(Cell(x, y))

    def get_cell(self, x, y):
        return self.cells[y * self.grid_width + x]

    def get_neighbor_cells(self, cell):
        neighborsNodes = get_neighbors(cell)
        neighbors = []
        for i in neighborsNodes:
            neighbors.append(self.get_cell(i.x, i.y))
        return neighbors

    def update_graph(self):
        cell = self.goal
        grid = self.graph
        #mark start
        print(self.start.x, self.start.y)
        if grid[self.start.y][self.start.x] == 1:
            grid[self.start.y][self.start.x] = 'p'
        elif grid[self.start.y][self.start.x] == 2:
            grid[self.start.y][self.start.x] = 'q'
        elif grid[self.start.y][self.start.x] == 'a':
            grid[self.start.y][self.start.x] = 'r'
        elif grid[self.start.y][self.start.x] == 'b':
            grid[self.start.y][self.start.x] = 's'
        #mark path
        while cell is not self.start and cell is not None:
            if grid[cell.y][cell.x] == 1:
                grid[cell.y][cell.x] = 'p'
            elif grid[cell.y][cell.x] == 2:
                grid[cell.y][cell.x] = 'q'
            elif grid[cell.y][cell.x] == 'a':
                grid[cell.y][cell.x] = 'r'
            elif grid[cell.y][cell.x] == 'b':
                grid[cell.y][cell.x] = 's'
            cell = cell.parent

        return grid

    def init_start_goal(self, start, goal):
        # add start to fringe
        self.start = self.get_cell(start[0],start[1])
        self.goal = self.get_cell(goal[0],goal[1])

    def getNodeExpand(self):
        return self.node_expanded

    def getMemReq(self):
        return self.max_memreq

    def incMemReq(self):
        self.memreq += 1
        if(self.memreq > self.max_memreq):
            self.max_memreq = self.memreq

    def update_cell(self, fromCell, toCell, weight):
        if fromCell.g + get_cost(self.graph, fromCell, toCell) < toCell.g:
            toCell.g = fromCell.g + get_cost(self.graph, fromCell, toCell)
            toCell.parent = fromCell
            if (toCell.f, toCell) in self.fringe:
                self.fringe.remove((toCell.f, toCell))
            toCell.h = self.get_h(toCell)
            toCell.f = weight * toCell.h + toCell.g
            heapq.heappush(self.fringe, (toCell.f, toCell))
            self.incMemReq()

    def search(self,start,goal,weight):
        self.init_start_goal(start,goal)
        heapq.heappush(self.fringe, (self.start.f, self.start))
        self.incMemReq()
        while len(self.fringe):
            # pop one from fringe
            f, cell = heapq.heappop(self.fringe)
            self.memreq -=1
            # add cell to visited list
            self.visited.add(cell)
            self.node_expanded += 1
            # if found GOAL, do sth
            if cell is self.goal:
                return self.update_graph()
            # get neighbors
            neighbors = self.get_neighbor_cells(cell)
            for neighbor in neighbors:
                if neighbor not in self.visited:
                    if (neighbor.f, neighbor) not in self.fringe:
                        neighbor.g = 999999
                        neighbor.parent = None
                        # add neighbor to fringe
                    self.update_cell(cell, neighbor,weight)
        return self.update_graph()

class UCS(Abstract_Heuristic):

    def get_h(self,curr):
        return 0

class AsMan(Abstract_Heuristic):

    def get_h(self, curr):
        return 0.25*(abs(curr.x - self.goal.x) + abs(curr.y - self.goal.y))

class AsCostMan(Abstract_Heuristic):

    def get_h(self, curr):
        dx = abs(curr.x - self.goal.x)
        dy = abs(curr.y - self.goal.y)

        return 2*get_curr_cost(self.graph,curr)* (dx + dy)

class AsEu(Abstract_Heuristic):
    def get_h(self, curr):
        import math
        return math.sqrt(math.pow((curr.x - self.goal.x),2) + math.pow((curr.y - self.goal.y),2))

class AsME(Abstract_Heuristic):
    def get_h(self, curr):
        import math
        return 0.5*math.sqrt(math.pow((curr.x - self.goal.x),2) + math.pow((curr.y - self.goal.y),2)) + 0.5*(abs(curr.x - self.goal.x) + abs(curr.y - self.goal.y))

class AsDia(Abstract_Heuristic):

    def get_h(self,curr):
        '''
        dx = abs(curr.x - self.goal.x)
        dy = abs(curr.y - self.goal.y)
        normal_cost = get_curr_cost(self.graph,curr)
        import math
        diagonal_cost = normal_cost*math.sqrt(2)
        return  normal_cost * max(dx,dy) + (diagonal_cost - 2*normal_cost) * min(dx,dy)
        '''
        dx1 = curr.x - self.goal.x
        dy1 = curr.y - self.goal.y
        dx2 = self.start.x - self.goal.x
        dy2 = self.start.y - self.goal.y
        return abs(dx1 * dy2 - dx2 * dy1)

class AsSeq(Abstract_Heuristic):
    w1 = 1
    w2 = 1
    A1 = None
    A2 = None
    A3 = None
    A4 = None
    A5 = None
    algorSet = None

    def init_algorSet(self):
        self.A1 = AsMan(self.graph)
        self.A2 = AsCostMan(self.graph)
        self.A3 = AsEu(self.graph)
        self.A4 = AsME(self.graph)
        self.A5 = AsDia(self.graph)
        self.algorSet = [self.A1, self.A2, self.A3, self.A4, self.A5]

    def key(self, s, i):
        s.h = self.w1 * self.algorSet[i].get_h(s)
        s.f = s.g + self.w1 * self.algorSet[i].get_h(s)
        return s.f

    def not_in_fringe(self, s, fringe):
        for t in fringe:
            if t[1] is s:
                return False
        return True

    def expandState(self, s, i):
        # get cell from (key,cell) pair
        s = s[1]
        #print('s is ',s.x,s.y)
        for neighbor in self.algorSet[i].get_neighbor_cells(s):
            if neighbor not in self.algorSet[i].visited and self.not_in_fringe(neighbor, self.algorSet[i].fringe):
                neighbor.g = 999999
                neighbor.parent = None
            if neighbor.g > s.g + get_cost(self.algorSet[i].graph, s, neighbor):
                neighbor.g = s.g + get_cost(self.algorSet[i].graph, s, neighbor)
                neighbor.parent = s
                if neighbor not in self.algorSet[i].visited:
                    for fringe_item in self.algorSet[i].fringe:
                        if fringe_item[1] is neighbor:
                            self.algorSet[i].fringe.remove(fringe_item)
                            self.memreq -= 1
                            heapq.heapify(self.algorSet[i].fringe)
                    heapq.heappush(self.algorSet[i].fringe, (self.key(neighbor,i), neighbor))
                    self.incMemReq()

    def search(self, start, goal, w1, w2):
        self.w1 = w1
        self.w2 = w2
        self.init_start_goal(start,goal)
        self.init_algorSet()
        for i in range(5):
            self.algorSet[i].init_start_goal(start,goal)
            self.algorSet[i].start.g = 0
            self.algorSet[i].goal.g = 999999
            self.algorSet[i].start.parent = None
            self.algorSet[i].goal.parent = None
            heapq.heappush(self.algorSet[i].fringe, (self.key(self.algorSet[i].start, i), self.algorSet[i].start))
            self.incMemReq()

        while self.algorSet[0].fringe[0][0] < 999999:
            for i in range(1,5):
                #print(len(self.algorSet[i].fringe[0]))
                if not self.algorSet[i].fringe:
                    print('fringe ',i,'is empty for some reason')
                    continue
                if not self.algorSet[0].fringe:
                    print('fringe ', 0, 'is empty for some reason')
                    continue

                if self.algorSet[i].fringe[0][0] <= self.w2 * self.algorSet[0].fringe[0][0]:
                    if self.algorSet[i].goal.g <= self.algorSet[i].fringe[0][0]:
                        if self.algorSet[i].goal.g < 999999:
                            self.cells = self.algorSet[i].cells
                            return self.algorSet[i].update_graph()
                    else:
                        s = heapq.heappop(self.algorSet[i].fringe)
                        self.memreq -= 1
                        self.node_expanded += 1
                        self.expandState(s,i)
                        self.algorSet[i].visited.add(s[1])
                else:
                    if self.algorSet[0].goal.g <= self.algorSet[0].fringe[0][0]:
                        if self.algorSet[0].goal.g < 999999:
                            self.cells = self.algorSet[0].cells
                            return self.algorSet[0].update_graph()
                    else:
                        s = heapq.heappop(self.algorSet[0].fringe)
                        self.memreq -= 1
                        self.node_expanded += 1
                        self.expandState(s, 0)
                        self.algorSet[0].visited.add(s[1])
            if not self.algorSet[0].fringe:
                print('fringe ', 0, 'is empty no path found')
                return self.algorSet[0].update_graph()
                break

class AsQue(AsSeq):

    visited_inad = set()

    def remove_from_all_fringe(self, tuple):
        for i in range(5):
            for item in self.algorSet[i].fringe:
                if item is tuple:
                    self.algorSet[i].fringe.remove(item)
                    heapq.heapify(self.algorSet[i].fringe)
                    break

    def never_generated(self, cell):
        if cell in self.visited or cell in self.visited_inad:
            return False
        for i in range(5):
            if self.not_in_fringe(cell, self.algorSet[i].fringe):
                continue
            else:
                # cell found in fringe i
                return False
        # not in both visited nor in all fringes
        return True

    def expandState(self, s):
        self.remove_from_all_fringe(s)
        # get cell from (key,cell) pair
        s = s[1]
        # print('s is ',s.x,s.y)

        for neighbor in self.get_neighbor_cells(s):
            if self.never_generated(neighbor):
                neighbor.g = 999999
                neighbor.parent = None
            if neighbor.g > s.g + get_cost(self.graph, s, neighbor):
                neighbor.g = s.g + get_cost(self.graph, s, neighbor)
                neighbor.parent = s
                if neighbor not in self.visited:
                    # insert/update in Open_0
                    for fringe_item in self.algorSet[0].fringe:
                        if fringe_item[1] is neighbor:
                            self.algorSet[0].fringe.remove(fringe_item)
                            self.memreq -= 1
                            heapq.heapify(self.algorSet[0].fringe)
                    heapq.heappush(self.algorSet[0].fringe, (self.key(neighbor, 0), neighbor))
                    self.incMemReq()

                    if neighbor not in self.visited_inad:
                        for i in range(1,5):
                            if self.key(neighbor, i) <= self.w2 * self.key(neighbor,0):
                                # insert/update in Open_i
                                for fringe_item in self.algorSet[i].fringe:
                                    if fringe_item[1] is neighbor:
                                        self.algorSet[i].fringe.remove(fringe_item)
                                        self.memreq -= 1
                                        heapq.heapify(self.algorSet[i].fringe)
                                heapq.heappush(self.algorSet[i].fringe, (self.key(neighbor, i), neighbor))
                                self.incMemReq()
        return

    def search(self, start, goal, w1, w2):
        self.w1 = w1
        self.w2 = w2
        self.init_algorSet()

        self.init_start_goal(start,goal)
        self.start.g = 0
        self.goal.g = 999999

        for i in range(5):
            self.algorSet[i].start = self.start
            self.algorSet[i].goal  = self.goal
            heapq.heappush(self.algorSet[i].fringe, (self.key(self.start, i), self.start))
            self.incMemReq()

        while self.algorSet[0].fringe[0][0] < 999999:
            for i in range(1,5):

                if not self.algorSet[i].fringe:
                    #print('fringe ',i,'is empty for some reason')
                    minkey_i = 999999
                else:
                    minkey_i = self.algorSet[i].fringe[0][0]
                if not self.algorSet[0].fringe:
                    print('fringe ', 0, 'is empty for some reason')
                    minkey_0 = 999999
                else:
                    minkey_0 = self.algorSet[0].fringe[0][0]

                if minkey_0 == minkey_i == 999999:
                    continue
                #print(self.algorSet[i].fringe[0])
                #print(self.algorSet[i].fringe[0][0])
                #print(self.algorSet[0].fringe[0])
                #print(self.algorSet[0].fringe[0][0])

                if minkey_i <= self.w2 * minkey_0:
                    if self.goal.g <= minkey_i:
                        if self.goal.g < 999999:
                            return self.update_graph()
                    else:
                        s = heapq.heappop(self.algorSet[i].fringe)
                        self.memreq -= 1
                        self.node_expanded += 1
                        self.expandState(s)
                        self.visited_inad.add(s[1])
                else:
                    if self.goal.g <= minkey_0:
                        if self.goal.g < 999999:
                            return self.update_graph()
                    else:
                        s = heapq.heappop(self.algorSet[0].fringe)
                        self.memreq -= 1
                        self.node_expanded += 1
                        self.expandState(s)
                        self.visited.add(s[1])
            if not self.algorSet[0].fringe:
                print('fringe ', 0, 'is empty no path found')
                return self.update_graph()

