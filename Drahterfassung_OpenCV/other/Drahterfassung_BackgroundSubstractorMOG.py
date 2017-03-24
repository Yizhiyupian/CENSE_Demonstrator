import numpy as np
import cv2
import sys

bgSub=cv2.createBackgroundSubtractorMOG2()
for i in range(1,15):
    bgImageFile = "bg{0}.jpg".format(i)
    bg = cv2.imread(bgImageFile)
    bg=cv2.resize(bg,None,fx=0.125,fy=0.125)
    bgSub.apply(bg, learningRate=0.5)

stillFrame=cv2.imread('Still1.jpg')
stillFrame=cv2.resize(stillFrame,None,fx=0.125,fy=0.125)
fgmask=bgSub.apply(stillFrame, learningRate=0)

cv2.imshow('Original', stillFrame)
cv2.imshow('Masked', fgmask)
cv2.waitKey(0)
cv2.destroyAllWindows()