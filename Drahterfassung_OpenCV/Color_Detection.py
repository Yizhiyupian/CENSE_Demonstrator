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

def color_vision(name, color, focus, bands, thresh, scale):
    masks = colorDetect(name, bands, color, focus, scale)
    rows, cols = masks[3].shape
    sum_mask = np.zeros((rows, cols), np.uint8)

    for i in range(len(masks)-3):
        sum_mask += masks[3+i]

    for i in range(rows):
        for j in range(cols):
            if sum_mask[i, j] >= thresh:
                sum_mask[i, j] = 1
            else:
                sum_mask[i, j] = 0
    sum_mask = cv2.dilate(sum_mask, None, iterations=6)
    sum_mask = cv2.erode(sum_mask, None, iterations=5)
    res = cv2.bitwise_and(masks[0], masks[0], mask=sum_mask)
    masks.append(res)
    masks.append(sum_mask)
    return masks


def colorDetect(name, bands, color, focus, scale):

    img = cv2.imread(name)
    img = cv2.resize(img, None, fx=scale, fy=scale)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    minp = color-focus[0]
    maxp = color
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    list = [img, hsv]
    min_a = np.array([minp, focus[1], focus[3]])
    max_a = np.array([maxp, focus[2], focus[4]])
    mask = cv2.inRange(hsv, min_a, max_a)

    for i in xrange(bands):
        minp += (focus[0])/bands
        maxp += (focus[0])/bands
        min_a = np.array([minp, focus[1], focus[3]])
        max_a = np.array([maxp, focus[2], focus[4]])
        mask = cv2.inRange(hsv, min_a, max_a)

        ret, mask_binary = cv2.threshold(mask, 1, 1, cv2.THRESH_BINARY)

        list.append(mask_binary)

    return list

