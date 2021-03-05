from tkinter import *
import time
from collections import deque
window = Tk()
window.title("Pathfinding By Lakvinu")
window.resizable(0,0)


left_side = Frame(window)
left_side.pack(side=LEFT)
right_side = Frame(window)
right_side.pack(side = RIGHT)
grid = [[[None] for i in range(50)] for j in range(50)]

# variables to change the direction of the game
obs_status = True
find_start = False
find_end = False


# creating the functions and design of the grid and etc

def chs():
    global obs_status
    obs_status = True

    def on_drag(event):
        global obs_status

        if obs_status:
            x, y = window.winfo_pointerxy()
            btn = window.winfo_containing(x, y)

            if btn and hasattr(btn, 'selectable'):
                btn.config(bg="black")

    window.bind('<B1-Motion>', on_drag)


def change_pos(row, col):
    global find_end
    global find_start

    if find_start:
        grid[row][col]['bg'] = "orange"
        find_start = False

    if find_end:
        grid[row][col]['bg'] = "blue"
        find_end = False


def start_pos():
    global find_start
    global obs_status
    obs_status = False
    find_start = True


def end_pos():
    global obs_status
    global find_end

    obs_status = False
    find_end = True





# algorithm section
new_grid = [['.' for i in range(30)] for j in range(30)]

def find_quickest():
    for i in range(30):
        for j in range(30):
            if grid[i][j]['bg'] == "black":
                new_grid[i][j] = "#"
            elif grid[i][j]['bg'] == "orange":
                start_place = i, j
                new_grid[i][j] = '*'
            elif grid[i][j]['bg'] == "blue":
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

    vp = []

    # Storing the distance with its
    # distance in the vector array
    print(arr)
    for i in range(len(arr)):

        dist = pow((p[0] - arr[i][0][-1][0]), 2) + pow((p[1] - arr[i][0][-1][1]), 2)
        dist += pow((start[0] - arr[i][0][-1][0]), 2) + pow((start[1] - arr[i][0][-1][1]), 2)

        vp.append([dist, arr[i]])

        # Sorting the array with
    # respect to its distance
    vp = sorted(vp, key=lambda x: (x[0], x[1][1]))
    print(vp)
    vp = [lis[1] for lis in vp]



    return vp



def bfs(start_place, end_place):

    global new_grid

    moves = [(1, 0), (-1, 0), (0, 1), (0, - 1)]

    myde = deque([([start_place],0)])

    y_possible = set(list(range(30)))

    x_possible = set(list(range(30)))

    while myde:

        cur = myde.popleft()

        row, col = cur[0][-1]

        move_no = cur[-1]

        grid[row][col]['bg'] = "red"

        new_grid[row][col] = '1'

        window.update()
        time.sleep(0.0001)

        for i in range(4):
            y, x = moves[i]
            new_y, new_x = row + y, col + x

            if (new_y, new_x) == end_place:
                return cur[0] + [(new_y, new_x)]

            if new_y in y_possible and new_x in x_possible:
                if new_grid[new_y][new_x] == '.':
                    new_grid[new_y][new_x] = '1'
                    myde.append((cur[0] + [(new_y, new_x)], move_no + 1))

        myde = deque(sort_arr(myde, start_place, end_place))






























def create_grid():
    for i in range(30):
        for j in range(30):
            grid[i][j] = Button(left_side, height=1, width=2, command=lambda row=i, col=j: change_pos(row, col))
            grid[i][j].selectable = True
            grid[i][j].grid(row=i, column=j)

    start = Button(right_side, height=3, width=15, text="Choose Starting \n Position", font=("Arial", 15),
                   command=start_pos)
    start.grid(padx=30)

    end = Button(right_side, height=3, width=15, text="Choose End \n Position", font=("Arial", 15), command=end_pos)
    end.grid(padx=30, pady=15)

    obstacles = Button(right_side, height=3, width=20, text="Choose Your Obstacles", font=("Arial", 10), command=chs)
    obstacles.grid(padx=30)

    find = Button(right_side, height=2, width=10, text="Find", font=("Arial", 20), command=find_quickest)
    find.grid(padx=30, pady=15)




create_grid()





























window.mainloop()