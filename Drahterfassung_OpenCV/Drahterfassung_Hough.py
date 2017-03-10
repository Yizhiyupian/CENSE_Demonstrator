import numpy as np
import cv2
from PIL import Image


img = cv2.imread('Bilder\Draht1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

minLineLength = 1
maxLineGap = 20
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
print('Lines found: {}'.format(len(lines)))

for i in range(0,len(lines)):
    for x1,y1,x2,y2 in lines[i]:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),10)


img = cv2.resize(img, None, fx=0.25, fy=0.25)
cv2.imshow('houghlines5.jpg',img)
cv2.waitKey()





