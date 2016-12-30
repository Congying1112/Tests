import numpy as np
import cv2
from matplotlib import pyplot as plt

image = cv2.imread('1.jpg', 0)

# Initiate STAR detector
surf = cv2.xfeatures2d.SURF_create()

# find the keypoints & descriptors
kp, des = surf.detectAndCompute(image, None)

# draw only keypoints location,not size and orientation
dummy = np.zeros((1,1))
img2 = cv2.drawKeypoints(image, kp, dummy, color=(0,255,0), flags=0)

cv2.imwrite("surf.jpg", img2)