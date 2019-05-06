class graph_data(object):
    algor=None
    weight=1
    def __init__(self, start_goal_pairs, graph):
        self.start_goal_pairs = start_goal_pairs
        self.graph = graph

def parse_start_goal(starts,goals):
    result  = []
    start   = starts.split(' ', 1)
    goal    = goals.split(' ', 1)

    for i in range(len(start)):
        if start[i] == '\n':
            continue
        else:
            result.append((start[i],goal[i]))
    # result is list of (start, goal) pairs
    return result


def read_file(file):
    lines = file.readlines()
    lineCount = 0
    start_coordinates   = lines[lineCount]
    lineCount += lineCount
    goal_coordinates    = lines[lineCount]

    # skip center of hard to traverse
    lines = lines[lineCount:lineCount + 8]
    # read the graph, consisting of 0,1,2,a,b in to 2D array
    row = []
    graph = []
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            # skip '\n' and ' '
            if (lines[i][j] == '\n' or lines[i][j] == ' '):
                continue
            # convert string to integer
            if lines[i][j] == '1':
                lines[i][j] = 1
            elif lines[i][j] == '2':
                lines[i][j] = 2
            elif lines[i][j] == '0':
                lines[i][j] = 0
            row.append(lines[i][j])
        graph.append(row)
        row = []

    #convert start and goal into pairs
    start_goal_pairs = parse_start_goal(start_coordinates,goal_coordinates)

    file.close()

    return graph_data(start_goal_pairs, graph)