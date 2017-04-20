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


# an image or saved image will be color processed and the masks will be returned in an array
def color_vision(color, focus, bands, thresh, scale, name=None, image=None):
    # the bands will be saved into an array of masks
    masks = colorDetect(bands, color, focus, scale, name, image)
    rows, cols = masks[2].shape

    # an empty numpy array will be generated with the shape of the masks
    sum_mask = np.zeros((rows, cols), np.uint8)

    # all masks will be added together in a numpy array
    for i in range(len(masks)-3):
        sum_mask += masks[3+i]

    # any value above 'thresh' will be set to 1 and all the other values will be set to 0 creating a binary mask
    for i in range(rows):
        for j in range(cols):
            if sum_mask[i, j] >= thresh:
                sum_mask[i, j] = 1
            else:
                sum_mask[i, j] = 0

    # morphological transformations will be applied to the resulting mask to be able to remove noise
    kernel = np.ones((1,1), np.uint8)
    sum_mask = cv2.morphologyEx(sum_mask, cv2.MORPH_OPEN, kernel)
    sum_mask = cv2.morphologyEx(sum_mask, cv2.MORPH_CLOSE, kernel)
#    sum_mask = cv2.dilate(sum_mask, None, iterations=1)
#    sum_mask = cv2.morphologyEx(sum_mask, cv2.MORPH_OPEN, kernel)
#    sum_mask = cv2.morphologyEx(sum_mask, cv2.MORPH_OPEN, kernel)
#   sum_mask = cv2.morphologyEx(sum_mask, cv2.MORPH_CLOSE, kernel)
#   sum_mask = cv2.morphologyEx(sum_mask, cv2.MORPH_OPEN, kernel)
#   sum_mask = cv2.erode(sum_mask, None, iterations=1)

    # resulting mask will be applied to the original image to see what the camera sees from the mask and saved to masks
    res = cv2.bitwise_and(masks[0], masks[0], mask=sum_mask)
    masks.append(res)
    masks.append(sum_mask)
    return masks


def colorDetect(bands, color, focus, scale, name=None, image=None):
    # when no file path was specified but an image was given then process the image if not then return None
    if name is None:
        if image is None:
            return None
        else:
            img = image
    else:
        img = cv2.imread(name)

    # image is resized
    img = cv2.resize(img, None, fx=scale, fy=scale)

    # image color format is changed from bgr to rgb
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # the min hue and max hue are specified
    minp = color-focus[0]
    maxp = color

    # an Hue, Saturation, Value color formatted version of the image is saved on 'hsv' and saved to 'list' with original
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    list = [img, hsv]

    # the min range values for the color detection of OpenCV are initialized
    min_a = np.array([minp, focus[1], focus[3]])
    max_a = np.array([maxp, focus[2], focus[4]])

    # first band is calculated and saved in mask
    mask = cv2.inRange(hsv, min_a, max_a)

    # the process is repeated for the amount of bands needed
    for i in xrange(bands):
        minp += (focus[0])/bands
        maxp += (focus[0])/bands
        min_a = np.array([minp, focus[1], focus[3]])
        max_a = np.array([maxp, focus[2], focus[4]])
        mask = cv2.inRange(hsv, min_a, max_a)

        ret, mask_binary = cv2.threshold(mask, 1, 1, cv2.THRESH_BINARY)

        list.append(mask_binary)

    # masks and images are returned in an array of images
    return list


# no idea but it was recommended to write this here for the camera preview video stream
def nothing(x):
    pass


# a 'real-time' video stream of images processed by the color detection and sliders for the parameters will be shown
def preview_colors(color, focus, bands, thresh, scale):
    # object for image capture initialized for camera in port 1
    cap = cv2.VideoCapture(1)

    # the window is initialized with the name 'Settings'
    cv2.namedWindow('Settings')

    # trackbars are created and min values are set
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

    # video stream is displayed
    while True:
        # a frame is taken from the camera feed and saved in 'frame'
        __, frame = cap.read()

        # trackbar positions are read and saved onto the appropriate paramters
        color = cv2.getTrackbarPos('color', 'Settings')
        bands = cv2.getTrackbarPos('bands', 'Settings')
        thresh = cv2.getTrackbarPos('thresh', 'Settings')
        focus[0] = cv2.getTrackbarPos('bandwidth', 'Settings')
        focus[1] = cv2.getTrackbarPos('min S', 'Settings')
        focus[2] = cv2.getTrackbarPos('max S', 'Settings')
        focus[3] = cv2.getTrackbarPos('min H', 'Settings')
        focus[4] = cv2.getTrackbarPos('max H', 'Settings')

        # frame is filtered and displayed
        filtered = color_vision(color, focus, bands, thresh, scale, image=frame)
        gray = filtered[len(filtered)-1]*255
        gray = cv2.resize(gray, None, fx=1/scale, fy=1/scale)

        cv2.imshow('Preview', gray)

        # waits for the escape key to stop the video stream and save the trackbar values onto the appropriate parameters
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

    # returns the filter parameters
    return bands, thresh, color, focus
