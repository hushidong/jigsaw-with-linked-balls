#include<stdio.h>
#include<vector>
#include<math.h>
#include<time.h>
#include<stdlib.h>
#include"datatype.h"
#include"classball.h"
#include"classshape.h"
#include<iostream>
#include<fstream>
#include<iomanip>

#ifndef CLASSGRID_H
#define CLASSGRID_H


/*
球构成的下三角矩阵
*/
class grid
{
private:
    int n_scale;//网格的大小，行列数均为n_scale
	int n_balls_ofshape;//链接形状中的球数
	int n_ofshapes;//划分成的形状数
    int n_total;
	int n_focus;//<当前网格中的焦点,用于在其位置及邻居位置判断占用情况,从1开始计数，为实际球序号
    std::vector<balltopo> vecgrid;//球列表
	std::vector<linkshape> veclinkshape;//形状列表
	std::vector<linkshape> veclinkshapesaved;//用于保存原始的形状列表，因为形状的各种操作会改变veclinkshape的数据
	int flagouthints=0;//=0时，输出一些提示，=1时，输出。

public:

grid(int n,int m)//构造函数
    {
        n_scale=n;
		n_balls_ofshape=m;
        balltopo trigrid[n_scale][n_scale];
		//下三角网格，只是一个下三角矩阵即可
		int nij=0;
		printf("construct:\n");
        for (int i=0;i<n_scale;i++){//存储结构是先行后列.
            for(int j=0;j<=i;j++){
                vecgrid.push_back(trigrid[i][j]);
				nij++;
				printf("%d ",nij);
			}
        }
		printf("\n");
		trigridinit();
    }
	
	//利用形状中的球数和特征值列表判断形状是否相同
	//0表示不同，1表示相同
int checksameshape(linkshape a,linkshape b)
	{
		if(a.getshapenballs() != b.getshapenballs()) {
			return 0;
		}else
		{
			for(int i=0;i<a.getshapenballs();i++)
			{
				if(fabs(a.getshapeeigen(i)-b.getshapeeigen(i))>0.000001) return 0;
			}
		}
		
		//printf("eigen is the same!\n");
		
		int flagsame=0;
		//printf("ball a rows=%d , cols=%d\n",a.getrows(),a.getcols());
		//printf("ball b rows=%d , cols=%d\n",b.getrows(),b.getcols());
		if(a.getrows() != a.getcols()) {//行列不相等时，只要做翻转就可以比较了
			if(a.getrows()==b.getrows() && a.getcols()==b.getcols() )//当行数列数完全相同
			{
				int sumrowsa=0;
				int sumcolsa=0;
				int sumrowsb=0;
				int sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)//正常比较坐标位置行和列加和后的总数
				{
					sumrowsa=sumrowsa+a.getptrow(i);
					sumcolsa=sumcolsa+a.getptcol(i);
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//printf("ball a pos sum of rows=%d , of cols=%d\n",sumrowsa,sumcolsa);
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb) flagsame=1; 
				
				b.mirror_lr();//左右翻转一下
				sumrowsb=0;
				sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)
				{
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb)  flagsame=1;
				
				b.mirror_ab();//接着上下翻转一下
				sumrowsb=0;
				sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)
				{
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if (sumrowsa==sumrowsb && sumcolsa==sumcolsb) flagsame=1;
				
				b.mirror_lr();//接着再左右翻转一下，4中情况都覆盖到了
				sumrowsb=0;
				sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)
				{
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb)  flagsame=1;
			}
			else if(a.getrows()==b.getcols() && a.getcols()==b.getrows() )//当a行数=b列数，a列数=b行数
			{
				b.rotate_right();//转过来使得行，列数相同
				int sumrowsa=0;
				int sumcolsa=0;
				int sumrowsb=0;
				int sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)//正常比较坐标位置行和列加和后的总数
				{
					sumrowsa=sumrowsa+a.getptrow(i);
					sumcolsa=sumcolsa+a.getptcol(i);
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//printf("ball a pos sum of rows=%d , of cols=%d\n",sumrowsa,sumcolsa);
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb) flagsame=1; 
				
				b.mirror_lr();//左右翻转一下
				sumrowsb=0;
				sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)
				{
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb)  flagsame=1;
				
				b.mirror_ab();//接着上下翻转一下
				sumrowsb=0;
				sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)
				{
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if (sumrowsa==sumrowsb && sumcolsa==sumcolsb) flagsame=1;
				
				b.mirror_lr();//接着再左右翻转一下，4中情况都覆盖到了
				sumrowsb=0;
				sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)
				{
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb)  flagsame=1;
			}
			else
			{
				return 0;
			}
		}
		else//行列相等时，需要做旋转和翻转
		{
			if(b.getrows() != b.getcols()) 
			{
				return 0;
			}else
			{
				int sumrowsa=0;
				int sumcolsa=0;
				int sumrowsb=0;
				int sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)//正常比较坐标位置行和列加和后的总数
				{
					sumrowsa=sumrowsa+a.getptrow(i);
					sumcolsa=sumcolsa+a.getptcol(i);
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//a.pos_show();
				//b.pos_show();
				//printf("ball a pos sum of rows=%d , of cols=%d\n",sumrowsa,sumcolsa);
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb) flagsame=1; 
				
				b.rotate_right();//顺时针旋转90度
				sumrowsb=0;
				sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)
				{
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//b.pos_show();
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb)  flagsame=1;
				
				b.rotate_right();//顺时针旋转180度
				sumrowsb=0;
				sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)
				{
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//b.pos_show();
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb)  flagsame=1;
				
				b.rotate_right();//顺时针旋转270度
				sumrowsb=0;
				sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)
				{
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//b.pos_show();
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb)  flagsame=1;
				
				b.rotate_right();//顺时针旋转360度，还原
				b.mirror_ab();//接着上下翻转一下
				sumrowsb=0;
				sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)
				{
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//b.pos_show();
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb)  flagsame=1;
				
				b.rotate_right();//接着再顺时针旋转90度
				sumrowsb=0;
				sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)
				{
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//b.pos_show();
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb)  flagsame=1;
				
				b.rotate_right();//接着再顺时针旋转180度
				sumrowsb=0;
				sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)
				{
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//b.pos_show();
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb)  flagsame=1;
				
				b.rotate_right();//接着再顺时针旋转270度
				sumrowsb=0;
				sumcolsb=0;
				for(int i=0;i<a.getshapenballs();i++)
				{
					sumrowsb=sumrowsb+b.getptrow(i);
					sumcolsb=sumcolsb+b.getptcol(i);
				}
				//b.pos_show();
				//printf("ball b pos sum of rows=%d , of cols=%d\n",sumrowsb,sumcolsb);
				if(sumrowsa==sumrowsb && sumcolsa==sumcolsb)  flagsame=1;
				
			}
			
		}
		
		if(flagsame==0) return 0;
		return 1;
	}


