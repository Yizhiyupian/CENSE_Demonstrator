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

# camera port and amount of frames to be discarded while focusing
port = 1
frames = 5


# class with variables needed to know if camera is in use or not
class Kamera:
    cam = None
    released = True


# camera is released for further use
def release_cam():
    Kamera.cam = None
    Kamera.released = True


# image is taken and returned
def get_image():
    if Kamera.released:
        Kamera.cam = cv2.VideoCapture(port)
        Kamera.released = False

    im = get_image_internal()

    return im


# image is taken and returned without initializing the camera
def get_image_internal():
    retval = False

    while not retval:
        retval, im = Kamera.cam.read()

    return im


# image is taken, undistorted and saved to the file path in 'name'
def capture_image(name):
    if Kamera.released:
        Kamera.cam = cv2.VideoCapture(port)
        Kamera.released = False

    for i in xrange(frames):
        temp = get_image_internal()

    camera_capture = get_image_internal()

    release_cam()

    # image is transformed into undistorted version using the module Kalibrierung.py
    camera_capture = cal.undistort_img(camera_capture)

    cv2.imwrite(name, camera_capture)