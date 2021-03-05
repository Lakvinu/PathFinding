from tkinter import *
import time
from collections import deque

window = Tk()
window.title("Pathfinding By Lakvinu")
window.resizable(0, 0)

width, length = 30, 30
left_side = Frame(window)
left_side.pack(side=LEFT)
right_side = Frame(window)
right_side.pack(side=RIGHT)
grid = [[[None] for i in range(width)] for j in range(length)]

# variables to change the direction of the game
obs_status = True
find_start = False
find_end = False


# creating the functions and design of the grid and etc

def on_drag(event):
    """ function that allows the controller to drag squares to position the
    obstacles instead of individually cliking on it"""
    global obs_status

    if obs_status:
        x, y = window.winfo_pointerxy()
        btn = window.winfo_containing(x, y)

        if btn and hasattr(btn, 'selectable'):
            btn.config(bg="black")


# button function to change variables
def chs():
    """function that allows the controller to create obstacles"""
    global obs_status
    obs_status = True
    window.bind('<B1-Motion>', on_drag)


def change_pos(row, col):
    """function that updates what the controller wants to place next"""
    global find_end
    global find_start

    if find_start:
        grid[row][col]['bg'] = "orange"
        find_start = False

    if find_end:
        grid[row][col]['bg'] = "blue"
        find_end = False


def start_pos():
    """function that allows player to choose the starting position"""
    global find_start
    global obs_status
    obs_status = False
    find_start = True


def end_pos():
    """function that allows player to choose ending position"""
    global obs_status
    global find_end

    obs_status = False
    find_end = True


# algorithm section
new_grid = [['.' for i in range(width)] for j in range(length)]


def find_quickest():
    """fucntion that updates the grid used for algorithms and visualises the quickest path"""
    for i in range(width):
        for j in range(length):

            cur = grid[i][j]['bg']

            if cur == "black":

                new_grid[i][j] = "#"

            elif cur == "orange":

                start_place = i, j
                new_grid[i][j] = '*'

            elif cur == "blue":

                end_place = i, j
                new_grid[i][j] = '!'

    ans = deque(bfs(start_place, end_place))

    while ans:
        cur = ans.pop()
        row, col = cur
        grid[row][col]['bg'] = 'green'
        window.update()
        time.sleep(0.000001)


def sort_arr(arr, start, p):
    """ function that sorts the array depending on f value(g + h)"""
    # [([(10, 18), (11, 18)], 0), ([(10, 18), (9, 18)], 0), ([(10, 18), (10, 19)], 0), ([(10, 18), (10, 17)], 0)]

    # Storing the distance with its
    # distance in the vector array

    for i in range(len(arr)):
        cur_distance = arr[i][-1]

        end_dist = abs(p[0] - arr[i][0][-1][0]) + abs(p[1] - arr[i][0][-1][1])

        start_dist = abs(arr[i][0][-1][0] - arr[i][0][-2][0]) + abs(arr[i][0][-1][1] - arr[i][0][-2][1])

        #start_dist = pow((arr[i][0][-1][0] - arr[i][0][-2][0]), 2) + pow((arr[i][0][-1][1] - arr[i][0][-2][1]), 2)

        # vp.append([end_dist + start_dist, arr[i]])
        arr[i][1] = start_dist + end_dist + cur_distance
        print(arr[i][1], start, end_dist)

        # Sorting the array with

    # respect to its distance

    return sorted(arr, key=lambda x: x[1])


def update_changes(row, col):
    """function that updates the interactive board to demonstrate the box it is looking at currently"""
    grid[row][col]['bg'] = "red"

    new_grid[row][col] = '1'

    window.update()

    time.sleep(0.0001)


def update_distance(dis, end_place, row, col):
    """ fucntion that changes the distane in order to makes suae there is no extra distance shown"""
    if dis != 0:
        dis -= abs(end_place[0] - row) + abs(end_place[1] - col)

    return dis


def bfs(start_place, end_place):
    """ Fucntion that shows an A* algortihm and returns an array showing the quickest path"""
    moves = [(1, 0), (-1, 0), (0, 1), (0, - 1)]

    myde = deque([[[start_place], 0]])

    y_possible = set(list(range(length)))

    x_possible = set(list(range(width)))

    while myde:

        cur = myde.popleft()

        row, col = cur[0][-1]

        distance = update_distance(cur[-1], end_place, row, col)

        update_changes(row, col)

        new_moves = []

        for i in range(4):

            y, x = moves[i]

            new_y, new_x = row + y, col + x
            # found
            if (new_y, new_x) == end_place:
                return cur[0] + [(new_y, new_x)]

            # checking if move is within range
            if new_y not in y_possible or new_x not in x_possible:
                continue

            # checking if the mvoes hasnt been visited before
            if new_grid[new_y][new_x] == '1':
                continue

            # checking if the move isnt an obstacle
            if new_grid[new_y][new_x] == '#':
                continue

            # updating move to show that it has been visited
            new_grid[new_y][new_x] = '1'

            new_moves.append([cur[0] + [(new_y, new_x)], distance])

        # appending the new moves with the new distance
        myde += deque(sort_arr(new_moves, start_place, end_place))

        # sorting the deque by then distance in order to find the best next move
        myde = deque(sorted(myde, key=lambda x: x[1]))


def create_grid():
    """ function that creates the layout and structure for the interactive grid and buttons"""
    for i in range(width):
        for j in range(length):
            grid[i][j] = Button(left_side, height=1, width=2, command=lambda row=i, col=j: change_pos(row, col))

            grid[i][j].selectable = True

            grid[i][j].grid(row=i, column=j)

    start = Button(right_side, height=3, width=15, text="Choose Starting \n Position", font=("Arial", 15),
                   command=start_pos)
    start.grid(padx=30)

    end = Button(right_side, height=3, width=15, text="Choose End \n Position", font=("Arial", 15), command=end_pos)

    end.grid(padx=30, pady=15)

    obstacles = Button(right_side, height=3, width=15, text="Choose Your \n Obstacles", font=("Arial", 15), command=chs)

    obstacles.grid(padx=30)

    find = Button(right_side, height=2, width=10, text="Find", font=("Arial", 20), command=find_quickest)

    find.grid(padx=30, pady=15)


create_grid()

window.mainloop()
