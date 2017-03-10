import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('Bilder\Buddah3.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.resize(img, None, fx=0.125, fy=0.125)
gray = cv2.resize(gray, None, fx=0.125, fy=0.125)
retval, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
retval2, otsu = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
gaus = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)


cv2.imshow('Gray', gray)
cv2.imshow('Image', img)
cv2.imshow('Threshold', thresh)
cv2.imshow('Gaus', gaus)
cv2.imshow('OTSU', otsu)

cv2.waitKey(0)
cv2.destroyAllWindows()
