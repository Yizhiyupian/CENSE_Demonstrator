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
import Kalibrierung as cal

port = 1
frames = 35

class Kamera:
    cam = None
    released = True


def release_cam():
    Kamera.cam = None
    Kamera.released = True


def get_image():
    if Kamera.released:
        Kamera.cam = cv2.VideoCapture(port)
        Kamera.released = False

    im = get_image_internal()

    return im


def get_image_internal():
    retval = False

    while not retval:
        retval, im = Kamera.cam.read()

    return im


def capture_image(name):
    if Kamera.released:
        Kamera.cam = cv2.VideoCapture(port)
        Kamera.released = False

    for i in xrange(frames):
        temp = get_image_internal()

    camera_capture = get_image_internal()

    release_cam()

    camera_capture = cal.undistort_img(camera_capture)

    cv2.imwrite(name, camera_capture)
    #capture_image('Bilder\Test5.png')