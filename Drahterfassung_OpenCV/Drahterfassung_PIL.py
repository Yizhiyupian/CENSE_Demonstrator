from PIL import Image
from PIL import ImageChops
import numpy as np
from matplotlib import pyplot as plt

image1=Image.open('Bilder\im1.jpg')
image2=Image.open('Bilder\im2.jpg')

image=ImageChops.subtract(image2, image1)

mask1=Image.eval(image, lambda a: 0 if a<=10 else 255)
mask2=mask1.convert('1')

blank=Image.eval(image, lambda a:0 )
new=Image.composite(image2, blank, mask2)
img=np.array(new)
plt.imshow(img)
plt.show()