void outputshapes()//将网格和形状信息输出到文件中，内容是json格式的。
{
    //网格构成的列表:
    std::ofstream outfile;
	outfile.open("datatopython.dat");
    
	outfile<<"[";
    outfile<<"[";
	for(int i=0;i<n_scale;++i)
	{
        outfile<<"[";
        for(int j=0;j<n_scale-1;++j)
        {
            if (j<=i){
                outfile<<1<<",";
            }
            else{
                outfile<<0<<",";
            }
        }
        int j=n_scale-1;
        if(j==i){
            outfile<<1;
        }else{
            outfile<<0;
        }
        if(i==n_scale-1) {
            outfile<<"]";
        }else{
            outfile<<"],";
        }
	}
    outfile<<"],";
    outfile<<std::endl;
    
    for(int k=0;k<n_ofshapes;k++)
    {   
        int nballs=veclinkshape[k].getshapenballs();
        int rows=veclinkshape[k].getrows()+1;
        int cols=veclinkshape[k].getcols()+1;
        printf("idx_ball=%d\n",k);
        printf("num_ball=%d\n\n",nballs);
        outfile<<"[";
        for (int i=0;i<rows;i++){
            outfile<<"[";
            for(int j=0;j<cols;j++)
            {
                int flag=0;
                for(int m=0;m<nballs;m++)
                {
                    int row=veclinkshape[k].getptrow(m);
                    int col=veclinkshape[k].getptcol(m);
                    //printf("row=%d,col=%d\n",row,col);
                    if(i==row and j==col){
                        flag=1;
                        break;
                    }
                }
                if(j==cols-1){
                    outfile<<flag;
                }else{
                    outfile<<flag<<",";
                }
            }
            if(i==rows-1){
                outfile<<"]";
            }else
            {
                outfile<<"],";
            }
        }
        if(k==n_ofshapes-1){
            outfile<<"]";
        }else
        {        
            outfile<<"],";
            outfile<<std::endl;
        }
    }
    
    
    outfile<<"]";
	outfile.close();
}    
    
void veclinksave()//保存原始形状列表
{
	veclinkshapesaved=veclinkshape;
}

void veclinkrestore()//恢复原始形状列表
{
	veclinkshape=veclinkshapesaved;
}
	

