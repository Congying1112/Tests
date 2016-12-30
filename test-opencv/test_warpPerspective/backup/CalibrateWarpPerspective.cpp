//
// Created by Congying on 4/20/16.
//
#include "CalibrateWarpPerspective.h"
#include "CoordTrans.h"
#include <fstream>

Mat calibrateWarpPerspective(const Mat &mat, const std::vector<Point2f> &img_cali_pts, const std::vector<Point2f> &world_cali_pts)
{
    assert(img_cali_pts.size() == 9 && world_cali_pts.size() == 9);

	float worldCoords[9][2];
    for(int i = 0 ; i < 9; i++) {
        worldCoords[i][0] = world_cali_pts[i].x;
        worldCoords[i][1] = world_cali_pts[i].y;
    }

	//寻找这9个点的x范围与y范围
	float xMinWorld,xMaxWorld,yMinWorld,yMaxWorld;
	xMinWorld = xMaxWorld = worldCoords[0][0];
	yMinWorld = yMaxWorld = worldCoords[0][1];
	for(int i=0 ; i<9 ;i++)
	{
		if( worldCoords[i][0] < xMinWorld )
			xMinWorld = worldCoords[i][0];

		if( worldCoords[i][0] > xMaxWorld )
			xMaxWorld = worldCoords[i][0];

		if( worldCoords[i][1] < yMinWorld )
			yMinWorld = worldCoords[i][1];

		if( worldCoords[i][1] > yMaxWorld )
			yMaxWorld = worldCoords[i][1];
	}

    //世界坐标到鸟瞰图坐标的变换：
    //Yb = k1 * Xw + b1
    //Xb = k2 * Yw + b2
    //以下计算参数(k1,b1)与(k2,b2)
	VecPosition pos1( xMinWorld , (float)mat.rows * 0.95 );
	VecPosition pos2( xMaxWorld , (float)mat.rows * 0.05 );
	VecPosition coef1 = CoordTrans::GetKBGivenTwoPos( pos1 , pos2 );

	VecPosition pos3( yMinWorld , (float)mat.cols * 0.95 );
	VecPosition pos4( yMaxWorld , (float)mat.cols * 0.05 );
	VecPosition coef2 = CoordTrans::GetKBGivenTwoPos( pos3 , pos4 );

    // 鸟瞰图到世界坐标的变换：
    // Yw = k3 * Xb + b3
    // Xw = k4 * Yb + b4
    // 以下计算参数(k3,b3) and (k4,b4)
    VecPosition b2w_coef1(1.0/coef2.getX() , -1.0 * coef2.getY() / coef2.getX() );
    VecPosition b2w_coef2(1.0/coef1.getX() , -1.0 * coef1.getY() / coef1.getX() );


	ofstream ofs("bird2world.txt");
	ofs<< b2w_coef1.getX()<<" "<< b2w_coef1.getY()<<endl;
	ofs<< b2w_coef2.getX()<<" "<< b2w_coef2.getY()<<endl;
	ofs.close();

    //计算9个世界坐标的鸟瞰图坐标，因为计算单应矩阵需要鸟瞰图坐标和图像坐标
    std::vector<Point2f> bird_cali_pts;
    for( int posNum = 0 ; posNum < 9 ;posNum ++) //用9个点来标定
    {
        bird_cali_pts.push_back(Point2f(CoordTrans::GetYGivenXandKB(worldCoords[posNum][1] , coef2 ), CoordTrans::GetYGivenXandKB(worldCoords[posNum][0] , coef1 )));
    }

    return findHomography( bird_cali_pts, img_cali_pts, CV_RANSAC );
}


void getCheckPtsInImage(const Size &img_size, const vector<VecPosition> &roi_contour) {

    for( int i = 0 ; i< img_size.height; i++ )
    {
        for( int j = 0 ; j < img_size.width ; j++ )
        {
            CvPoint posTmp;
            posTmp.x = j;
            posTmp.y = i;
//            m_roiResult[i][j] = CheckPointInROI(posTmp);
        }
    }
}