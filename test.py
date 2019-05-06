from heuristic import *
from graphic import *

def produce_frame():
    frame = {}
    frame = init_frame(frame)
    frame = shape_frame(frame)
    return frame

def main():
#for a in range(20):
    # Generate map
    while True:
        frame = produce_frame()
        if frame[0][0] == 0 or frame[119][159] == 0:
            continue
        else:
            break

    for i in range(120):
        for j in range(160):
            print(frame[i][j],end='')
        print()

    import random
    astar = AsQue(frame)
    a2 = AsMan(frame)
    sx = random.randrange(0,159)
    sy = random.randrange(0,119)
    gx = random.randrange(0,159)
    gy = random.randrange(0,119)
    #print(frame[sy][sx],frame[gy][gx])
    grid = astar.search((sx,sy),(gx,gy),1.5,1.5)
    grid = a2.search((sx,sy),(gx,gy),1.5)
    make_graphic(grid,a2)
    #a+=1
    print('\n')

main()
print('end')