void Partition()//将球划分到形状中
{
	int i,j,k;
	int sn_now,sn_ball,posrow_now,poscol_now;
	linkshape shapevec[n_total];
	linkshape shapevecrec[n_total];
	float randtemp;
	srand(time(NULL));
	int shapenumber,shapenumberrec;
	int flagnoleft;//网格中存在球未划分的标记=0，表示还需要划分，>0否则不需要划分
	int flaginshape;//用于表示当前球是在形状中的标记
	int flagsameshape;
	
	
	shapenumberrec=n_total;
	int ndopart;
	for(ndopart=0;ndopart<1000;ndopart++){
		//printf("-----------------------------------------\n");
		//printf("times of partitions:%d\n",ndopart);
		
		for(i=0;i<n_total;i++)//清除划分状态，便于再次划分
		{
			vecgrid[i].setshpd(0);
		}
		
		shapenumber=0;
		flagnoleft=0;
		int ndoshapes=0;//用于避免无法划分出不同形状完全覆盖网格时的死循环
		
		while (flagnoleft==0 && ndoshapes<200)
		{
			ndoshapes++;
			//printf("times of create different shape to cover all the grid :%d\n",ndoshapes);
			coord ptpos[n_balls_ofshape]={0};
			int ptnum[n_balls_ofshape]={0};
			
			
			//确定起点
			// k=0;
			// i=0;
			// while(i<n_total)
			// {
				// if(vecgrid[i].getshpd()==0){
					// sn_now=i;
					// posrow_now=0;
					// poscol_now=0;
					// vecgrid[sn_now].setshpd(1);
					// ptnum[k]=sn_now;
					// ptpos[k].row=posrow_now;
					// ptpos[k].col=poscol_now;
					// //printf("i=%d",i);
					// i=n_total;
				// } else {
					// i++;
					// //printf("i=%d",i);
					// if(i >= n_total) flagnoleft=1;
					// //printf("flagnoleft=%d",flagnoleft);
				// }
			// }
			
			//确定起点机制换一种
			k=0;
			do 
			{
				flagnoleft=1;//首先确定是否存在没有连接的球
				for(i=0;i<n_total;i++)
				{
					if(vecgrid[i].getshpd()==0) flagnoleft=0;
				}
				sn_now=rand()%n_total;
			}
			while(vecgrid[sn_now].getshpd()==1 && flagnoleft==0);
			if(vecgrid[sn_now].getshpd()==0 && flagnoleft==0)
			{
				vecgrid[sn_now].setshpd(1);
				coord coorda=getrowcolformsn(sn_now+1);
                posrow_now=coorda.row;
                poscol_now=coorda.col;
				ptnum[k]=sn_now;
				ptpos[k].row=posrow_now;
				ptpos[k].col=poscol_now;
			}
			//if(flagnoleft==1) break;
			
			
			if(flagnoleft==0) {
			
				// printf("\ninitial ball numbers:");
				// for(j=0;j<=k;j++)
				// {
					// printf("%d ",ptnum[j]+1);//球真实序号比矢量中的序号大1
				// }
				// printf("\ninitial ball postions:");
				// for(j=0;j<=k;j++)
				// {
					// printf("(%d,%d) ",ptpos[j].row,ptpos[j].col);
				// }
				// printf("\n");
				
				
				int nstep=0;
				float isfourorfive=(rand()%10/10.0);
				int nballsrand;//当球数固定的时候，以及无法划分了。所以取两个值来调整
				// if(isfourorfive < 0.6) {
					// nballsrand=n_balls_ofshape;}
				// else if(isfourorfive < 0.9) {
					// nballsrand=n_balls_ofshape-1;
				// }
				// else{
					// nballsrand=n_balls_ofshape-2;
					// }
				if(isfourorfive < 1) {//0.5-0.9
					nballsrand=n_balls_ofshape;}
				else{
					nballsrand=n_balls_ofshape-1;
					}
				//
				while(k<nballsrand-1 && nstep < 100){//当球数未达到要求，走动次数小于100次时做
					nstep++;
					randtemp=(rand()%100/100.0);
					//printf("steps of moving try to create a shape:%d. ",nstep);
					//printf("nstep=%d\n",nstep);
					//printf("randt=%f\n",randtemp);
					
					if(randtemp < 0.25)//右移
					{
						//printf("sn_now=%d\n",sn_now);
						//printf("right of sn_now=%d\n",vecgrid[sn_now].getright()-1);
						sn_ball=vecgrid[sn_now].getright();
						if(sn_ball>0) {
							if(vecgrid[sn_ball-1].getshpd() == 0){
								sn_now=sn_ball-1;//矢量中的序号比球真实序号小1
								poscol_now++;
								k++;
								ptnum[k]=sn_now;
								ptpos[k].row=posrow_now;
								ptpos[k].col=poscol_now;
								vecgrid[sn_now].setshpd(1);
							}else{//处理往回走的情况，但不能走到其它形状中
								flaginshape=0;
								for(j=0;j<=k;j++)
								{
									if(sn_ball-1==ptnum[j]) flaginshape=1;
								}
								if(flaginshape==1) {//当移动到的球在形状内则确定移动
									sn_now=sn_ball-1;
									poscol_now++;
								}
							}
						}
					}
					else if(randtemp < 0.5)//左移
					{
						//printf("sn_now=%d\n",sn_now);
						//printf("left of sn_now=%d\n",vecgrid[sn_now].getleft()-1);
						sn_ball=vecgrid[sn_now].getleft();
						if(sn_ball>0) {
							if(vecgrid[sn_ball-1].getshpd() == 0){
								sn_now=sn_ball-1;//矢量中的序号比球真实序号小1
								poscol_now--;
								k++;
								ptnum[k]=sn_now;
								ptpos[k].row=posrow_now;
								ptpos[k].col=poscol_now;
								vecgrid[sn_now].setshpd(1);
							}else{//处理往回走的情况，但不能走到其它形状中
								flaginshape=0;
								for(j=0;j<=k;j++)
								{
									if(sn_ball-1==ptnum[j]) flaginshape=1;
								}
								if(flaginshape==1) {
									sn_now=sn_ball-1;
									poscol_now--;
								}
							}
						}
					}
					else if(randtemp < 0.75)//上移
					{
						//printf("sn_now=%d\n",sn_now);
						//printf("above of sn_now=%d\n",vecgrid[sn_now].getabove()-1);
						sn_ball=vecgrid[sn_now].getabove();
						if(sn_ball>0) {
							if(vecgrid[sn_ball-1].getshpd() == 0){
								sn_now=sn_ball-1;//矢量中的序号比球真实序号小1
								posrow_now--;
								k++;
								ptnum[k]=sn_now;
								ptpos[k].row=posrow_now;
								ptpos[k].col=poscol_now;
								vecgrid[sn_now].setshpd(1);
							}else{//处理往回走的情况，但不能走到其它形状中
								flaginshape=0;
								for(j=0;j<=k;j++)
								{
									if(sn_ball-1==ptnum[j]) flaginshape=1;
								}
								if(flaginshape==1) {
									sn_now=sn_ball-1;
									posrow_now--;
								}
							}
						}
					}
					else//下移
					{
						//printf("sn_now=%d\n",sn_now);
						//printf("below of sn_now=%d\n",vecgrid[sn_now].getbelow()-1);
						sn_ball=vecgrid[sn_now].getbelow();
						if(sn_ball>0) {
							if(vecgrid[sn_ball-1].getshpd() == 0){
								sn_now=sn_ball-1;//矢量中的序号比球真实序号小1
								posrow_now++;
								k++;
								ptnum[k]=sn_now;
								ptpos[k].row=posrow_now;
								ptpos[k].col=poscol_now;
								vecgrid[sn_now].setshpd(1);
							}else{//处理往回走的情况，但不能走到其它形状中
								flaginshape=0;
								for(j=0;j<=k;j++)
								{
									if(sn_ball-1==ptnum[j]) flaginshape=1;
								}
								if(flaginshape==1) {
									sn_now=sn_ball-1;
									posrow_now++;
								}
							}
						}
					}
					//printf("sn_now=%d, real_sn_of_ball=%d\n",sn_now,sn_now+1);
					// int tempa;
					// std::cin>>tempa;
				}
				
				
				//显示一下当前的形状的球序号和相对坐标
				// trigriddisplay();
				// trigridshapedshow();
				// printf("\n");
				// printf("ball numbers:");
				// for(j=0;j<=k;j++)
				// {
					// printf("%d ",ptnum[j]+1);
				// }
				// printf("\n");
				// printf("ball postions:");
				// for(j=0;j<=k;j++)
				// {
					// printf("(%d,%d) ",ptpos[j].row,ptpos[j].col);
				// }
				// printf("\n");
				// printf("number of balls in this shape:%d\n",k+1);//从0开始的当前形状中的球数+1。
				//int tempa;
				//std::cin>>tempa;
				
				
				//将当前形状放到形状数组中
				coord vectmp[k+1];
				int vecnumber[k+1];
				for(j=0;j<=k;j++)
				{
					vectmp[j].row=ptpos[j].row;
					vectmp[j].col=ptpos[j].col;
					vecnumber[j]=ptnum[j]+1;//输出真实的球序号，而不是从0开始的序号。
				}
				linkshape shapea=linkshape(shapenumber+1,k+1,vectmp,vecnumber);
				//先判断形状是否与原先构成的相同
				if(shapenumber==0) {
					shapevec[shapenumber]=shapea;
					shapenumber++;
				}else{
					flagsameshape=0;
					for(j=0;j<shapenumber;j++)
					{
						if(checksameshape(shapea,shapevec[j]))
						{
							flagsameshape=1;
							//printf("flagsameshape=%d\n",flagsameshape);
						}
					}
					if(flagsameshape==0){//和之前的形状不相同
						shapevec[shapenumber]=shapea;
						shapenumber++;
					}else{
						for(j=0;j<=k;j++)
						{
							vecgrid[ptnum[j]].setshpd(0);
						}
					}
				}
				//int tempa;
				//std::cin>>tempa;
			}
		}
		
		//输出当前次，划分的形状
		// printf("\n");
		// printf("do the %d th time's partition\n",ndopart);
		// printf("number of shapes in grid is %d\n",shapenumber);
		// for(j=0;j<shapenumber;j++)
		// {
			// printf("j=%d ,shape sn: %d\n",j,shapevec[j].getshapesn());
			// printf("j=%d ,total number of balls in shape: %d\n",j,shapevec[j].getshapenballs());
			// printf("j=%d ,serial number of balls in shape:",j);
			// for(i=0;i<shapevec[j].getshapenballs();i++){
			// printf("%d ",shapevec[j].getballnumber(i));}
			// printf("\n");
		// }
		// trigridshapedshow();
		// if(flagnoleft==0) {
			// printf("partition is not completed,grid is not covered\n");
		// }
		
		
		//用形状数来判断是否是最佳划分，形状数最小的肯定是最佳的，
		//并记录到shapevecrec数组中
		//当网格未完全覆盖,则不做记录
		if(shapenumber<shapenumberrec and flagnoleft==1) {
			for(j=0;j<shapenumber;j++)
			{
				shapevecrec[j]=shapevec[j];
			}
			shapenumberrec=shapenumber;
			//break;//加这句不做最优选择，划分出一个结果即结束
		}
		
		// if(flagnoleft==1) {
		// int tempa;
		// std::cin>>tempa;
		// }
	}
	
		//输出并记录最佳划分，划分的形状
		if(shapenumberrec<n_total){//如果没有划分则不做输出
		printf("\n");
		trigriddisplay();
		printf("\n");
		printf("best partition for %d times' attempt:\n",ndopart);
		printf("total number of shapes in grid is %d\n",shapenumberrec);
		for(j=0;j<shapenumberrec;j++)
		{
			printf("Shape No.=%d ,shape sn: %d\n",j,shapevecrec[j].getshapesn());
			printf("shape No.=%d ,total number of balls in shape: %d\n",j,shapevecrec[j].getshapenballs());
            printf("shape No.=%d ,balls positions of the shape in grid:",j);
			for(i=0;i<shapevecrec[j].getshapenballs();i++){
			printf("{%d,%d},",shapevecrec[j].getptrow(i)+shapevecrec[j].getrowofzero(),shapevecrec[j].getptcol(i)+shapevecrec[j].getcolofzero());
			}
            printf("\n");
			printf("shape No.=%d ,(row,col) of balls in shape:",j);
			for(i=0;i<shapevecrec[j].getshapenballs();i++){
			printf("(%d,%d),",shapevecrec[j].getptrow(i),shapevecrec[j].getptcol(i));
			}
			printf("\n");
			printf("shape No.=%d ,serial number of balls in shape:",j);
			for(i=0;i<shapevecrec[j].getshapenballs();i++){
			printf("%d ",shapevecrec[j].getballnumber(i));}
			printf("\n\n");
			//把链接形状放到veclinkshape形状中
			veclinkshape.push_back(shapevecrec[j]);
		}
		n_ofshapes=shapenumberrec;
		}
}  


