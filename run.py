__author__ = "Chaozhang Huang, Weize Shen"

from graphic import *
#from file_process import *
from heuristic import *

def is_num(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def main():
    print('1 : load map from file')
    print('2 : generate random map')
    user_input = input('enter your option: ')
    while user_input != '1' and user_input != '2':
        user_input = input('invalid input, enter your option again: ')

    if user_input == '1':
        # read file
        filename = input('enter file name: ')
        import os.path
        while not os.path.isfile(filename):
            filename = input('invalid file name, enter file name again: ')
        file = open(filename, "r")
        graph_data = read_file(file)


    if user_input == '2':
        # ask for start and goal
        user_input = input('enter start coordinate ( e.g 10 110 ): ')
        start = user_input.split(' ',1)
        startx = int(start[0])
        starty = int(start[1])
        while len(start)!=2 or startx<0 or startx>159 or starty<0 or starty>119:
            user_input = input('invalid input, enter start coordinate again ( e.g 10 110 ): ')
            start = user_input.split(' ', 1)
            startx = int(start[0])
            starty = int(start[1])

        user_input = input('enter goal coordinate ( e.g 10 110 ): ')
        goal = user_input.split(' ', 1)
        goalx = int(goal[0])
        goaly = int(goal[1])
        while len(goal) != 2 or goalx < 0 or goalx > 159 or goaly < 0 or goaly > 119:
            user_input = input('invalid input, enter goal coordinate again ( e.g 10 110 ): ')
            goal = user_input.split(' ', 1)
            goalx = int(goal[0])
            goaly = int(goal[1])

        # Generate map
        while True:
            frame = {}
            frame = init_frame(frame)
            frame = shape_frame(frame)
            if frame[starty][startx] == 0 or frame[goaly][goalx] == 0:
                continue
            else:
                break
        grid = frame
        # ask for which algor. to use
        print('1 : Uniform Cost Search')
        print('2 : A*Manhattan')
        print('3 : A*Cost Manhattan')
        print('4 : A*Euclidean')
        print('5 : A*Diagonal Distance')
        print('6 : A*ME')
        print('7 : A*Sequential')
        print('8 : A*Queue')

        user_input = input('enter your option: ')
        while int(user_input)<0 or int(user_input)>8:
            user_input = input('invalid input, enter your option again: ')
         # UCS
        if user_input == '1':
            astar = UCS(grid)
            frame = astar.search((startx, starty), (goalx, goaly),1)
        # AsMan
        elif user_input == '2':
            # ask for weight
            user_input = input('enter weight: ')
            while not is_num(user_input):
                user_input = input('invalid input, enter your option again: ')
            astar = AsMan(grid)
            frame = astar.search((startx, starty), (goalx, goaly), int(user_input))
        # AsCostMan
        elif user_input == '3':
            # ask for weight
            user_input = input('enter weight: ')
            while not is_num(user_input):
                   user_input = input('invalid input, enter your option again: ')
            astar = AsCostMan(grid)
            frame = astar.search((startx, starty), (goalx, goaly), int(user_input))
        # AsEuc
        elif user_input == '4':
            # ask for weight
            user_input = input('enter weight: ')
            while not is_num(user_input):
                user_input = input('invalid input, enter your option again: ')
            astar = AsEu(grid)
            frame = astar.search((startx, starty), (goalx, goaly), int(user_input))
        # AsDia
        elif user_input == '5':
            # ask for weight
            user_input = input('enter weight: ')
            while not is_num(user_input):
                user_input = input('invalid input, enter your option again: ')
            astar = AsDia(grid)
            frame = astar.search((startx, starty), (goalx, goaly), int(user_input))
        # AsME
        elif user_input == '6':
            # ask for weight
            user_input = input('enter weight: ')
            while not is_num(user_input):
                user_input = input('invalid input, enter your option again: ')
            astar = AsME(grid)
            frame = astar.search((startx, starty), (goalx, goaly), int(user_input))
        elif user_input == '7':
            # ask for weight
            user_input_1 = input('enter weight 1: ')
            while not is_num(user_input_1):
                user_input_1 = input('invalid input, enter your option again: ')
            user_input_2 = input('enter weight 2: ')
            while not is_num(user_input_2):
                user_input_2 = input('invalid input, enter your option again: ')
            astar = AsSeq(grid)
            frame = astar.search((startx, starty), (goalx, goaly), int(user_input_1),int(user_input_2))
        elif user_input == '8':
            # ask for weight
            user_input_1 = input('enter weight 1: ')
            while not is_num(user_input_1):
                user_input_1 = input('invalid input, enter your option again: ')
            user_input_2 = input('enter weight 2: ')
            while not is_num(user_input_2):
                user_input_2 = input('invalid input, enter your option again: ')
            astar = AsQue(grid)
            frame = astar.search((startx, starty), (goalx, goaly), int(user_input_1), int(user_input_2))
        make_graphic(frame,astar)

def read_file(f):
    strs = f.readline()
    starts = strs.replace('[', '')
    starts = starts.replace(',', '')
    starts = starts.replace(']', '')
    starts = starts.split()

    strs = f.readline()
    goals = strs.replace('[', '')
    goals = goals.replace(',', '')
    goals = goals.replace(']', '')
    goals = goals.split()

    strs = f.readline()
    strs = f.readline()
    frame = strs.replace('[', '')
    frame = frame.replace(',', '')
    frame = frame.replace(']', '')
    frame = frame.replace('\'', '')
    frame = frame.split()
    array = [[1 for i in range(160)] for j in range(120)]
    for i in range(120):
        for j in range(160):
            if is_num(frame[i * 160 + j]):
                array[i][j] = int(frame[i * 160 + j])
            else:
                array[i][j] = frame[i * 160 + j]

    astar = AsMan(array)
    array = astar.search((int(starts[1]), int(starts[0])), (int(goals[1]), int(goals[0])),1)
    make_graphic(array,astar)
    f.close()


if __name__ == "__main__":
   main()
