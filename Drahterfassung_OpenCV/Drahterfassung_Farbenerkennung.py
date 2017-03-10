import numpy as np
import cv2

SCALE = 0.25
img = cv2.imread('Bilder\Draht1.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

LOWER_GREEN = np.array([10,30,50])
UPPER_GREEN = np.array([40,150,255])

mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
mask = cv2.dilate(mask, None)
mask = cv2.dilate(mask, None)
mask = cv2.dilate(mask, None)
mask = cv2.dilate(mask, None)
mask = cv2.dilate(mask, None)
mask = cv2.erode(mask, None)
mask = cv2.erode(mask, None)
mask = cv2.erode(mask, None)
mask = cv2.erode(mask, None)
mask = cv2.erode(mask, None)
res = cv2.bitwise_and(img, img, mask=mask)

img2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, 0, (0,255,0), 3)

img = cv2.resize(img, None, fx=SCALE, fy=SCALE)
res = cv2.resize(res, None, fx=SCALE, fy=SCALE)
hsv = cv2.resize(hsv, None, fx=SCALE, fy=SCALE)
mask = cv2.resize(mask, None, fx=SCALE, fy=SCALE)

cv2.imshow('Image', img)
cv2.imshow('RES', res)
cv2.imshow('HSV', hsv)
cv2.imshow('MASK', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()