int canbesetdown(int n_balls,int sn_focus_inshape, coord ballscoords[])//根据焦点球序号以及形状中焦点和坐标确定形状能否放入网格中
//n_balls形状中球数，sn_focus_inshape为形状中焦点球序号从1开始计数，ballscoords形状中各点行列坐标
{
	int row=ballscoords[sn_focus_inshape-1].row;
	int col=ballscoords[sn_focus_inshape-1].col;
	int flagcanbe=1;
	for(int i=0;i<n_balls;i++)
	{
		int drow=ballscoords[i].row -row;
		int dcol=ballscoords[i].col -col;
		int sn_ball=getnumdrowdcola(drow,dcol);
		if(sn_ball<0 || vecgrid[sn_ball-1].getoccp()==1){//当球不在范围内或者球所在框已被占据则无法放入
			flagcanbe=0;
		}
	}
	return flagcanbe;
}



int merge()//将形状合成三角网格(起点按顺序选择)
{
	int matrixgrid[n_scale*2][n_scale*2]={0};//用于标记当前行列位置的是否已占据
	for(int i=0;i<n_scale*2;++i)
	{
		for(int j=0;j<n_scale*2;++j){
			matrixgrid[i][j]=0;
		}
	}
	int flagok=0;//拼图成功
	int flagmergeok=0;//标记当前各形状拼图完成
	int flagshapeused[n_ofshapes]={0};//标记各形状是否已经使用过
	
	int tempa;//临时
	//srand(time(NULL));
	srand(time(0));
	
	int colball=0;//起点位置
	int rowball=0;
	int mgtimes=0;//拼图的次数
	while(flagok==0 && mgtimes<100000000)//设置拼图尝试次数，避免无限循环
	{
		if(flagouthints==1){
			std::cout<<"------------------"<<std::endl;
			std::cout<<"start "<<mgtimes<<std::endl;
			//显示一下拼图占用情况
			// for(int i=0;i<n_scale;++i)
			// {
				// for(int j=0;j<=i;++j)
				// {
					// printf("%5d",matrixgrid[i][j]);
				// }
				// printf("\n");
			// }
		}
		
		++mgtimes;
		int nstimes=0;//尝试加入新形状的次数
		while(flagmergeok==0 && nstimes< n_ofshapes*2)//当尝试加入新形状的次数次数多于一定次数，说明当前拼图无法完成，则退出循环，进入下一次拼图
		{
			++nstimes;
			
			
			//确定起点
			for(int col=0;col<n_scale;++col)//从第1列开始找没有填充的位置
			{
				int flagfound=0;
				for(int row=col;row<n_scale;++row)//从当前列第一行开始找没有填充的位置
				{
					if(matrixgrid[row][col]==0){
						colball=col;//形状的中最小栏，最小行的球的所要放的位置
						rowball=row;//
						flagfound=1;
						if(flagouthints==1) std::cout<<"row="<<rowball<<" col="<<colball<<" is selected"<<" occp="<<matrixgrid[row][col]<<std::endl;
						break;
					}
				}
				if(flagfound==1) break;
			}
			
			
			//另一种确定起点机制，随机选取
			// int flagfound=0;
			// while(flagfound==0)
			// {
				// int row=rand()%n_scale;
				// int col=rand()%n_scale;
				// //std::cout<<"row="<<row<<" col="<<col<<" used:"<<matrixgrid[row][col]<<std::endl;
				// if(matrixgrid[row][col]==0 && col<=row)
				// {
					// colball=col;
					// rowball=row;//
					// flagfound=1;
					// std::cout<<"row="<<rowball<<" col="<<colball<<" is selected"<<" occp="<<matrixgrid[row][col]<<std::endl;
					// break;
				// }
			// }
			//std::cout<<"rowball="<<rowball<<" colball="<<colball<<std::endl;
			//std::cout<<"press any int to continue:";
			//std::cin>>tempa;
			
			
			//随机选择形状:
			
			int sn_now=rand()%n_ofshapes;//随机选择一个形状，序号以0开始
			while(flagshapeused[sn_now]!=0){
				sn_now=rand()%n_ofshapes;
			}
			
			//std::cout<<"shape sn="<<sn_now<<std::endl;
			//veclinkshape[sn_now].pos_show();
			//std::cout<<"press any int to continue:";
			//std::cin>>tempa;
			
			
			//在拼图中加入形状
			int flagcanbeset=0;//标记是否可以加入拼图，0表示不能
			int n_balls=veclinkshape[sn_now].getshapenballs();
			int settimes=0;//变换次数，用于错误处理
			while(flagcanbeset==0 && settimes<20)//变换次数多于一定次数仍然不能加入，说明该形状无法加入，则退出循环
			{
				settimes++;
				
				//尝试当前形状变换状态下设置不同的焦点球能否放入
				int sn_focus;//遍历选择焦点球
				int rowfocus;
				int colfocus;
				int flagballused[n_balls];
				for(int i=0;i<n_balls;++i)
				{
					flagballused[i]=0;
				}
				while(true)
				{
					flagcanbeset=1;
					sn_focus=rand()%n_balls;//随机选择焦点球
					while(flagballused[sn_focus]!=0){
						sn_focus=rand()%n_balls;
					}
					flagballused[sn_focus]=1;
					rowfocus=veclinkshape[sn_now].getptrow(sn_focus);
					colfocus=veclinkshape[sn_now].getptcol(sn_focus);
									
					for(int i=0;i<n_balls;++i)//判断一下当前形状能否加入拼图
					{
						int drow=veclinkshape[sn_now].getptrow(i)-rowfocus;
						int dcol=veclinkshape[sn_now].getptcol(i)-colfocus;
						int row=rowball+drow;//焦点球放到当前起点位置上
						int col=colball+dcol;
						if(col<0 || row<0 || col>row || row>=n_scale){//增加一个约束
							flagcanbeset=0;
							break;
						}
						if(matrixgrid[row][col]>0){
							flagcanbeset=0;
							break;
						}
					}
					if(flagcanbeset==1) break;
					int flagballallused=0;
					for(int i=0;i<n_balls;++i)
					{
						flagballallused+=flagballused[i];
					}
					if(flagballallused>=n_balls) break;
				}
				
				//当上述变换焦点球仍不能加入时，做形状变换
				if(flagcanbeset==0)
				{
					int transid=rand()%4+1;
					switch(transid)
					{
						case 1:
							veclinkshape[sn_now].rotate_right();
							break;
						case 2:
							veclinkshape[sn_now].rotate_left();
							break;
						case 3:
							veclinkshape[sn_now].mirror_ab();
							break;
						case 4:
							veclinkshape[sn_now].mirror_lr();
							break;
						default:
							break;
					}
				}else{
					for(int i=0;i<n_balls;++i)
					{
						int drow=veclinkshape[sn_now].getptrow(i)-rowfocus;
						int dcol=veclinkshape[sn_now].getptcol(i)-colfocus;
						int row=rowball+drow;//焦点球放到当前起点位置上
						int col=colball+dcol;
						matrixgrid[row][col]=sn_now+1;//用形状的序号表示占用
						//std::cout<<"row="<<row<<" col="<<col<<" is seted"<<std::endl;
					}
					//veclinkshape[sn_now].pos_show();
					//std::cout<<"press any int to continue:";
					//std::cin>>tempa;
					if(flagouthints==1) std::cout<<"shape id="<<sn_now+1<<" is used!"<<std::endl;
					flagshapeused[sn_now]=1;
				}
			}
			
			//显示一下拼图占用情况
			// for(int i=0;i<n_scale;++i)
			// {
				// for(int j=0;j<=i;++j)
				// {
					// printf("%5d",matrixgrid[i][j]);
				// }
				// printf("\n");
			// }
			
			
			//判断一下是否所有形状都加入拼图中
			int flagallused=0;
			for(int i=0;i<n_ofshapes;++i)
			{
				flagallused+=flagshapeused[i];
			}
			if(flagallused==n_ofshapes){
				flagmergeok=1;
			}

		}
		//std::cout<<"added all shapes:"<<flagmergeok<<std::endl;
		//std::cout<<"press any int to continue:";
		//std::cin>>tempa;
		
		
		//一次拼图后，所有形状的使用状态重设:
		for(int i=0;i<n_ofshapes;++i)
		{
			flagshapeused[i]=0;
		}
		
				
		//判断拼图是否成功
		flagok=1;
		for(int i=0;i<n_scale;++i)
		{
			for(int j=0;j<=i;++j){
				if(matrixgrid[i][j]==0){
					flagok=0;
					break;
				}
			}
			if(flagok==0) break;
		}
		if(flagok==0)//本次拼图未成功，则重新开始拼图，重设占用
		{
			flagmergeok=0;//重新拼图标志:
			for(int i=0;i<n_scale*2;++i)
			{
				for(int j=0;j<n_scale*2;++j){
					matrixgrid[i][j]=0;
				}
			}
		}else
		{
			//显示一下拼图占用情况
			std::ofstream outfile;
			outfile.open("sn-grid.dat",std::ios_base::out|std::ios_base::app);
			outfile<<"------------"<<std::endl;
			outfile<<"times="<<mgtimes<<std::endl;
			for(int i=0;i<n_scale;++i)
			{
				for(int j=0;j<=i;++j)
				{
					printf("%5d",matrixgrid[i][j]);
					outfile<<std::setw(5)<<matrixgrid[i][j];
				}
				printf("\n");
				outfile<<std::endl;
			}
			outfile.close();
		}
		std::cout<<"time="<<mgtimes<<" is seccessful:"<<flagok<<std::endl;
		//std::cout<<"press any int to continue:"<<std::endl;
		//std::cin>>tempa;
	}
	
	return mgtimes;
}




