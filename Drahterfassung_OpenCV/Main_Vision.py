"""
===========================
@Author  : aguajardo<aguajardo.me>
@Version: 1.0    24/03/2017
This is a module for detecting a cable
with use of color detection and then
skeletonizing it with the Zhan-Suen
thinning algorithm.
===========================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import Color_Detection as colors
import Thinning as skelet
import Kamera as cam

name = 'Bilder\Test5.png'
scale = 0.5
bands = 8
thresh = 3
color = 25
focus = [25, 35, 255, 35, 255]
bands, thresh, color, focus = colors.preview_colors(color, focus, bands, thresh, scale)
cam.capture_image(name)
images = colors.color_vision(color, focus, bands, thresh, scale, name)

ret, mask_binary = cv2.threshold(images[len(images)-1], 0, 1, cv2.THRESH_BINARY)
rows, cols = images[len(images)-1].shape
skeleton = skelet.zhangSuen(mask_binary)
img_skelet = np.zeros((rows, cols, 3), np.uint8)

for i in range(cols):
    for j in range(rows):
        if skeleton[j, i] == 1:
            img_skelet[j, i] = [255, 0, 0]
        else:
            img_skelet[j, i] = images[0][j, i]


images.append(img_skelet)
titles = ['Original Image', 'Result', 'Binary Mask', 'Skeleton']
plot = [images[1], images[len(images)-1], images[len(images)-2], skeleton]

for i in xrange(len(plot)):
    plt.subplot(2,2,i+1),plt.imshow(plot[i])
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()