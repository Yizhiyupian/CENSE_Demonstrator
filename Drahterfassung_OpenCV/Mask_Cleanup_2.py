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
from random import randint


class Agents:
    agents = []
    agents_temp = []


def sync_agents():
    Agents.agents = np.array(Agents.agents_temp)

def neighbours(x, y, image):
    img = image
    x_1, y_1, x1, y1 = x - 1, y - 1, x + 1, y + 1
    return [img[x_1][y], img[x][y1],  # u,ur,r,dr
            img[x1][y], img[x][y_1]]  # d,dl,l,ul


def alive(agent, mask):
    Agents.agents_temp.append(agent)
    mask[agent[0]][agent[1]] = 1


def dead(agent, mask):
    mask[agent[0]][agent[1]] = 0
    Agents.agents_temp.remove([agent[0], agent[1]])


def reproduce(agent, directions, mask):
    position = list(agent)
    random = randint(0, 3)
    if directions[random] == 0:
        if random == 0:
            position[1] += 1
            alive(position, mask)
            return
        if random == 1:
            position[0] += 1
            alive(position, mask)
            return
        if random == 2:
            position[1] -= 1
            alive(position, mask)
            return
        if random == 3:
            position[0] -= 1
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
            p_1 = [y+190+1, x+1]
            break
    if roi[y][x] == 1:
        p_1 = [y+190+1, x+1]
        break

cv2.imshow('roi', roi*255)
rows, cols = mask.shape
print([rows, cols])
new_mask = np.zeros((rows, cols), np.uint8)



ret, mask = cv2.threshold(mask, 0, 1, cv2.THRESH_BINARY_INV)


alive(p_1, new_mask)
sync_agents()

cv2.imshow('original', mask*255)

while True:
    temp = cv2.bitwise_or(mask, new_mask)
    u, r, d, l = neighbours(Agents.agents[len(Agents.agents)-1][0], Agents.agents[len(Agents.agents)-1][1], temp)
    connections = u+r+d+l
    directions = [r, d, l, u]
    if connections <= 2:
        reproduce(Agents.agents[len(Agents.agents)-1], directions, new_mask)
        sync_agents()
    else:
        length = len(Agents.agents)
        while len(Agents.agents)!= 1 and len(Agents.agents) > length-4:
            dead(Agents.agents[len(Agents.agents)-1], new_mask)
            sync_agents()

    print(len(Agents.agents))

    cv2.imshow('New', temp * 255)
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