# подключение основных библиотек

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import itertools
import time
from threading import Timer
import threading
import ast

# создание класса Point для описания молекулы газа
class Point():
    def __init__(self, x=0, y=0, vx=10, vy=0, colour= 0 ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.colour = colour

# обработка взаимодействия 4-х точек
def collision_of_4_points(point0, point1, point2, point3):
    if point0[0] == point1[0] == point2[0] == point3[0] and point0[1] == point1[1] == point2[1] == point3[1]:
        return True
    return

# обработка взаимодействия 3-х точек ( лобовое по горизонтали, третья по побочной диагонали)
def collision_of_3_points_horiz_up_right(point0, point1, point2):
    if point2[3] == point1[3] == 0 and point2[2] == -point1[2] and point0[2] < 0 and point0[3] < 0:
        point2[3] = -point2[2]
        point1[3] = -point1[2]
        return (point0, point1, point2)
    return

# обработка взаимодействия 3-х точек ( лобовое по горизонтали, третья по главной диагонали)
def collision_of_3_points_horiz_down_right(point0, point1, point2):
    if point0[3] == point2[3] == 0 and point0[2] == -point2[2] and point1[2] < 0 and point1[3] > 0:
        point0[3] = point0[2]
        point2[3] = point2[2]
        return (point0, point1, point2)
    return

# обработка взаимодействия 3-х точек ( лобовое по горизонтали, третья по главной диагонали)
def collision_of_3_points_horiz_up_left(point0, point1, point2):
    if point0[3] == point2[3] == 0 and point0[2] == -point2[2] and point1[2] > 0 and point1[3] < 0:
        point0[3] = point0[2]
        point2[3] = point2[2]
        return (point0, point1, point2)
    return

# обработка взаимодействия 3-х точек ( лобовое по горизонтали, третья по побочной)
def collision_of_3_points_horiz_down_left(point0, point1, point2):
    if point0[3] == point1[3] == 0 and point0[2] == -point1[2] and point2[2] > 0 and point2[3] > 0:
        point0[3] = -point0[2]
        point1[3] = -point1[2]
        return (point0, point1, point2)
    return

# обработка взаимодействия 3-х точек
def collision_of_3_points_horiz(point0, point1, point2):
    if collision_of_3_points_horiz_up_right(point0, point1, point2) or \
            collision_of_3_points_horiz_down_right(point0, point1, point2) or \
            collision_of_3_points_horiz_up_left(point0, point1, point2) or \
            collision_of_3_points_horiz_down_left(point0, point1, point2):
        return (point0, point1, point2)
    return

# обработка горизонтального взаимодействия 3-х точек ( лобовое по главной диагонали, 3-тья по побочной  )
def collision_of_3_points_diag_main_horiz(point0, point1, point2):
    if point2[3] == 0 and point2[2] > 0 and point1[2] > 0 and point1[2] == -point0[2] and point1[3] < 0 and point1[
        3] == -point0[3]:  # left
        point1[2] = -point1[2]
        point0[2] = -point0[2]
        return (point0, point1, point2)
    if point0[3] == 0 and point0[2] < 0 and point2[2] > 0 and point2[2] == -point1[2] and point2[3] < 0 and point2[
        3] == -point1[3]:  # right
        point1[2] = -point1[2]
        point2[2] = -point2[2]
        return (point0, point1, point2)
    return

# обработка горизонтального взаимодействия 3-х точек ( лобовое по побочной диагонали, 3-тья по главной )
def collision_of_3_points_diag_unmain_horiz(point0, point1, point2):
    if point1[3] == 0 and point1[2] != 0 and point2[2] > 0 and point2[3] > 0 and point2[2] == -point0[2] and point2[
        3] == -point0[3]:  # right
        point2[2] = -point2[2]
        point0[2] = -point0[2]
        return (point0, point1, point2)

    return


# обработка горизонтального взаимодействия 3-х точек ( лобовое по главной дагонали, 3-тья по побочной)
def collision_of_3_points_diag_main_diag(point0, point1, point2): 
    if point1[2] == point0[3] > 0 and point1[3] == point0[2] < 0 and point2[3] > 0:
        point1[3] = 0
        point0[3] = 0
        return (point0, point1, point2)
    if point2[2] == point1[3] > 0 and point2[3] == point1[2] < 0 and point0[3] < 0:
        point2[3] = 0
        point1[3] = 0
        return (point0, point1, point2)
    return

# обработка горизонтального взаимодействия 3-х точек ( лобовое по побочной диагонали, 3-тья по главной)
def collision_of_3_points_diag_unmain_diag(point0, point1, point2):
    if point2[2] == point2[3] > 0 and point0[2] == point0[3] < 0 and point1[3] != 0:
        point2[3] = 0
        point0[3] = 0
        return (point0, point1, point2)
    return

# общая обработка соударений 3-х точек при диагональном лобом ударе
def collision_of_3_points_diag(point0, point1, point2):
    if collision_of_3_points_diag_main_horiz(point0, point1, point2) or \
            collision_of_3_points_diag_unmain_horiz(point0, point1, point2) or \
            collision_of_3_points_diag_main_diag(point0, point1, point2) or \
            collision_of_3_points_diag_unmain_diag(point0, point1, point2):
        return (point0, point1, point2)
    return

# общая обраборка взаимодействия 3-х точек
def collision_of_3_points(point0, point1, point2):
    if point0[0] == point1[0] == point2[0] and point0[1] == point1[1] == point2[1]:
        if collision_of_3_points_horiz(point0, point1, point2) or collision_of_3_points_diag(point0, point1, point2):
            return (point0, point1, point2)
    return

# обработка соударения 2-х точек, лобовое по горизонтали
def collision_of_2_points_horiz(point0, point1):
    if point0[2] < 0 and point0[3] == 0 and point1[3] == 0 and point0[2] == -point1[2]:
        gamma = random.uniform(0, 1)
        if 0 <= gamma <= 0.5:
            point0[3] = point0[2]
            point1[3] = point1[2]
            alfa = random.uniform(0, 1)
            if alfa >= 0.5:
                point0[4], point1[4] = point1[4], point0[4]
        if 0.5 < gamma <= 1:
            point0[3] = -point0[2]
            point1[3] = -point1[2]
            alfa = random.uniform(0, 1)
            if alfa >= 0.5:
                point0[4], point1[4] = point1[4], point0[4]
       # if 0.2 < gamma <= 1:
        #    return (point0, point1)
        return (point0, point1)
    return

# обработка соударения 2-х точек, лобовое по главной диагонали
def collision_of_2_points_diag_main(point0, point1):
    if point1[2] == point0[3] > 0 and point1[3] == point0[2] < 0:
        gamma = random.uniform(0, 1)
        if 0 <= gamma <= 0.5:
            point1[3] = point1[2]
            point0[3] = point0[2]
            alfa = random.uniform(0, 1)
            if alfa >= 0.5:
                point0[4], point1[4] = point1[4], point0[4]
        if 0.5 <= gamma <= 1:
            point1[3] = 0
            point0[3] = 0
            alfa = random.uniform(0, 1)
            if alfa >= 0.5:
                point0[4], point1[4] = point1[4], point0[4]
        #if 0.2 <= gamma <= 1:
          #  return(point0, point1)
        return (point0, point1)
    return

# обработка соударения 2-х точек, лобовое по побочной диагонали
def collision_of_2_points_diag_unmain(point0, point1):
    if point1[2] == point1[3] > 0 and point0[2] == point0[3] < 0:
        gamma = random.uniform(0, 1)
        if 0 <= gamma <= 0.5:
            point1[3] = point0[2]
            point0[3] = point1[2]
            alfa = random.uniform(0, 1)
            if alfa >= 0.5:
                point0[4], point1[4] = point1[4], point0[4]
        if 0.5 < gamma <= 1:
            point1[3] = 0
            point0[3] = 0
            alfa = random.uniform(0, 1)
            if alfa >= 0.5:
                point0[4], point1[4] = point1[4], point0[4]
       # if 0.2 < gamma <= 1:
          #  return (point0, point1)
        return (point0, point1)
    return

# обработка нелобового удара для двух точек разного цвета
def collision_of_2_points_noncental(point0,point1):
    if point0[0] == point1[0] and point0[1]==point1[1]:
        point0[4],point1[4] = point1[4],point0[4]
        # print(1234)
    return(point0,point1)

# общая обработка взаимодействия двух точек
def collision_of_2_points(point0, point1):
    # print('beg', point0, point1)
    if point0[0] == point1[0] and point0[1] == point1[1]:
        if (point0[0], point0[1]) not in s2:
            if collision_of_2_points_diag_main(point0, point1) or collision_of_2_points_diag_unmain(point0, point1) or \
                collision_of_2_points_horiz(point0, point1) or collision_of_2_points_noncental(point0,point1):
                s2.add((point0[0], point0[1]))
                return (point0, point1)
        else:
            # print('else')
            return

    return

# обработка соударения все случаи
def collision(point0, point1, point2, point3):
    if collision_of_4_points(point0, point1, point2, point3):
        return [point0, point1, point2, point3]
    if collision_of_3_points(point0, point1, point2) or collision_of_3_points(point0, point1,point3) or collision_of_3_points(point0,point2, point3) or collision_of_3_points(point1, point2, point3):
        return [point0, point1, point2, point3]

    if collision_of_2_points(point0, point1) or collision_of_2_points(point0, point2) or collision_of_2_points(point0,point3) or collision_of_2_points(
            point1, point2) or \
            collision_of_2_points(point1, point3) or collision_of_2_points(point2,point3):
        return [point0, point1, point2, point3]

    return

# граничные условия для правой стороны
def right_out_of_bounds(point, func_grid, func_speed):
    if (point[0] > func_grid and point[3] == 0 and point[2] > 0):
        return [point[0] - 2 * func_grid - func_speed, point[1], point[2], point[3],point[4]]
    if (point[0] > func_grid and point[3] > 0 and point[2] > 0):
        return [func_speed - point[1], func_speed - point[0], point[2], point[3],point[4]]
    if (point[0] > func_grid and point[3] < 0 and point[2] > 0):
        return [func_speed + point[1], -func_speed + point[0], point[2], point[3],point[4]]
    return

# граничные условия для левой стороны
def left_out_of_bounds(point, func_grid, func_speed):
    if (point[0] < -func_grid and point[3] == 0 and point[2] < 0):
        return [point[0] + 2 * func_grid + func_speed, point[1], point[2], point[3],point[4]]
    if (point[0] < -func_grid and point[3] > 0 and point[2] < 0):
        return [point[1] - func_speed, point[0] + func_speed, point[2], point[3],point[4]]
    if (point[0] < -func_grid and point[3] < 0 and point[2] < 0):
        return [-func_speed - point[1], -func_speed - point[0], point[2], point[3],point[4]]
    return

# граничные условия для верхней стороны
def up_out_of_bounds(point, func_grid, func_speed):
    if (point[1] > func_grid and point[2] > 0) and point[3] > 0:
        return [func_speed - point[1], func_speed - point[0], point[2], point[3],point[4]]
    if (point[1] > func_grid and point[2] < 0) and point[3] > 0:
        return [-func_speed + point[1], func_speed + point[0], point[2], point[3],point[4]]
    return

# граничные условия для нижней стороны
def down_out_of_bounds(point, func_grid, func_speed):
    if (point[1] < -func_grid and point[2] > 0 and point[3] < 0):
        return [func_speed + point[1], - func_speed + point[0], point[2], point[3],point[4]]
    if (point[1] < -func_grid and point[2] < 0 and point[3] < 0):
        return [-func_speed - point[1], - func_speed - point[0], point[2], point[3],point[4]]
    return

# функция сбора распределения числа точек от направления их скоростей
def stats_of_points(board, n, t):
    with open('information.txt', "a") as f:
        with open('data.txt', "a") as y:
            stats1 = [0, 0, 0]
            stats2 = [0, 0, 0]
            string = ''
            for i in range(n):
                if board[i][3] == 0 and board[i][2] > 0:
                    stats1[0] += 1
                if board[i][3] == 0 and board[i][2] < 0:
                    stats1[0] += 1
                if (board[i][2] > 0 and board[i][3] > 0) or (board[i][2] < 0 and board[i][3] < 0):
                    stats1[2] += 1
                if (board[i][2] < 0 and board[i][3] > 0) or ((board[i][2] > 0 and board[i][3] < 0)):
                    stats1[1] += 1

            for i in stats1:
                string += str(i) + ' '
            string += str(t) + '\n'
            f.write(string)
            # print(string)


    return

def open_bounds_up(point):

    if point[1] == 400:
           counts[point[0]] = counts.get(point[0], 0) + 1
    return counts

global counts
counts = {}
def advance(board, n):
    global base
    global s2

    s2 = set()
    board = sorted(board).copy()
    base = board
    # print(board)
    # проверка всех точек из массива на условие взаимодействия
    for i in range(n - 3):
        collision(board[i], board[i + 1], board[i + 2], board[i + 3])

    if len(board) >= 6 :
        collision(board[-6], board[-5], board[-4], board[-3])
    if len(board) >= 5:
        collision(board[-5], board[-4], board[-3], board[-2])
    if len(board) >= 4:
        collision(board[-4], board[-3], board[-2], board[-1])

    newstate = []
    # перемещение точек за 1 дискретный момент времени
    for i in range(n):
        grid = 400
        speed = 1

        newstate.append([board[i][0] + board[i][2], board[i][1] + board[i][3], board[i][2], board[i][3],board[i][4]])
        #open_bounds_up(board[i])
        if right_out_of_bounds(board[i], grid, speed):
            newstate[i] = right_out_of_bounds(board[i], grid, speed)
        if left_out_of_bounds(board[i], grid, speed):
            newstate[i] = left_out_of_bounds(board[i], grid, speed)
        if up_out_of_bounds(board[i], grid, speed):
            newstate[i] = up_out_of_bounds(board[i], grid, speed)
        if down_out_of_bounds(board[i], grid, speed):
            newstate[i] = down_out_of_bounds(board[i], grid, speed)
    base = newstate

    return newstate

# сама анимация движения точек
def animate(i, data, mat):
    global n
    global coordinates
    global points
    global s

    coordinates = advance(coordinates, n)

    base = coordinates.copy()

    x, y, vx, vy,colour = zip(*coordinates)
    temp = np.array([x, y])
    mat.set_offsets(temp.transpose())
    mat.set_array(colour)
    mat.set_sizes([32]*n)
    s = s + str(coordinates)

    if int(time.process_time()) % 5 == 0:
        if len(quantity_of_points_time) != len(quantity_of_points_time | {int(time.process_time())}):
            quantity_of_points_time.add(int(time.process_time()))
            t = list(quantity_of_points_time)[-1]
            stats_of_points(coordinates, n, t)

    return mat,

global quantity_of_points_time , coords
quantity_of_points_time = set()
r = 100
# функция расположения начального фронта точек в виде идеальной капли
def sericle(r,coords):
    dp = dict.fromkeys(sorted(i[1] for i in coords))
    for y in dp.keys():
        dp[y] = sorted(set([i[0] for i in coords if i[1] == y]))
    for y in dp.keys():
        dp[y] = sorted(set(i for i in range(int(min(dp[y])), int(max(dp[y])) + 1, int(r) // 10)))
    for y in dp.keys():
        for x in dp[y]:
            coords |= {(x, y)}

    return
# создание начального фронта точек в виде пустой оболочки капли
points = []
coords = {(r*round(np.cos(fi), 1), r*round(np.sin(fi), 1)) for fi in [np.random.uniform(0, 2*np.pi) for i in range(1000)]}
points = [Point(p[0] + 120, p[1], -1, 0,0.5) for p in coords] + [Point(p[0] - 120, p[1]-150, 1, 0,0.1) for p in coords].copy()

sericle(r,coords)
points = [Point(p[0] + 200, p[1], -1, 0, 0.5) for p in coords]
points += [Point(p[0] - 200, p[1], 1, 0, 1) for p in coords].copy()
#points = [Point(50, i*2, -1, 0,0.5) for i in range(-200, 200,1)] + [Point(-50, i*2, 1, 0,0.5) for i in range(-200, 200,1)]
#points = [Point(50, i * 2, -1, 0,5) for i in range(-80, 80, 40)] + [Point(-50, i * 2, 1, 0) for i in range(-80, 80, 40)]

coordinates = [[i.x, i.y, i.vx, i.vy, i.colour] for i in points]

n = len(points)
print(n)

s = ''
fig, ax = plt.subplots()
fig.patch.set_facecolor('white')
fig.patch.set_alpha(1)
x, y, vx, vy, colour = zip(*coordinates)

mat = ax.scatter(x, y, 23, colour)
ax.axis([-400, 400, -400, 400])
ax.patch.set_facecolor('white')
ax.patch.set_alpha(1)
f = open("information.txt", 'w')
ani = animation.FuncAnimation(fig, animate, interval=1,fargs = (colour, mat) )
fig.subplots_adjust(left=0, bottom=0, top=1, right=1)

plt.show()
print(counts)
print(sum(counts.values()))
with open('bob.txt', 'w') as f:
    for key, value in counts.items():
        f.write(f"{key} {value}\n")