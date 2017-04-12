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


def color_vision(color, focus, bands, thresh, scale, name=None, image=None):
    masks = colorDetect(bands, color, focus, scale, name, image)
    rows, cols = masks[2].shape
    sum_mask = np.zeros((rows, cols), np.uint8)

    for i in range(len(masks)-3):
        sum_mask += masks[3+i]

    for i in range(rows):
        for j in range(cols):
            if sum_mask[i, j] >= thresh:
                sum_mask[i, j] = 1
            else:
                sum_mask[i, j] = 0
    kernel = np.ones((1,1), np.uint8)
    sum_mask = cv2.morphologyEx(sum_mask, cv2.MORPH_OPEN, kernel)
    sum_mask = cv2.morphologyEx(sum_mask, cv2.MORPH_CLOSE, kernel)
#    sum_mask = cv2.dilate(sum_mask, None, iterations=1)
#    sum_mask = cv2.morphologyEx(sum_mask, cv2.MORPH_OPEN, kernel)
#    sum_mask = cv2.morphologyEx(sum_mask, cv2.MORPH_OPEN, kernel)
#   sum_mask = cv2.morphologyEx(sum_mask, cv2.MORPH_CLOSE, kernel)
#   sum_mask = cv2.morphologyEx(sum_mask, cv2.MORPH_OPEN, kernel)
#   sum_mask = cv2.erode(sum_mask, None, iterations=1)
    res = cv2.bitwise_and(masks[0], masks[0], mask=sum_mask)
    masks.append(res)
    masks.append(sum_mask)
    return masks


def colorDetect(bands, color, focus, scale, name=None, image=None):
    if name is None:
        if image is None:
            return None
        else:
            img = image
    else:
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


def nothing(x):
    pass


def preview_colors(color, focus, bands, thresh, scale):
    cap = cv2.VideoCapture(1)
    cv2.namedWindow('Settings')

    cv2.createTrackbar('color', 'Settings', color, 180, nothing)
    cv2.createTrackbar('bands', 'Settings', bands, 20, nothing)
    cv2.createTrackbar('thresh', 'Settings', thresh, 20, nothing)
    cv2.createTrackbar('bandwidth', 'Settings', focus[0], 180, nothing)
    cv2.createTrackbar('min S', 'Settings', focus[1], 255, nothing)
    cv2.createTrackbar('max S', 'Settings', focus[2], 255, nothing)
    cv2.createTrackbar('min H', 'Settings', focus[3], 255, nothing)
    cv2.createTrackbar('max H', 'Settings', focus[4], 255, nothing)
    cv2.setTrackbarMin('bands', 'Settings', 1)
    cv2.setTrackbarMin('thresh', 'Settings', 1)

    while True:
        __, frame = cap.read()
        color = cv2.getTrackbarPos('color', 'Settings')
        bands = cv2.getTrackbarPos('bands', 'Settings')
        thresh = cv2.getTrackbarPos('thresh', 'Settings')
        focus[0] = cv2.getTrackbarPos('bandwidth', 'Settings')
        focus[1] = cv2.getTrackbarPos('min S', 'Settings')
        focus[2] = cv2.getTrackbarPos('max S', 'Settings')
        focus[3] = cv2.getTrackbarPos('min H', 'Settings')
        focus[4] = cv2.getTrackbarPos('max H', 'Settings')

        filtered = color_vision(color, focus, bands, thresh, scale, image=frame)
        gray = filtered[len(filtered)-1]*255
        gray = cv2.resize(gray, None, fx=1/scale, fy=1/scale)

        cv2.imshow('Preview', gray)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

    return bands, thresh, color, focus