int mergec()//将形状合成三角网格(起点按顺序选择，测试不同约束的形状填充)
{
	int matrixgridpre[n_scale*2][n_scale*2]={0};//把matrixgrid周围的内存空出来
	int matrixgrid[n_scale*2][n_scale*2]={0};//用于标记当前行列位置的是否已占据
	int matrixgridpos[n_scale*2][n_scale*2]={0};//把matrixgrid周围的内存空出来
	int flagok=0;//拼图成功
	int flagmergeok=0;//标记当前各形状拼图完成
	int flagshapeused[n_ofshapes]={0};//标记各形状是否已经使用过
	
	int tempa=0;//临时
	//srand(time(NULL));
	srand(time(0));
	
	int colball=0;//起点位置
	int rowball=0;
	int mgtimes=0;//拼图的次数
	while(flagok==0 && mgtimes<100000000)//设置拼图尝试次数，避免无限循环
	{
		if(flagouthints==1){
			std::cout<<"------------------"<<std::endl;
			std::cout<<"start "<<mgtimes<<std::endl;
			//显示一下拼图占用情况
			// for(int i=0;i<n_scale;++i)
			// {
				// for(int j=0;j<=i;++j)
				// {
					// printf("%5d",matrixgrid[i][j]);
				// }
				// printf("\n");
			// }
		}
		
		++mgtimes;
		int nstimes=0;//尝试加入新形状的次数
		while(flagmergeok==0 && nstimes< n_ofshapes*2)//当尝试加入新形状的次数次数多于一定次数，说明当前拼图无法完成，则退出循环，进入下一次拼图
		{
			++nstimes;
			
			
			//确定起点
			for(int col=0;col<n_scale;++col)//从第1列开始找没有填充的位置
			{
				int flagfound=0;
				for(int row=col;row<n_scale;++row)//从当前列第一行开始找没有填充的位置
				{
					if(matrixgrid[row][col]==0){
						colball=col;//形状的中最小栏，最小行的球的所要放的位置
						rowball=row;//
						flagfound=1;
						if(flagouthints==1) std::cout<<"row="<<rowball<<" col="<<colball<<" is selected"<<" occp="<<matrixgrid[row][col]<<std::endl;
						break;
					}
				}
				if(flagfound==1) break;
			}
			
			
			//另一种确定起点机制，随机选取
			// int flagfound=0;
			// while(flagfound==0)
			// {
				// int row=rand()%n_scale;
				// int col=rand()%n_scale;
				// //std::cout<<"row="<<row<<" col="<<col<<" used:"<<matrixgrid[row][col]<<std::endl;
				// if(matrixgrid[row][col]==0 && col<=row)
				// {
					// colball=col;
					// rowball=row;//
					// flagfound=1;
					// std::cout<<"row="<<rowball<<" col="<<colball<<" is selected"<<" occp="<<matrixgrid[row][col]<<std::endl;
					// break;
				// }
			// }
			
			//std::cout<<"rowball="<<rowball<<" colball="<<colball<<std::endl;
			//std::cout<<"press any int to continue:";
			//std::cin>>tempa;
			
		
			
			//随机选择形状:
			
			int sn_now=rand()%n_ofshapes;//随机选择一个形状，索引以0开始
			while(flagshapeused[sn_now] != 0){
				sn_now=rand()%n_ofshapes;
				//std::cout<<"shape sn="<<sn_now<<" used:"<<flagshapeused[sn_now]<<std::endl;
			}
			
			//std::cout<<"shape sn="<<sn_now<<std::endl;
			//veclinkshape[sn_now].pos_show();
			//std::cout<<"press any int to continue:"<<std::endl;
			//std::cin>>tempa;
			
			
			//在拼图中加入形状
			int flagcanbeset=0;//标记是否可以加入拼图，0表示不能
			int n_balls=veclinkshape[sn_now].getshapenballs();
			int settimes=0;//变换次数，用于错误处理
			
		
			while(flagcanbeset==0 && settimes<20)//变换次数多于一定次数仍然不能加入，说明该形状无法加入，则退出循环
			{
				settimes++;
				
				//尝试当前形状变换状态下设置不同的焦点球能否放入
				int sn_focus;//遍历选择焦点球
				int rowfocus;
				int colfocus;
				int flagballused[n_balls];
				for(int i=0;i<n_balls;++i)
				{
					flagballused[i]=0;
				}
				while(true)
				{
					flagcanbeset=1;
					sn_focus=rand()%n_balls;//随机选择焦点球
					while(flagballused[sn_focus]!=0){
						sn_focus=rand()%n_balls;
					}
					flagballused[sn_focus]=1;
					rowfocus=veclinkshape[sn_now].getptrow(sn_focus);
					colfocus=veclinkshape[sn_now].getptcol(sn_focus);
									
					for(int i=0;i<n_balls;++i)//判断一下当前形状能否加入拼图
					{
						int drow=veclinkshape[sn_now].getptrow(i)-rowfocus;
						int dcol=veclinkshape[sn_now].getptcol(i)-colfocus;
						int row=rowball+drow;//焦点球放到当前起点位置上
						int col=colball+dcol;
						// if(col<0 || row<0 || col>row || row>=n_scale){//增加一个约束
							// flagcanbeset=0;
							// break;
						// }
						if(col<0 || row<0 || col>row || row>=n_scale){//增加一个约束
							flagcanbeset=0;
							break;
						}
						if(matrixgrid[row][col]>0 ){
							flagcanbeset=0;
							break;
						}
					}
					if(flagcanbeset==1) break;
					int flagballallused=0;//判断一下焦点是不是已经遍历所有球
					for(int i=0;i<n_balls;++i)
					{
						flagballallused+=flagballused[i];
					}
					if(flagballallused>=n_balls) break;
				}
				
				//当上述变换焦点球仍不能加入时，做形状变换
				if(flagcanbeset==0)
				{
					int transid=rand()%4+1;
					switch(transid)
					{
						case 1:
							veclinkshape[sn_now].rotate_right();
							break;
						case 2:
							veclinkshape[sn_now].rotate_left();
							break;
						case 3:
							veclinkshape[sn_now].mirror_ab();
							break;
						case 4:
							veclinkshape[sn_now].mirror_lr();
							break;
						default:
							break;
					}
				}else{
					for(int i=0;i<n_balls;++i)
					{
						int drow=veclinkshape[sn_now].getptrow(i)-rowfocus;
						int dcol=veclinkshape[sn_now].getptcol(i)-colfocus;
						int row=rowball+drow;//焦点球放到当前起点位置上
						int col=colball+dcol;
						if(row>=0 && col>=0 ){//避免影响到其他变量，因为row或col为负时，内存指向到其它变量中了，而上界因为2*n_scale，余量比较大一般不会超出本数组范围。
						matrixgrid[row][col]=sn_now+1;//用形状的序号表示占用
						}
					}
					//veclinkshape[sn_now].pos_show();
					//std::cout<<"press any int to continue:";
					//std::cin>>tempa;
					if(flagouthints==1) std::cout<<"shape id="<<sn_now+1<<" is used!"<<std::endl;
					flagshapeused[sn_now]=1;
					
				}
			}
			
			//显示一下拼图占用情况
			// for(int i=0;i<n_scale;++i)
			// {
				// for(int j=0;j<=i;++j)
				// {
					// printf("%5d",matrixgrid[i][j]);
				// }
				// printf("\n");
			// }
			
			
			//判断一下是否所有形状都加入拼图中
			int flagallused=0;
			for(int i=0;i<n_ofshapes;++i)
			{
				flagallused=flagallused+flagshapeused[i];
			}
			if(flagallused==n_ofshapes){
				flagmergeok=1;
			}

		}
		//std::cout<<"added all shapes:"<<flagmergeok<<std::endl;
		//std::cout<<"press any int to continue:";
		//std::cin>>tempa;
		
		
		//一次拼图后，所有形状的使用状态重设:
		for(int i=0;i<n_ofshapes;++i)
		{
			flagshapeused[i]=0;
		}
		
				
		//判断拼图是否成功
		flagok=1;
		for(int i=0;i<n_scale;++i)
		{
			for(int j=0;j<=i;++j){
				if(matrixgrid[i][j]==0){
					flagok=0;
					break;
				}
			}
			if(flagok==0) break;
		}
		if(flagok==0)//本次拼图未成功，则重新开始拼图，重设占用
		{
			flagmergeok=0;//重新拼图标志:
			for(int i=0;i<n_scale*2;++i)
			{
				for(int j=0;j<n_scale*2;++j){
					matrixgrid[i][j]=0;
				}
			}
		}else
		{
			//显示一下拼图占用情况
			std::ofstream outfile;
			outfile.open("sn-gridc.dat",std::ios_base::out|std::ios_base::app);
			outfile<<"------------"<<std::endl;
			outfile<<"times="<<mgtimes<<std::endl;
			for(int i=0;i<n_scale;++i)
			{
				for(int j=0;j<=i;++j)
				{
					printf("%5d",matrixgrid[i][j]);
					outfile<<std::setw(5)<<matrixgrid[i][j];
				}
				printf("\n");
				outfile<<std::endl;
			}
			outfile.close();
		}
		//std::cout<<"time="<<mgtimes<<" is seccessful:"<<flagok<<std::endl;
		//std::cout<<"press any int to continue:"<<std::endl;
		//std::cin>>tempa;
	}
	
	return mgtimes;
}




