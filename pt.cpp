#include<iostream>
#include <fstream>
#include"classgrid.h"
#include <vector>
#include <time.h>

int main(int argc, char* argv[])
{

    if(argc < 3) {
        std::cerr<<"error:require input coefficients"<<std::endl;
        return 1;
    }
	else if(argc == 3){
		std::cout<<"right input!"<<std::endl;
	}
	else{
		std::cout<<"input coefficients more than required, get the first 2 coefficients!"<<std::endl;
	}

	for(int i=0;i<argc;i++){
		std::cout<<"input argv:"<< argv[i] <<std::endl;
	}
    // std::cout<<"input argv:"<< *argv <<std::endl;
    // std::cout<<"input argv:"<< *(argv+1) <<std::endl;
    // std::cout<<"input argv:"<< argv[0] <<std::endl;
    // std::cout<<"input argv:"<< argv[1] <<std::endl;
	
	// char tempa;
	// std::cout<<"please put a key to continue:"<<std::endl;
	// std::cin>>tempa;
	
	int gridsize; //拼图总的大小，即拼图的球网格大小
	int linksize; //拼图中连接球形状大小，即一个形状中的连接球数
	gridsize=std::atoi(argv[1]);//字符串转换为整数
	linksize=std::atoi(argv[2]);

    
	//测试拼图算法
	int res;
	clock_t start, end;
	double cpu_time_used;
	
	
	//ofstream outfile("sn-times.dat");
	// std::ofstream outfile;
	// outfile.open("sn-times.csv");
	// std::ofstream outfileb;
	// outfileb.open("sn-timesb.csv");
	std::ofstream outfilec;
	outfilec.open("sn-timesc.csv");
	
	grid gridb=grid(gridsize,linksize);
    gridb.trigriddisplay();
	gridb.Partition();
	gridb.veclinksave();
    gridb.outputshapes();

	//std::cin>>tempa;
	
	// if(0){
		// for(int i=0;i<20;++i)
		// {
			// gridb.veclinkrestore();
			// int res=gridb.merge();
			// outfile<<i+1<<","<<res<<std::endl;
			
			// gridb.veclinkrestore();
			// res=gridb.mergeb();
			// outfileb<<i+1<<","<<res<<std::endl;
			// //int tempa;
			// //std::cin>>tempa;
		// }
		// outfile.close();
		// outfileb.close();
	// }
	

	
	if(1){
		for(int i=0;i<1;++i)
		{
			std::cout<<"--------------"<<std::endl;
			gridb.veclinkrestore();
			start = clock();
			res=gridb.merge();
			end = clock();
			cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
			outfilec<<i+1<<","<<res<<","<<cpu_time_used<<std::endl;
			std::cout<<i+1<<","<<res<<","<<cpu_time_used<<std::endl;
			//int tempa;
			//std::cin>>tempa;
		}
		outfilec.close();
	}
	
    return 0;
}
