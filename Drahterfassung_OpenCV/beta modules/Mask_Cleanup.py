"""
===========================
@Author  : aguajardo<aguajardo.me>
@Version: 1.0    24/03/2017
This is a color detection method that allows to focus onto the
color being detected with color variance.
===========================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import Color_Detection as colors


class Agents:
    agents = []
    agents_temp = []


def sync_agents():
    Agents.agents = np.array(Agents.agents_temp)

def neighbours(x, y, image):
    img = image
    x_1, y_1, x1, y1 = x - 1, y - 1, x + 1, y + 1
    return [img[x_1][y], img[x_1][y1], img[x][y1], img[x1][y1],  # u,ur,r,dr
            img[x1][y], img[x1][y_1], img[x][y_1], img[x_1][y_1]]  # d,dl,l,ul


def alive(agent, mask):
    Agents.agents_temp.append(agent)
    mask[agent[0]][agent[1]] = 1


def dead(agent, mask):
    mask[agent[0]][agent[1]] = 0
    Agents.agents_temp.remove([agent[0], agent[1]])


def move(agent, directions, mask):
    position = list(agent)
    for i in range(len(directions)):
        if directions[i] == 0:
            if i == 0:
                dead(agent, mask)
                position[1] += 1
                alive(position, mask)
                return
            if i == 1:
                dead(agent, mask)
                position[0] += 1
                position[1] += 1
                alive(position, mask)
                return
            if i == 2:
                dead(agent, mask)
                position[0] += 1
                alive(position, mask)
                return
            if i == 3:
                dead(agent, mask)
                position[0] += 1
                position[1] -= 1
                alive(position, mask)
                return
            if i == 4:
                dead(agent, mask)
                position[1] -= 1
                alive(position, mask)
                return
            if i == 5:
                dead(agent, mask)
                position[0] -= 1
                position[1] -= 1
                alive(position, mask)
                return
            if i == 6:
                dead(agent, mask)
                position[0] -= 1
                alive(position, mask)
                return
            if i == 7:
                dead(agent, mask)
                position[0] -= 1
                position[1] += 1
                alive(position, mask)
                return


def reproduce(agent, directions, mask):
    position = list(agent)
    for i in range(len(directions)):
        if directions[i] == 0:
            if i == 0:
                position[1] += 1
                alive(position, mask)
                return
            if i == 1:
                position[0] += 1
                position[1] += 1
                alive(position, mask)
                return
            if i == 2:
                position[0] += 1
                alive(position, mask)
                return
            if i == 3:
                position[0] += 1
                position[1] -= 1
                alive(position, mask)
                return
            if i == 4:
                position[1] -= 1
                alive(position, mask)
                return
            if i == 5:
                position[0] -= 1
                position[1] -= 1
                alive(position, mask)
                return
            if i == 6:
                position[0] -= 1
                alive(position, mask)
                return
            if i == 7:
                position[0] -= 1
                position[1] += 1
                alive(position, mask)
                return


name = 'Bilder\Test6.png'
scale = 1
bands = 8
thresh = 3
color = 25
focus = [25, 35, 255, 35, 255]
images = colors.color_vision(color, focus, bands, thresh, scale, name)

mask = np.array(images[len(images)-1])

roi = mask[190:215, 0:25]
rows, cols = roi.shape

for x in range(cols):
    for y in range(rows):
        if roi[y][x] == 1:
            p_1 = [y+190, x]
            break
    if roi[y][x] == 1:
        p_1 = [y+190, x]
        break


rows, cols = mask.shape
print([rows, cols])
new_mask = np.zeros((rows, cols), np.uint8)



ret, mask = cv2.threshold(mask, 0, 1, cv2.THRESH_BINARY_INV)


population = 0
max_population = 4000
pop_change = True


alive(p_1, new_mask)
sync_agents()
cv2.imshow('original', mask*255)

while True:
    pop_change = False
    for agent in Agents.agents:
        temp = cv2.bitwise_or(mask, new_mask)
        if population != max_population:
            u, ur, r, dr, d, dl, l, ul = neighbours(agent[0], agent[1], temp)
            connections = u+ur+r+dr+d+dl+l+ul
            directions = [r, dr, d, dl, l, ul, u, ur]
            if connections < 8:
                reproduce(agent, directions, new_mask)
                population += 1
                pop_change = True
        else:
            u, ur, r, dr, d, dl, l, ul = neighbours(agent[0], agent[1], temp)
            connections = u + ur + r + dr + d + dl + l + ul
            directions = [r, dr, d, dl, l, ul, u, ur]
            if connections < 8:
                move(agent, directions, new_mask)
                pop_change = True
    sync_agents()
    print(len(Agents.agents))
    cv2.imshow('New',  * 255)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

sum = 0
for i in range(rows):
    for j in range(cols):
       if new_mask[i][j]==1:
           sum+=1
print(sum)

cv2.destroyAllWindows()