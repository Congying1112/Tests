#include "CoordTrans.h"

VecPosition CoordTrans::GetPosWhenOrgMoved(VecPosition old , double xTrans , double yTrans , double angleTrans)
{
	VecPosition result( old.getX() - xTrans , old.getY() - yTrans );
	return result.rotate( - angleTrans );
}

VecPosition CoordTrans::GetKBGivenTwoPos(VecPosition pos1 , VecPosition pos2)
{
	double k = (pos2.getY() - pos1.getY())/( pos2.getX() - pos1.getX() );
	double b = pos1.getY() - k * pos1.getX();

	VecPosition result(k,b);
	return result;
}

double CoordTrans::GetYGivenXandKB(double x , VecPosition kb)
{
	return kb.getX()*x + kb.getY();
}