int mergeb()//将形状合成三角网格(起点随机选择)
{
	int matrixgrid[n_scale*2][n_scale*2]={0};//用于标记当前行列位置的是否已占据
	for(int i=0;i<n_scale*2;++i)
	{
		for(int j=0;j<n_scale*2;++j){
			matrixgrid[i][j]=0;
		}
	}
	int flagok=0;//拼图成功
	int flagmergeok=0;//标记当前各形状拼图完成
	int flagshapeused[n_ofshapes]={0};//标记各形状是否已经使用过
	
	int tempa;//临时
	//srand(time(NULL));
	srand(time(0));
	
	int colball=0;//起点位置
	int rowball=0;
	int mgtimes=0;//拼图的次数
	while(flagok==0 && mgtimes<50000)//设置拼图尝试次数，避免无限循环
	{
		if(flagouthints==1){
			std::cout<<"------------------"<<std::endl;
			std::cout<<"start "<<mgtimes<<std::endl;
			//显示一下拼图占用情况
			// for(int i=0;i<n_scale;++i)
			// {
				// for(int j=0;j<=i;++j)
				// {
					// printf("%5d",matrixgrid[i][j]);
				// }
				// printf("\n");
			// }
		}
		
		++mgtimes;
		int nstimes=0;//尝试加入新形状的次数
		while(flagmergeok==0 && nstimes< n_ofshapes*2)//当尝试加入新形状的次数次数多于一定次数，说明当前拼图无法完成，则退出循环，进入下一次拼图
		{
			++nstimes;
			
			
			//确定起点
			// for(int col=0;col<n_scale;++col)//从第1列开始找没有填充的位置
			// {
				// int flagfound=0;
				// for(int row=col;row<n_scale;++row)//从当前列第一行开始找没有填充的位置
				// {
					// if(matrixgrid[row][col]==0){
						// colball=col;//形状的中最小栏，最小行的球的所要放的位置
						// rowball=row;//
						// flagfound=1;
						// std::cout<<"row="<<rowball<<" col="<<colball<<" is selected"<<" occp="<<matrixgrid[row][col]<<std::endl;
						// break;
					// }
				// }
				// if(flagfound==1) break;
			// }
			
			
			//另一种确定起点机制，随机选取
			int flagfound=0;
			while(flagfound==0)
			{
				int row=rand()%n_scale;
				int col=rand()%n_scale;
				//std::cout<<"row="<<row<<" col="<<col<<" used:"<<matrixgrid[row][col]<<std::endl;
				if(matrixgrid[row][col]==0 && col<=row)
				{
					colball=col;
					rowball=row;//
					flagfound=1;
					if(flagouthints==1) std::cout<<"row="<<rowball<<" col="<<colball<<" is selected"<<" occp="<<matrixgrid[row][col]<<std::endl;
					break;
				}
			}
			
			//std::cout<<"rowball="<<rowball<<" colball="<<colball<<std::endl;
			//std::cout<<"press any int to continue:";
			//std::cin>>tempa;
			
			
			//随机选择形状:
			
			int sn_now=rand()%n_ofshapes;//随机选择一个形状，序号以0开始
			while(flagshapeused[sn_now]!=0){
				sn_now=rand()%n_ofshapes;
			}
			
			//std::cout<<"shape sn="<<sn_now<<std::endl;
			//veclinkshape[sn_now].pos_show();
			//std::cout<<"press any int to continue:";
			//std::cin>>tempa;
			
			
			//在拼图中加入形状
			int flagcanbeset=0;//标记是否可以加入拼图，0表示不能
			int n_balls=veclinkshape[sn_now].getshapenballs();
			int settimes=0;//变换次数，用于错误处理
			while(flagcanbeset==0 && settimes<20)//变换次数多于一定次数仍然不能加入，说明该形状无法加入，则退出循环
			{
				settimes++;
				
				//尝试当前形状变换状态下设置不同的焦点球能否放入
				int sn_focus;//遍历选择焦点球
				int rowfocus;
				int colfocus;
				int flagballused[n_balls];
				for(int i=0;i<n_balls;++i)
				{
					flagballused[i]=0;
				}
				while(true)
				{
					flagcanbeset=1;
					sn_focus=rand()%n_balls;//随机选择焦点球
					while(flagballused[sn_focus]!=0){
						sn_focus=rand()%n_balls;
					}
					flagballused[sn_focus]=1;
					rowfocus=veclinkshape[sn_now].getptrow(sn_focus);
					colfocus=veclinkshape[sn_now].getptcol(sn_focus);
									
					for(int i=0;i<n_balls;++i)//判断一下当前形状能否加入拼图
					{
						int drow=veclinkshape[sn_now].getptrow(i)-rowfocus;
						int dcol=veclinkshape[sn_now].getptcol(i)-colfocus;
						int row=rowball+drow;//焦点球放到当前起点位置上
						int col=colball+dcol;
						if(col<0 || row<0 || col>row || row>=n_scale){//增加一个约束
							flagcanbeset=0;
							break;
						}
						if(matrixgrid[row][col]>0){
							flagcanbeset=0;
							break;
						}
					}
					if(flagcanbeset==1) break;
					int flagballallused=0;
					for(int i=0;i<n_balls;++i)
					{
						flagballallused+=flagballused[i];
					}
					if(flagballallused>=n_balls) break;
				}
				
				//当上述变换焦点球仍不能加入时，做形状变换
				if(flagcanbeset==0)
				{
					int transid=rand()%4+1;
					switch(transid)
					{
						case 1:
							veclinkshape[sn_now].rotate_right();
							break;
						case 2:
							veclinkshape[sn_now].rotate_left();
							break;
						case 3:
							veclinkshape[sn_now].mirror_ab();
							break;
						case 4:
							veclinkshape[sn_now].mirror_lr();
							break;
						default:
							break;
					}
				}else{
					for(int i=0;i<n_balls;++i)
					{
						int drow=veclinkshape[sn_now].getptrow(i)-rowfocus;
						int dcol=veclinkshape[sn_now].getptcol(i)-colfocus;
						int row=rowball+drow;//焦点球放到当前起点位置上
						int col=colball+dcol;
						matrixgrid[row][col]=sn_now+1;//用形状的序号表示占用
						//std::cout<<"row="<<row<<" col="<<col<<" is seted"<<std::endl;
					}
					//veclinkshape[sn_now].pos_show();
					//std::cout<<"press any int to continue:";
					//std::cin>>tempa;
					if(flagouthints==1) std::cout<<"shape id="<<sn_now+1<<" is used!"<<std::endl;
					flagshapeused[sn_now]=1;
				}
			}
			
			//显示一下拼图占用情况
			// for(int i=0;i<n_scale;++i)
			// {
				// for(int j=0;j<=i;++j)
				// {
					// printf("%5d",matrixgrid[i][j]);
				// }
				// printf("\n");
			// }
			
			
			//判断一下是否所有形状都加入拼图中
			int flagallused=0;
			for(int i=0;i<n_ofshapes;++i)
			{
				flagallused+=flagshapeused[i];
			}
			if(flagallused==n_ofshapes){
				flagmergeok=1;
			}

		}
		//std::cout<<"added all shapes:"<<flagmergeok<<std::endl;
		//std::cout<<"press any int to continue:";
		//std::cin>>tempa;
		
		
		//一次拼图后，所有形状的使用状态重设:
		for(int i=0;i<n_ofshapes;++i)
		{
			flagshapeused[i]=0;
		}
		
				
		//判断拼图是否成功
		flagok=1;
		for(int i=0;i<n_scale;++i)
		{
			for(int j=0;j<=i;++j){
				if(matrixgrid[i][j]==0){
					flagok=0;
					break;
				}
			}
			if(flagok==0) break;
		}
		if(flagok==0)//本次拼图未成功，则重新开始拼图，重设占用
		{
			flagmergeok=0;//重新拼图标志:
			for(int i=0;i<n_scale*2;++i)
			{
				for(int j=0;j<n_scale*2;++j){
					matrixgrid[i][j]=0;
				}
			}
		}else
		{
			//显示一下拼图占用情况
			std::ofstream outfile;
			outfile.open("sn-gridb.dat",std::ios_base::out|std::ios_base::app);
			outfile<<"------------"<<std::endl;
			outfile<<"times="<<mgtimes<<std::endl;
			for(int i=0;i<n_scale;++i)
			{
				for(int j=0;j<=i;++j)
				{
					printf("%5d",matrixgrid[i][j]);
					outfile<<std::setw(5)<<matrixgrid[i][j];
				}
				printf("\n");
				outfile<<std::endl;
			}
			outfile.close();
		}
		std::cout<<"time="<<mgtimes<<" is seccessful:"<<flagok<<std::endl;
		//std::cout<<"press any int to continue:"<<std::endl;
		//std::cin>>tempa;
	}
	
	return mgtimes;
}


