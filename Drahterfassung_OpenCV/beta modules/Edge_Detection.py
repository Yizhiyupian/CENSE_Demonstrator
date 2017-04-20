"""
===========================
@Author  : aguajardo<aguajardo.me>
@Version: 1.0    28/03/2017
This is a color detection method that allows to focus onto the
color being detected with color variance.
===========================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def edge_vision(name, minval, maxval, apsize, scale):
    img = cv2.imread(name,0)
    img = cv2.resize(img, None, fx=scale, fy=scale)

    edges = cv2.Canny(img, minval, maxval, apertureSize=apsize, L2gradient=True)
    ret, edges_binary = cv2.threshold(edges, 1, 1, cv2.THRESH_BINARY_INV)



    return edges_binary

cv2.imshow('edges', edge_vision('Bilder\Test6.png', 100, 200, 3, 1)*255)
cv2.waitKey(0)