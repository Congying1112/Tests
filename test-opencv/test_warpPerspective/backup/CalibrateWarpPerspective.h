//
// Created by Congying on 4/20/16.
//

#ifndef TEST_WARPPERSPECTIVE_CALIBRATEWARPPERSPECTIVE_H
#define TEST_WARPPERSPECTIVE_CALIBRATEWARPPERSPECTIVE_H

#include "Geometry.h"
using namespace GeoMath;

#include <vector>
using namespace std;

#include <opencv2/opencv.hpp>
using namespace cv;

Mat calibrateWarpPerspective(const Mat &mat, const std::vector<Point2f> &img_cali_pts, const std::vector<Point2f> &world_cali_pts);
Mat calibrateWarpPerspectiveByBird(const Mat &mat, const std::vector<Point2f> &img_cali_pts, const std::vector<Point2f> &bird_cali_pts);
void getCheckPtsInImage(const Size &img_size, const vector<VecPosition> &roi_contour);

#endif //TEST_WARPPERSPECTIVE_CALIBRATEWARPPERSPECTIVE_H
