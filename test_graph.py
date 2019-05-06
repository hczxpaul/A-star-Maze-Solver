import numpy
import pygame
from heuristic import *
import time


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
GREY =  (238, 203, 173)
DARK_GREY = (49, 79, 79)
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 8
HEIGHT = 8



def init_frame(frame):
    frame = [[1 for i in range(10)] for j in range(10)]
    return frame

def shape_frame(frame):

    #frame = make_block(frame)

    return frame

def make_block(frame):
    #random 100 number
    random_block = numpy.random.choice(100,size=20,replace = False)
    for i in range(20):
        #get the x_pos and y_pos
        y_pos = random_block[i]//10
        x_pos = random_block[i]-y_pos*10
        if(frame[int(y_pos)][int(x_pos)]==1):
            frame[int(y_pos)][int(x_pos)]=0
        else:
            #regenerate number
            while(frame[int(y_pos)][int(x_pos)]!=1):
                random_block[i] = numpy.random.randint(100)
                y_pos = random_block[i] // 10
                x_pos = random_block[i] -y_pos*10
            frame[int(y_pos)][int(x_pos)] = 0

    return frame

def make_graphic(frame):
    file_frame = frame

    pygame.init()
    WINDOW_SIZE = [1560, 960]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("Map")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Set the screen background
    screen.fill(WHITE)

    # Draw the grid
    for row in range(10):
        for column in range(10):
            color = BLACK
            pygame.draw.rect(screen,color,(WIDTH * column ,HEIGHT * row ,WIDTH,HEIGHT),1)

    # Limit to 60 frames per second
    clock.tick(60)

    # fill color based on 2d array
    for x in range(10):
        for y in range (10):
            if(frame[x][y]==2):
                color = GREY
            elif(frame[x][y]==0):
                color = DARK_GREY
            elif(frame[x][y]=='a'):
                color = BLUE
            elif(frame[x][y]=='b'):
                color = BLUE
            elif(frame[x][y]==1):
                color = WHITE
            elif(frame[x][y]=='p' or frame[x][y]=='q' or frame[x][y]=='r' or frame[x][y]=='s'):
                color = RED
            else:
                continue
            make_grid_color(screen,color,y*8,x*8)

    # Go ahead and update the screen with what we've drawn.
    #pygame.display.flip()

    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    myfont = pygame.font.SysFont("Comic Sans MS", 30)
    textsurface = myfont.render('Start', False, (0, 0, 0))
    screen.blit(textsurface, (1380, 800))

    astar = AsMan(frame)
    check = 0

    pygame.display.flip()
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if(pos[0]>=1385 and pos[0]<=1455 and pos[1]>=810 and pos[1]<=835):
                    #store start&end position in file
                    start_goal_pos = init_start_goal_pos(frame)
                    for i in range(10):
                        file_start_point.append([start_goal_pos[i*4+0], start_goal_pos[i*4+1]])
                    for i in range(10):
                        file_end_point.append([start_goal_pos[i*4+2], start_goal_pos[i*4+3]])

                    for z in range(50):
                        start_time = time.time()

                        for x in range(10):
                            for y in range(10):
                                if (frame[x][y] == 'p'):
                                    frame[x][y] = 1
                                elif(frame[x][y]=='q'):
                                    frame[x][y] = 2
                                elif(frame[x][y]=='r'):
                                    frame[x][y] = 'a'
                                elif(frame[x][y]=='s'):
                                    frame[x][y] = 'b'
                                else:
                                    continue

                        grid = frame
                        if(z<10):
                            astar = UCS(grid)
                            frame = astar.search((start_goal_pos[z*4+1], start_goal_pos[z*4+0]),
                                                 (start_goal_pos[z*4+3], start_goal_pos[z*4+2]),1)
                            cell_length.append(astar.get_cell(start_goal_pos[z*4+3], start_goal_pos[z*4+2]).f)
                        elif(z<20):
                            astar = AsMan(grid)
                            frame = astar.search((start_goal_pos[(z-10)*4+1], start_goal_pos[(z-10)*4+0]),
                                                 (start_goal_pos[(z-10)*4+3], start_goal_pos[(z-10)*4+2]),1)
                            cell_length.append(astar.get_cell(start_goal_pos[(z-10)*4 + 3], start_goal_pos[(z-10)*4 + 2]).f)
                        elif(z<30):
                            astar = AsEu(grid)
                            frame = astar.search((start_goal_pos[(z-20)*4+1], start_goal_pos[(z-20)*4+0]),
                                                 (start_goal_pos[(z-20)*4+3], start_goal_pos[(z-20)*4+2]),1.25)
                            cell_length.append(
                                astar.get_cell(start_goal_pos[(z - 20) * 4 + 3], start_goal_pos[(z - 20) * 4 + 2]).f)
                        elif(z<40):
                            astar = AsDia(grid)
                            frame = astar.search((start_goal_pos[(z-30)*4+1], start_goal_pos[(z-30)*4+0]),
                                                 (start_goal_pos[(z-30)*4+3], start_goal_pos[(z-30)*4+2]), 2)
                            cell_length.append(
                                astar.get_cell(start_goal_pos[(z - 30) * 4 + 3], start_goal_pos[(z - 30) * 4 + 2]).f)
                        elif(z<50):
                            astar = AsME(grid)
                            frame = astar.search((start_goal_pos[(z-40)*4+1], start_goal_pos[(z-40)*4+0]),
                                                 (start_goal_pos[(z-40)*4+3], start_goal_pos[(z-40)*4+2]),1)
                            cell_length.append(
                                astar.get_cell(start_goal_pos[(z - 40) * 4 + 3], start_goal_pos[(z - 40) * 4 + 2]).f)
                        check = 1
                        #result to store in output file
                        duration_time = time.time()-start_time
                        run_time.append(duration_time)
                        node_expand.append(astar.getNodeExpand())
                        memory_require.append(astar.getMemReq())

                        # fill color based on 2d array
                        for x in range(10):
                            for y in range(10):
                                if (frame[x][y] == 2):
                                    color = GREY
                                elif (frame[x][y] == 0):
                                    color = DARK_GREY
                                elif (frame[x][y] == 'a'):
                                    color = BLUE
                                elif (frame[x][y] == 'b'):
                                    color = BLUE
                                elif (frame[x][y] == 1):
                                    color = WHITE
                                elif (frame[x][y] == 'p'):
                                    color = RED
                                elif(frame[x][y]=='q'):
                                    color = RED
                                elif(frame[x][y]=='r'):
                                    color = RED
                                elif(frame[x][y]=='s'):
                                    color = RED
                                else:
                                    continue
                                make_grid_color(screen, color, y * 8, x * 8)
                        pygame.display.flip()
                elif(pos[0]>=0 and pos[0]<=1280 and pos[1]>=0 and pos[1]<=960):
                    if(check == 0):
                        continue
                    else:
                        content = []
                        content.append(int(astar.get_cell(int(pos[0]/8),int(pos[1]/8)).h))
                        content.append(int(astar.get_cell(int(pos[0]/8),int(pos[1]/8)).g))
                        content.append(int(astar.get_cell(int(pos[0]/8), int(pos[1]/8)).f))
                        pos_font = pygame.font.SysFont("Comic Sans MS", 30)
                        pos_text_surface = pos_font.render('h,g,f{}'.format(content), 1, (0, 0, 0))
                        screen.blit(pos_text_surface, (1281, 500))
                        pygame.display.update()
                        pos_text_surface = pos_font.render('h,g,f{}'.format(content), 1, WHITE)
                        screen.blit(pos_text_surface, (1281, 500))

    print('end')

    #clear file_frame
    for x in range(10):
        for y in range(10):
            if (file_frame[x][y] == 'p'):
                frame[x][y] = 1
            elif (file_frame[x][y] == 'q'):
                frame[x][y] = 2
            elif (file_frame[x][y] == 'r'):
                frame[x][y] = 'a'
            elif (file_frame[x][y] == 's'):
                frame[x][y] = 'b'
            else:
                continue
    result_file.write(str(file_start_point))
    result_file.write('\n')
    result_file.write(str(file_end_point))
    result_file.write('\n')
    result_file.write(str(file_hard_to_traverse_point))
    result_file.write('\n')
    result_file.write(str(file_frame))

    for i in range(5):
        file_run_time.append((run_time[10*i+0]+run_time[10*i+1]+run_time[10*i+2]+run_time[10*i+3]+run_time[10*i+4]+run_time[10*i+5]+run_time[10*i+6]+run_time[10*i+7]+run_time[10*i+8]+run_time[10*i+9])/10)
    time_file.write(str(file_run_time))
    time_file.write('\n')
    for i in range(5):
        file_cell_length.append((cell_length[10*i+0]+cell_length[10*i+1]+cell_length[10*i+2]+cell_length[10*i+3]+cell_length[10*i+4]+cell_length[10*i+5]+cell_length[10*i+6]+cell_length[10*i+7]+cell_length[10*i+8]+cell_length[10*i+9])/10)
    time_file.write(str(file_cell_length))
    time_file.write('\n')
    for i in range(5):
        file_node_expand.append((node_expand[10*i+0]+node_expand[10*i+1]+node_expand[10*i+2]+node_expand[10*i+3]+node_expand[10*i+4]+node_expand[10*i+5]+node_expand[10*i+6]+node_expand[10*i+7]+node_expand[10*i+8]+node_expand[10*i+9])/10)
    time_file.write(str(file_node_expand))
    time_file.write('\n')
    for i in range(5):
        file_memory_require.append((memory_require[10*i+0]+memory_require[10*i+1]+memory_require[10*i+2]+memory_require[10*i+3]+memory_require[10*i+4]+memory_require[10*i+5]+memory_require[10*i+6]+memory_require[10*i+7]+memory_require[10*i+8]+memory_require[10*i+9])/10)
    time_file.write(str(file_memory_require))

    return

def make_grid_color(screen, color, width_pos,height_pos):
    pygame.draw.rect(screen, color, (width_pos+1, height_pos+1, WIDTH-1, HEIGHT-1))
    return