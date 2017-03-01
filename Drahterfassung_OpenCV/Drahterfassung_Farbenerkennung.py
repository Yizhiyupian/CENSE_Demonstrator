import numpy as np
import cv2

LOWER = np.array([160, 160, 220], dtype='uint8')
UPPER = np.array([250, 250, 255], dtype='uint8')

img = cv2.imread('Bilder\Draht1.jpg')
img = cv2.resize(img, None, fx=0.125, fy=0.125)
mask = cv2.inRange(img, LOWER, UPPER)
output = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow('Filtered', np.hstack([img, output]))
cv2.waitKey(0)

