"""
===========================
@Author  : aguajardo<aguajardo.me>
@Version: 1.0    24/03/2017
This is a camera calibration method.
===========================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from Drahterfassung_OpenCV import Kamera as cam
import time
from Drahterfassung_OpenCV.calibration_vars import objpv
from Drahterfassung_OpenCV.calibration_vars import imgpv
import Drahterfassung_OpenCV.Color_Detection as colors


class Points:
    # Arrays to store object points and image points from all the images.
    objpoints = objpv
    imgpoints = imgpv


def save_file():
    # Save points to python file
    with open('calibration_vars.py', 'w') as f:
        f.write('from numpy import *')
        f.write('\n\nobjpv = %s' % str(Points.objpoints))
        f.write('\n\nimgpv = %s' % str(Points.imgpoints))


def calibrate():
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points
    objp = np.zeros((6*8,3), np.float32)
    objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

    # empty list to hold the pictures
    images = []

    # counter for amount of images with chessboard found
    count = 0

    for j in range(10):
        print('Pictures will be taken in 5 seconds.')
        time.sleep(5)

        # stores 15 pictures into images
        for i in range(15):
            print ('Taking picture %i out of 15' % int(i+1))
            images.append(cam.get_image())

        # checks all images for chessboard corners
        print ('Scanning for chessboard.')
        for img in images:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (8,6), None)

            # If found, add object points, image points (after refining them) and break the loop to take new images
            if ret:
                count += 1
                Points.objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                Points.imgpoints.append(corners2)
                print ('%i chessboards found out of 10' % int(count))
                break
    cam.release_cam()
    save_file()


def undistort_img(img):
    # checks to see if camera has been calibrated
    if Points.objpoints == [] or Points.imgpoints == []:
        print('Camera must be calibrated. Press enter to continue into calibration mode.')
        calibrate()

    # Image is turn into gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # gets the calibration matrix and optimizes it
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(Points.objpoints, Points.imgpoints, gray.shape[::-1], None, None)
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    # undistorts the image
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x, y, w, h = roi

    # returns the image
    dst = dst[y:y + h, x:x + w]
    return dst


def perspective_undistort(image):
    # scale at which the image will be processed
    scale = 0.7

    # the color focus area will be segmented into color bands this states how many bands will be analyzed
    bands = 8

    # minimum amount of bands in which a pixel has to be to make it to the resulting mask
    thresh = 3

    # color hue to be looked for
    color = 85

    # variation range for hue, saturation, and value e.g.: color+focus = max_hue, color-focus = min_hue
    focus = [25, 35, 255, 35, 255]

    # image is color analyzed to find the location of the corner points
    images = colors.color_vision(color, focus, bands, thresh, scale, image=image)

    # contours of the corner points are calculated
    im2, contours, hierarchy = cv2.findContours(images[len(images)-1], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # array with the coordinates of the center points of the corner points are saved on an array
    center_points = []
    for cnt in contours:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center_points.append([int(x), int(y)])

    # center point coordinates and end coordinates for the corner center points are prepped for the transformation
    rows, cols = images[len(images)-1].shape
    pts1 = np.float32(center_points)
    pts2 = np.float32([[0, 0], [rows, 0], [0, cols], [rows, cols]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    undistorted = cv2.warpPerspective(image, M, (rows, cols))

    return undistorted
