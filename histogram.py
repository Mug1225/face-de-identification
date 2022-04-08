import cv2
import numpy as np
from matplotlib import pyplot as plt
img=cv2.imread('face.jpg',0)
plt.hist(img.ravel(),256,[0,256]); plt.show()

img=cv2.imread('enc.jpg',0)
plt.hist(img.ravel(),256,[0,256]); plt.show()
