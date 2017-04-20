"""
===========================
@Author  : aguajardo<aguajardo.me>
@Version: 1.0    24/03/2017
This is a module for taking images from a
webcam and saving them as a png.
===========================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import Color_Detection as colors

def preview_colors(color, focus, bands, thresh, scale):
    cap = cv2.VideoCapture(0)

    while True:
        __, frame = cap.read()
        filtered = colors.color_vision(color, focus, bands, thresh, scale, image=frame)
        gray = filtered[len(filtered)-1]*255
        gray = cv2.resize(gray, None, fx=1/scale, fy=1/scale)

        cv2.imshow('filtered', gray)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

    return

scale = 0.7
bands = 8
thresh = 3
color = 25
focus = [25, 35, 255, 35, 255]

preview_colors(color, focus, bands, thresh, scale)