coord getrowcolformsn(int sn_ball){//输入是球的真实序号
	int nij=0;
	coord a={0,0};
	for(int i=0;i<n_scale;i++)
	{
		for(int j=0;j<=i;j++)
		{
			nij++;
			if(nij==sn_ball)
			{
				a={i,j};
				return a;
			}
		}
	}
	std::abort();//当sn_ball不在范围内时，直接退出
	return a;//这可能导致出错，如果sn_ball不在范围内时，所以采用上一句直接结束程序
}

int getsnfromrowcol(int row,int col){//输入的行和列是以0为起点的
	if(row<0) return -1;
	if(col<0) return -1;
	if(row>n_scale) return -1;
	if(col>row) return -1;
	
	int nij=0;
	for(int i=0;i<row;i++)
	{
		for(int j=0;j<=i;j++)
		{
			nij++;
		}
	}
	return nij+col+1;//sn_ball
}



int getnumdrowdcol(int drow,int dcol){//根据焦点球序号以及与焦点球的行距和列距确定当前球序号

	 coord a=getrowcolformsn(n_focus);//获取焦点球的行列
	 int row=a.row+drow;
	 int col=a.col+dcol;
	 return getsnfromrowcol(row,col);
	 
}


int getnumdrowdcola(int drow,int dcol){//根据焦点球序号以及与焦点球的行距和列距确定当前球序号
	 	
	//这种思路要注意的是因为列数总是小于等于当前行的行号，所以先走行，在走列
	int flagoutrange=0;
	int sn_now=n_focus-1;//sn_now是在矢量中的序号，等于球真实序号-1
	if(drow <=0) {
		for(int j=0;j<fabs(drow);j++)
		{
			if(sn_now>=0) {
				sn_now=vecgrid[sn_now].getabove()-1;//sn_now是在矢量中的序号，等于球真实序号-1
			}else
			{
				flagoutrange=1;
				j=fabs(drow);
			}
		}
	}else{
		for(int j=0;j<fabs(drow);j++)
		{
			if(sn_now>=0) {
				sn_now=vecgrid[sn_now].getbelow()-1;//sn_now是在矢量中的序号，等于球真实序号-1
			}else
			{
				flagoutrange=1;
				j=fabs(drow);
			}
		}
	}
	if(dcol <=0) {
		for(int j=0;j<fabs(dcol);j++)
		{
			if(sn_now>=0) {
				sn_now=vecgrid[sn_now].getleft()-1;//sn_now是在矢量中的序号，等于球真实序号-1
			}else
			{
				flagoutrange=1;
				j=fabs(dcol);
			}
		}
	}else{
		for(int j=0;j<fabs(dcol);j++)
		{
			if(sn_now>=0) {
				sn_now=vecgrid[sn_now].getright()-1;//sn_now是在矢量中的序号，等于球真实序号-1
			}else
			{
				flagoutrange=1;
				j=fabs(dcol);
			}
		}
	}
	if(flagoutrange==1){
		return -1;
	}else{
	return sn_now+1;
	}
	
}
	
