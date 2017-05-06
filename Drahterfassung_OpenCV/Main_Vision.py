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
import Drahterfassung_OpenCV.Color_Detection as colors
import Drahterfassung_OpenCV.Thinning as skelet
import Drahterfassung_OpenCV.Kamera as cam


# takes a picture and saves it in the file path 'name', processes it and saves the processed image as 'world_img.png'
def take_picture():
    # file path
    name = 'Drahterfassung_OpenCV\Bilder\camera_picture.png'

    # scale at which the image will be processed
    scale = 0.7

    # the color focus area will be segmented into color bands this states how many bands will be analyzed
    bands = 8

    # minimum amount of bands in which a pixel has to be to make it to the resulting mask
    thresh = 3

    # color hue to be looked for
    color = 25

    # variation range for hue, saturation, and value e.g.: color+focus = max_hue, color-focus = min_hue
    focus = [25, 35, 255, 35, 255]

    # a 'real-time' video feed with the color detection filter will be shown
    bands, thresh, color, focus = colors.preview_colors(color, focus, bands, thresh, scale)

    # an image will be captured and saved in the file path 'name'
    cam.capture_image(name)

    # a series of masks will be generated and saved onto 'images'
    images = colors.color_vision(color, focus, bands, thresh, scale, name)

    # the resulting mask saved in images will be turned into a binary mask
    ret, mask_binary = cv2.threshold(images[len(images)-1], 0, 1, cv2.THRESH_BINARY)

    # the dimensions of the image will be saved in rows and cols to calculate the scaling_constant and superimpose image
    rows, cols = images[len(images)-1].shape

    # the mask is then run through a thinning algorithm to generate a 1 pixel wide line
    skeleton = skelet.zhangSuen(mask_binary)

    # superimposes the skeleton image on the original image
    img_skelet = np.zeros((rows, cols, 3), np.uint8)

    for i in range(cols):
        for j in range(rows):
            if skeleton[j, i] == 1:
                img_skelet[j, i] = [255, 0, 0]
            else:
                img_skelet[j, i] = images[0][j, i]

    gray_skeleton = np.zeros((rows, cols, 3), np.uint8)
    rows, cols = skeleton.shape
    for i in range(rows):
        for j in range(cols):
            if skeleton[i, j] == 1:
                gray_skeleton[i, j] = [255, 255, 255]
            else:
                gray_skeleton[i, j] = [0, 0, 0]

    images.append(img_skelet)
    images.append(skeleton)

    cv2.imwrite('Drahterfassung_OpenCV\Bilder\world_img.png', gray_skeleton)

    # returns the images in an array
    return images


# plots the HSV, superimposed image, binary mask, and the skeleton
def plot_images(images):
    titles = ['Original Image', 'Result', 'Binary Mask', 'Skeleton']
    plot = [images[1], images[len(images)-2], images[len(images)-3], images[len(images)-1]]

    for i in range(len(plot)):
        plt.subplot(2,2,i+1),plt.imshow(plot[i])
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()

#plot_images(take_picture())