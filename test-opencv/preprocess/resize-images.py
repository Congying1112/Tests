import cv2
import os
import glob
import sys

for f in glob.glob(os.path.join(sys.argv[1], "*.JPG")):
    img1 = cv2.imread(f, 0)
    shape = (1280, 960)
    img1 = cv2.resize(img1, shape)
    cv2.imwrite(f, img1)