void setfocus(const int i){//设置焦点球序号,序号为球的真实序号，从1开始计数
	n_focus=i;
}


void trigridshapedshow(){//显示下三角网格信息,被占用的情况
    balltopo trigrid[n_scale][n_scale];
	int nij=0;
    for (int i=0;i<n_scale;i++){
            for(int j=0;j<=i;j++)
			{
				//矩阵和矢量的关系是
                trigrid[i][j]=vecgrid[nij];
				nij++;
			}
        }

    for(int i=1; i<=n_scale; i++)//行
        {
            for(int j=1; j<=i; j++)//列
            {
                if(j==i){
					if(trigrid[i-1][j-1].getshpd()==1) {printf("     *\n");}
					else{printf(" %5d\n",trigrid[i-1][j-1].getsn());}
					}
                else{
					if(trigrid[i-1][j-1].getshpd()==1) {
						printf("     *");
					}else{
						printf(" %5d",trigrid[i-1][j-1].getsn());
					}
					}
            }
        }
		
	// for(int i=0;i<n_total;i++)
	// {
		// printf("%5d ",vecgrid[i].getsn());
	// }
	// printf("\n");
	
}

void trigriddisplay(){//显示下三角网格信息函数
    balltopo trigrid[n_scale][n_scale];
	int nij=0;
    for (int i=0;i<n_scale;i++){
            for(int j=0;j<=i;j++)
			{
				//矩阵和矢量的关系是
                trigrid[i][j]=vecgrid[nij];
				nij++;
			}
        }

    for(int i=1; i<=n_scale; i++)//行
        {
            for(int j=1; j<=i; j++)//列
            {
                if(j==i){printf(" %5d\n",trigrid[i-1][j-1].getsn());}
                else{printf(" %5d",trigrid[i-1][j-1].getsn());}
            }
        }
		
	// for(int i=0;i<n_total;i++)
	// {
		// printf("%5d ",vecgrid[i].getsn());
	// }
	// printf("\n");
	
}


void trigridinit(){//下三角网格信息初始化
    balltopo trigrid[n_scale][n_scale];
    int n=n_scale;
    int sumlinelessi=0;
    int sn=0;
    for(int i=1; i<=n; i++)//行
    {
        sumlinelessi=sumlinelessi+(i-1);//i行前的球数,每行的球数都等于该行的行号
        for(int j=1; j<=i; j++)//列
        {
            //序号
            sn=sumlinelessi+j; //sn_self=sum_{k=1}^{i-1}(i)+j,注意:序号从1开始
                                                //但数组是从0开始的
            //左侧邻居
            int left=0;
            if(j==1){
                left=-1;//j=1时,左侧无邻居,所以设置为-1
            }
            else{
                left=sn-1;
            }

            //右侧邻居
            int right=0;
            if(j==i){
                right=-1;//j=i时,右侧无邻居,所以设置为-1
            }
            else{
                right=sn+1;
            }

            //上方邻居
            int above=0;
            if(i==j){
                above=-1;//i=j时,上方无邻居,所以设置为-1
            }
            else{
                above=sn-i+1;
            }

            //下方邻居
            int below=0;
            if(i==n){
                below=-1;//i=n时,下方无邻居,所以设置为-1
            }
            else{
                below=sn+i;
            }
			
			printf("sn:%d,left:%d,right:%d,above:%d,below:%d\n",sn,left,right,above,below);
            int toposet[5]={sn,left,right,above,below};
            trigrid[i-1][j-1].settopo(toposet);
        }
    }
    n_total=sn;
	int nij=0;
    for (int i=0;i<n_scale;i++)
	{
        for(int j=0;j<=i;j++)//[i][j]与矢量中序号是一一对应的。
		{ 
			trigrid[i][j].setoccp(0);
			trigrid[i][j].setshpd(0);
			vecgrid[nij]=trigrid[i][j];
			nij++;
		}
    }
}


void trigridtest(){//查看当前球及其邻居序号测试
    balltopo trigrid[n_scale][n_scale];
	int nij=0;
    for (int i=0;i<n_scale;i++)
	{
        for(int j=0;j<=i;j++)
		{
            trigrid[i][j]=vecgrid[nij];
			//printf("%d sn=%d\n",nij,vecgrid[nij].getsn());
			nij++;
		}
    }
    int n=n_scale;

    for(int i=1; i<=n; i++)//行
        {
            for(int j=1; j<=i; j++)//列
            {
                trigriddisplay();
                int topoget[5]={0};
                trigrid[i-1][j-1].gettopo(topoget);
                printf("%5c%5d%5c\n",' ',topoget[3],' ');
                printf("%5d%5d%5d\n",topoget[1],topoget[0],topoget[2]);
                printf("%5c%5d%5c\n",' ',topoget[4],' ');

                //char ch;
                //printf("please put in a key to continue:");
                //ch = getchar();
            }
        }
}

};


#endif // SHAPE_H
