"""
===========================
@Author  : Linbo<linbo>
@Edited by: aguajardo<aguajardo.me>
@Version: 1.0    25/10/2014
This is the implementation of the
Zhang-Suen Thinning Algorithm for skeletonization.
===========================
"""

import matplotlib
import matplotlib.pyplot as plt
#import skimage.io as io
import numpy as np

def neighbours(x, y, image):
    "Return 8-neighbours of image point P1(x,y), in a clockwise order"
    img = image
    x_1, y_1, x1, y1 = x - 1, y - 1, x + 1, y + 1
    return [img[x_1][y], img[x_1][y1], img[x][y1], img[x1][y1],  # P2,P3,P4,P5
            img[x1][y], img[x1][y_1], img[x][y_1], img[x_1][y_1]]  # P6,P7,P8,P9


def transitions(neighbours):
    "No. of 0,1 patterns (transitions from 0 to 1) in the ordered sequence"
    n = neighbours + neighbours[0:1]  # P2, P3, ... , P8, P9, P2
    return sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]))  # (P2,P3), (P3,P4), ... , (P8,P9), (P9,P2)


def zhangSuen(image):
    "the Zhang-Suen Thinning Algorithm"
    Image_Thinned = image.copy()  # deepcopy to protect the original image
    r, c = image.shape
    Test = np.zeros((r,c),np.uint8)
    changing1 = changing2 = changing3 = 1  # the points to be removed (set as 0)
    while changing1 or changing2:  # iterates until no further changes occur in the image
        # Step 1
        changing1 = []
        rows, columns = Image_Thinned.shape  # x for rows, y for columns
        for x in range(1, rows - 1):  # No. of  rows
            for y in range(1, columns - 1):  # No. of columns
                P2, P3, P4, P5, P6, P7, P8, P9 = n = neighbours(x, y, Image_Thinned)
                if (Image_Thinned[x][y] == 1 and  # Condition 0: Point P1 in the object regions
                                2 <= sum(n) <= 6 and  # Condition 1: 2<= N(P1) <= 6
                            transitions(n) == 1 and  # Condition 2: S(P1)=1
                                    P2 * P4 * P6 == 0 and  # Condition 3
                                    P4 * P6 * P8 == 0):  # Condition 4
                    changing1.append((x, y))
        for x, y in changing1:
            Image_Thinned[x][y] = 0
        # Step 2
        changing2 = []
        for x in range(1, rows - 1):
            for y in range(1, columns - 1):
                P2, P3, P4, P5, P6, P7, P8, P9 = n = neighbours(x, y, Image_Thinned)
                if (Image_Thinned[x][y] == 1 and  # Condition 0
                                2 <= sum(n) <= 6 and  # Condition 1
                            transitions(n) == 1 and  # Condition 2
                                    P2 * P4 * P8 == 0 and  # Condition 3
                                    P2 * P6 * P8 == 0):  # Condition 4
                    changing2.append((x, y))
        for x, y in changing2:
            Image_Thinned[x][y] = 0
    while changing3:
        # Step 3
        changing3 = 0
        rows, columns = Image_Thinned.shape  # x for rows, y for columns
        for x in range(1, rows - 1):
            for y in range(1, columns - 1):
                P2, P3, P4, P5, P6, P7, P8, P9 = n = neighbours(x, y, Image_Thinned)
                if Image_Thinned[x][y]==0 and ((P2 + P4 == 2 and P5 + P7 + P9 <= 2 and P6 + P8 + P3 == 0) or
                                                (P4 + P6 == 2 and P3 + P7 + P9 <= 2 and P8 + P2 + P5 == 0) or
                                                (P6 + P8 == 2 and P3 + P5 + P9 <= 2 and P2 + P4 + P7 == 0) or
                                                (P8 + P2 == 2 and P3 + P5 + P7 <= 2 and P4 + P6 + P9 == 0)):
                    changing3 = 1
                    Test[x][y] = 1
                    Image_Thinned[x][y] = 1

    return Image_Thinned