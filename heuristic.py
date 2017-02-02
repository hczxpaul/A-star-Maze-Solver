from queue import PriorityQueue


class Heuristic(object):
    def h(node,goal,size,grid):
        raise NotImplementedError("Please Implement this method")

    def add_path(self):
        raise NotImplementedError("Please Implement this method")


class UCS(Heuristic):

    def h(start,goal,size,grid):
        # initialize
        queue = PriorityQueue()
        visited = set()
        queue.put((0, start))

        while queue:
            cost, node = queue.get()
            if node not in visited:
                visited.add(node)

                if node == goal:
                    # add to path
                    print("goal!")
                    return
                # if the node is not GOAL, add to fringe
                for                                                                                     i in node.neighbors(node):
                    if i not in visited:
                        total_cost = cost + cost
                        queue.put((total_cost, i))

class As(Heuristic):
    def h(node,goal,size,grid):
        print("?")


class WAs(Heuristic):
    def h(node,goal,size,grid):
        print("?")