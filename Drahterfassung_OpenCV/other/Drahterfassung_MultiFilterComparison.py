import numpy as np
import cv2
import Thinning as skelet
import matplotlib.pyplot as plt

SCALE = 0.1
img = cv2.imread('Bilder\Draht1.jpg')
img = cv2.resize(img, None, fx=SCALE, fy=SCALE)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

LOWER_GREEN = np.array([15,45,50])
UPPER_GREEN = np.array([35,100,255])

mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
mask = cv2.dilate(mask, None, iterations=6)
mask = cv2.erode(mask, None, iterations=5)
res = cv2.bitwise_and(img, img, mask=mask)


ret, mask_binary = cv2.threshold(mask, 1, 1, cv2.THRESH_BINARY)

skeleton = skelet.zhangSuen(mask_binary)
rows, cols, __ = img.shape
img_skelet = np.zeros((rows, cols, 3), np.uint8)

for i in range(cols):
    for j in range(rows):
        if skeleton[j, i] == 1:
            img_skelet[j, i] = [0, 255, 0]
        else:
            img_skelet[j, i] = img[j, i]

titles = ['Original Image', 'Result', 'Binary Mask', 'Skeleton']
images = [img, img_skelet, mask_binary, skeleton]
for i in xrange(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i])
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

