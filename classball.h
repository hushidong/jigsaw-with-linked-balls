#include<stdio.h>
#include<vector>
#include<math.h>
#include<time.h>
#include<stdlib.h>
#include<iostream>
#include<fstream>
#include<iomanip>

#ifndef CLASSBALL_H
#define CLASSBALL_H

/**球的拓扑类
主要是设置球二维拓扑中左右上下的邻居信息
存在邻居则设置为邻居的编号
否则设置为负
*/
class balltopo
{
private:
    int sn_self;//< topo[0]  //是真实序号，从1开始计数
    int sn_left;//< topo[1]  //存在邻居则设置邻居序号，不存在则设置为-1
    int sn_right;
    int sn_above;
    int sn_below;
	int occupied; //用于判断网格中的球的位置是否已经占用,1表示占用,0表示不占用
	int shaped;//用于表示已经划分到形状中

public:
    /**根据设置球二维拓扑中左右上下的邻居信息
    */
    void settopo(int topo[5])
    {
        sn_self=topo[0];
        sn_left=topo[1];
        sn_right=topo[2];
        sn_above=topo[3];
        sn_below=topo[4];
    }
	
	void setoccp(int occp)
    {
		occupied=occp;
    }
	
	void setshpd(int shpd)
    {
		shaped=shpd;
    }
	
	int getoccp()
    {
		return occupied;
    }
	
	int getshpd()
    {
		return shaped;
    }

    /**得到当前球的编号/序号
    */
    int getsn()
    {
        return sn_self;
    }

    /**得到当前球在二维拓扑中左右上下的邻居信息
    */
    void gettopo(int topo[5])
    {
        topo[0]=sn_self;
        topo[1]=sn_left;
        topo[2]=sn_right;
        topo[3]=sn_above;
        topo[4]=sn_below;
    }
	
	int getright()
    {
        return sn_right;
    }

	int getleft()
    {
        return sn_left;
    }
	
	int getabove()
    {
        return sn_above;
    }
	int getbelow()
    {
        return sn_below;
    }
	
};



#endif //
