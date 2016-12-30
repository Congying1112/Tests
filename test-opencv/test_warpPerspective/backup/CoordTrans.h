#ifndef _ELEC_COORDTRANS_0907_
#define _ELEC_COORDTRANS_0907_

#include "Geometry.h"
using namespace GeoMath;

class CoordTrans
{
public:
	static VecPosition GetPosWhenOrgMoved(VecPosition old , double xTrans , double yTrans , double angleTrans);

	static VecPosition GetKBGivenTwoPos(VecPosition pos1 , VecPosition pos2);

	static double GetYGivenXandKB(double x , VecPosition kb);
};

#endif