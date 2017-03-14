import numpy as np
import cv2
import Thinning as skelet
import matplotlib.pyplot as plt

SCALE = 0.25
img = cv2.imread('Bilder\Draht1.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

LOWER_GREEN = np.array([10,30,50])
UPPER_GREEN = np.array([40,100,255])

mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
mask = cv2.dilate(mask, None, iterations=5)
mask = cv2.erode(mask, None, iterations=5)
res = cv2.bitwise_and(img, img, mask=mask)

img = cv2.resize(img, None, fx=SCALE, fy=SCALE)
res = cv2.resize(res, None, fx=SCALE, fy=SCALE)
hsv = cv2.resize(hsv, None, fx=SCALE, fy=SCALE)
mask = cv2.resize(mask, None, fx=SCALE, fy=SCALE)

ret,mask_binary = cv2.threshold(mask,1,1,cv2.THRESH_BINARY)

skeleton = skelet.zhangSuen(mask_binary)

titles = ['Original Image','Binary Mask','Result','Skeleton']
images = [img, mask_binary, res, skeleton]
for i in xrange(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()