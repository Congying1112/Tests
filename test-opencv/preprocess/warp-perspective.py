import cv2
import glob
import numpy as np
import os
import sys


M = np.matrix([[1.4620284333381663e+00, -1.1614798778742078e-03, 1.2750408637273040e+02],
                 [1.5408265591710199e-02, 1.6452529683578421e+00, 9.3094557880668560e+01],
                 [8.9480317554233113e-06, 1.5040531719712985e-05, 1.]])

pts1 = np.float32([[419, 96], [594, 97], [855, 100], [417, 488], [591, 489], [851, 490], [415, 876], [589, 878], [848, 881]])
delta_x = 60
x0 = 200 + delta_x
x1 = 320 + delta_x
x2 = 500 + delta_x
delta_y = 50
y0 = 0 + delta_y
y1 = 240 + delta_y
y2 = 480 + delta_y
pts2 = np.float32([[x0, y0], [x1, y0], [x2, y0], [x0, y1], [x1, y1], [x2, y1], [x0, y2], [x1, y2], [x2, y2]])

M, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC)
for f in glob.glob(os.path.join(sys.argv[1], "*.JPG")):
    img1 = cv2.imread(f, 0)
    shape = (1280, 960)
    img1 = cv2.resize(img1, shape)
    # cv2.imshow("a", img1)
    img2 = cv2.warpPerspective(img1, M, (840, 580), cv2.INTER_NEAREST | cv2.WARP_INVERSE_MAP | cv2.WARP_FILL_OUTLIERS)
    # cv2.imshow("b", img2)
    # cv2.waitKey(-1)
    cv2.imwrite(f, img2)
