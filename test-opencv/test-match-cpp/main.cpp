#include <opencv2/opencv.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <vector>
using namespace cv;
using namespace std;

int main(){
	auto img1 = imread("11.jpg");
	auto img2 = imread("22.jpg");

	auto descriptorExtractor = ORB::create();
	vector<KeyPoint> keypoints1, keypoints2;
	Mat descriptors1, descriptors2;
	descriptorExtractor->detect(img1, keypoints1);
	descriptorExtractor->detect(img2, keypoints2);
	descriptorExtractor->compute(img1, keypoints1, descriptors1);
	descriptorExtractor->compute(img2, keypoints2, descriptors2);

	// Mat img11, img22;
	// drawKeypoints(img1, keypoints1, img11, Scalar(255, 0, 0));
	// drawKeypoints(img2, keypoints2, img22, Scalar(255, 0, 0));
	// imshow("img1", img11);
	// imshow("img2", img22);
	// waitKey(-1);


	auto matcher = new BFMatcher();
	std::vector< DMatch > matches;
	matcher->match(descriptors1, descriptors2, matches);
	sort(matches.begin(), matches.end(), [](const DMatch &m1, const DMatch &m2){
		return m1.distance < m2.distance;
	});

	std::vector< DMatch > good_matches;
	for(int i = 0; i < 10 && i < matches.size(); i++) {
		good_matches.push_back(matches[i]);
	}
	Mat outImg;
	drawMatches	(img1, keypoints1, img2, keypoints2, good_matches, outImg, Scalar(255, 0, 0));	
	imshow("MATCH", outImg);
	waitKey(-1);

//	auto trans_matrix = findHomography(src_pts, dst_pts, RANSAC, 5.0);
}