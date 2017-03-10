import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image

# Import image with PIL
img = Image.open('Bilder\Draht1.jpg')

# Rotate image 180 degrees
img_r = img.rotate(180, expand=True)

# Transform image into Numpy Array
img_r = np.array(img_r)

# RGB to BGR
# img_r = img_r[:, :, ::-1].copy()

# Resize image
img_rs = cv2.resize(img_r, None, fx=0.125, fy=0.125, interpolation=cv2.INTER_CUBIC)

# Create a mask for the image
mask = np.zeros(img_rs.shape[:2], np.uint8)

# Create models for both the background and foreground
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

rect = (50, 110, 440, 275)
cv2.grabCut(img_rs,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
img_m = img_rs*mask2[:, :, np.newaxis]


# Show image
plt.imshow(img_m)
plt.show()