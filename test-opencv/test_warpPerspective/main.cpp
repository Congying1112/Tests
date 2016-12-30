#include <iostream>
using namespace std;

#include <opencv2/opencv.hpp>
using namespace cv;

int main() {
    // img
    Mat cali_mat = imread("cali.JPG");
    //
    std::vector<Point2f> img_cali_pts;
    auto pickImgPt = [](int event, int x, int y, int, void* img_cali_pts_ptr){
        if( event == CV_EVENT_LBUTTONDOWN )
        {
            static_cast<std::vector<Point2f> *>(img_cali_pts_ptr)->push_back(Point2f(x,y));
            cout << static_cast<std::vector<Point2f> *>(img_cali_pts_ptr)->size() << endl;
            cout << x << ", " << y << endl;
        }
    };
    imshow("Select Image Point", cali_mat);
    setMouseCallback( "Select Image Point" , pickImgPt, &img_cali_pts);
    while(img_cali_pts.size() < 9)
    {
        imshow("Select Image Point" , cali_mat);
        waitKey(30);
    }
    destroyWindow("Select Image Point");
    // bird cali pts
    std::vector<Point2f> bird_cali_pts;
//    bird_cali_pts.push_back(Point2f(280,0));
//    bird_cali_pts.push_back(Point2f(640,0));
//    bird_cali_pts.push_back(Point2f(1000,0));
//    bird_cali_pts.push_back(Point2f(280, 360));
//    bird_cali_pts.push_back(Point2f(640, 360));
//    bird_cali_pts.push_back(Point2f(1000, 360));
//    bird_cali_pts.push_back(Point2f(280, 720));
//    bird_cali_pts.push_back(Point2f(640, 720));
//    bird_cali_pts.push_back(Point2f(1000, 720));
    int x0 = 200, x1 = 320, x2 = 500;
    int y0 = 0, y1 = 240, y2 = 480;
    bird_cali_pts.push_back(Point2f(x0, y0));
    bird_cali_pts.push_back(Point2f(x1, y0));
    bird_cali_pts.push_back(Point2f(x2, y0));
    bird_cali_pts.push_back(Point2f(x0, y1));
    bird_cali_pts.push_back(Point2f(x1, y1));
    bird_cali_pts.push_back(Point2f(x2, y1));
    bird_cali_pts.push_back(Point2f(x0, y2));
    bird_cali_pts.push_back(Point2f(x1, y2));
    bird_cali_pts.push_back(Point2f(x2, y2));


    //
    Mat warp_pers_H = findHomography( bird_cali_pts, img_cali_pts, CV_RANSAC );
    FileStorage fs("H.xml", FileStorage::WRITE);
    fs << "warp_pers_H" << warp_pers_H;
    fs.release();

    Mat output;
    warpPerspective( cali_mat , output , warp_pers_H , cali_mat.size(), CV_INTER_LINEAR|CV_WARP_INVERSE_MAP|CV_WARP_FILL_OUTLIERS);


    int roi_click_nnum = 0;
    auto pickRoi = [](int event, int x, int y, int, void* ){
        if( event == CV_EVENT_LBUTTONDOWN )
        {

        }
    };
    imshow("Select ROI", output);
    setMouseCallback( "Select ROI" , pickRoi );
    while(roi_click_nnum < 6)
    {
        imshow("Select ROI" , output);
        waitKey(30);
    }
    cvDestroyWindow("Select ROI");

    return 0;
}