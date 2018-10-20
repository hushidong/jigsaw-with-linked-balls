# -*- coding: utf-8 -*-

"""
基于矩阵填充的球链接形状拼图算法
"""

import copy
import random
import time
import json
import sys


def MatrixTransform(mb,mirror,rotate):
    """
    mirror：翻转
    rotate：选择
    """
    rows=len(mb)
    cols=len(mb[0])
    
    #先做翻转
    mbn=[[0 for col in range(cols)] for row in range(rows)]
    
    if mirror==1:#l-r
        for row in range(rows):
            for col in range(cols):
                mbn[row][col]=mb[row][cols-1-col]
    elif mirror==2:#u-d
        for row in range(rows):
            for col in range(cols):
                mbn[row][col]=mb[rows-1-row][col]
    elif mirror==0:
        mbn=copy.deepcopy(mb)
    
    #接着做旋转
    if rotate==1:
        mcn=[[0 for col in range(rows)] for row in range(cols)]
        for row in range(cols):
            for col in range(rows):
                mcn[row][col]=mbn[col][cols-1-row]
    elif rotate==2:
        mcn=[[0 for col in range(cols)] for row in range(rows)]
        for row in range(rows):
            for col in range(cols):
                mcn[row][col]=mbn[rows-1-row][cols-1-col]
    elif rotate==3:
        mcn=[[0 for col in range(rows)] for row in range(cols)]
        for row in range(cols):
            for col in range(rows):
                mcn[row][col]=mbn[rows-1-col][row]
    elif rotate==0:
        mcn=mbn
    return mcn

def MatchCheckS(mc,md,shapeidx):
    
    rowsa=len(mc)
    rowsb=len(md)
    colsb=len(md[0])
    ptlist=[[i,j] for i in range(0,rowsa) for j in range(0,i+1) if mc[i][j]==1]
    ptslen=len(ptlist)
#    print("mc=",mc)
#    print("md=",md)
#    print("start pts=",ptlist)
#    print("pt number=",ptslen)
    
    startptchoose=0
    while startptchoose<ptslen:#可以选择A矩阵焦点的次数
        startptchoose+=1
        #矩阵a中的起点选择
        
        #第一种选择机制
        ptijn=random.randint(0,ptslen-1)
        rowa=ptlist[ptijn][0]
        cola=ptlist[ptijn][1]
        
        
        #第二种选择机制
#        rowa=random.randint(0,rowsa-1)
#        cola=random.randint(0,rowa)
#        #print("匹配焦点为[%d,%d]"%(rowa,cola))
#        while not mc[rowa][cola]==1:
#            rowa=random.randint(0,rowsa-1)
#            cola=random.randint(0,rowa)
        #print("")
        #print("待匹配矩阵a的匹配焦点为[%d,%d]"%(rowa,cola))
            
        #第三种选择机制
#        for i in range(rowsa):
#            for j in range(i):
#                if mc[i][j]==1:
#                    rowa=i
#                    cola=j
#                    break

        #第四种选择机制
        #rowa=ptlist[startptchoose-1][0]
        #cola=ptlist[startptchoose-1][1]
    
        for row in range(rowsb):#遍历待匹配矩形焦点
            for col in range(colsb):
                
                if md[row][col]==1:
                    focusneedchange=0
                    for i in range(rowsb):
                        for j in range(colsb):
                            if md[i][j]==1:
                                ia=rowa+i-row
                                ja=cola+j-col
                                #print("row=",row,"col=",col)
                                #print("i=",i,"j=",j)
                                #print("ia=",ia,"ja=",ja)
                                if ia<0 or ia > rowsa-1:
                                    focusneedchange=1
                                    break
                                if ja<0 or ja > ia:
                                    focusneedchange=1
                                    break
                                if not md[i][j]==mc[ia][ja]:
                                    focusneedchange=1
                                    break
                        if focusneedchange==1:
                            break
                    if focusneedchange==0:
                        for i in range(rowsb):
                            for j in range(colsb):
                                if md[i][j]==1:
                                    mc[rowa+i-row][cola+j-col]=2+shapeidx
                        return True
    return False

def MatchProcessS(ma,mbs):
    """
    """
    #rowsa=len(ma)
    #colsa=len(ma[0])
    nshapes=len(mbs)
    print("")
    print("ma =",ma)
    print("mbs=",mbs)
    
    k=0
    countchoose=0
    countmatch=0
    flagcompleted=0
    while flagcompleted==0:
        k+=1
        mc=copy.deepcopy(ma)
        print("")
        print("开始第%d次拼图"%(k))
        if k%10000 == 0:
            print("开始第%d次拼图"%(k))
        
        dealed=[]
        counta=0 #形状选择次数 
        countb=0 #形状匹配次数 
        lasttwo=[]
        shapeidxold=0
        while len(dealed)<nshapes and counta<2*nshapes:
        

            #选择一个形状
            shapeidx=random.randint(0,nshapes-1)
            while shapeidx in dealed:
                shapeidx=random.randint(0,nshapes-1)
                
            #当只剩下一个形状，且已经做过则退出
            if len(dealed)==nshapes-1:
                if shapeidxold==shapeidx:
                    break
                
            #当剩下2个形状时，且都已经做过则退出
            if len(dealed)==nshapes-2:
                if shapeidx not in lasttwo:
                    lasttwo.append(shapeidx)
                else:
                    if len(lasttwo)==2:
                        break
                
            counta+=1
            print("要匹配矩阵b的索引为%d"%(shapeidx))
            shapeidxold=shapeidx
            
            #做匹配，如果需要，做矩阵变换
            for i in range(8):
                if i==0:
                    md=copy.deepcopy(mbs[shapeidx])
                else:
                    md=MatrixTransform(mbs[shapeidx],i//4,i%4)
                    print("匹配失败做变换,mirror=%d,rotate=%d"%(i//4,i%4))
                    
                res=MatchCheckS(mc,md,shapeidx)
                countb+=1
                if res:
                    dealed.append(shapeidx)
                    print("匹配成功，结果为")
                    DisplayMatrix(mc)
                    break
        countchoose+=counta
        countmatch+=countb
        print("第%d次拼图，选择形状次数为%d"%(k,counta))
        print("第%d次拼图，形状匹配次数为%d"%(k,countb))
        if len(dealed)==nshapes:
            flagcompleted=1
    
    print("")
    #print("countchoose times=",countchoose)
    #print("countmatch  times=",countmatch)
    print("拼图结束")
    DisplayMatrix(mc)
    print("拼图所用次数为%d"%(k))
    print("形状选择总次数为%d"%(countchoose))    
    print("形状匹配总次数为%d"%(countmatch)) 


def MatchCheck(mc,md,rowa,cola,shapeidx):
    rowsa=len(mc)
    #colsa=len(mc[0])
    rowsb=len(md)
    colsb=len(md[0])
    for row in range(rowsb):#遍历焦点
        for col in range(colsb):
            
            if md[row][col]==1:
                focusneedchange=0
                for i in range(rowsb):
                    for j in range(colsb):
                        if md[i][j]==1:
                            ia=rowa+i-row
                            ja=cola+j-col
                            #print("row=",row,"col=",col)
                            #print("i=",i,"j=",j)
                            #print("ia=",ia,"ja=",ja)
                            if ia<0 or ia > rowsa-1:
                                focusneedchange=1
                                break
                            if ja<0 or ja > ia:
                                focusneedchange=1
                                break
                            if not md[i][j]==mc[ia][ja]:
                                focusneedchange=1
                                break
                    if focusneedchange==1:
                        break
                if focusneedchange==0:
                    mca=copy.deepcopy(mc)
                    for i in range(rowsb):
                        for j in range(colsb):
                            if md[i][j]==1:
                                mca[rowa+i-row][cola+j-col]=2+shapeidx
                    res=MatrixCheck(mca)#检测一下新的矩阵的合理性
                    if res:
                        for i in range(rowsb):
                            for j in range(colsb):
                                if md[i][j]==1:
                                    mc[rowa+i-row][cola+j-col]=2+shapeidx
                        return True
                    else:
                        return False
    return False
                
def TestMatchCheck():
    ma=[[1,0,0],
        [1,1,0],
        [1,1,1]]   
    mb=[[1,0],
        [1,1]]
    mb=[[1,1,1,1]]
    mb=[[1,1,1]]
    mb=[[1],[1],[1]]
    DisplayMatrix(ma)
    res=MatchCheck(ma,mb,2,2,0)
    print("match res:",res)
    DisplayMatrix(ma)
    res=MatchCheck(ma,mb,0,0,0)
    print("match res:",res)
    DisplayMatrix(ma)
    
    ma=[[1,0,0],
        [1,1,0],
        [1,1,1]]   
    mba=[[1,0],
         [1,1]]
    res=MatchCheck(ma,mba,1,1,0)
    print("match res:",res)
    DisplayMatrix(ma)

def DisplayMatrix(mc):
    setval="ABCDEFGHIJKLMNOPQRST"
    print("  |",end="")
    for j in range(len(mc[0])):
        print("%2s"%(j),end="")
    print(" |")
    print("--|",end="")
    for j in range(len(mc[0])):
        print("%2s"%("--"),end="")
    print(" |--")
    for i in range(len(mc)):
        print("%2d|"%(i),end="")
        for j in range(len(mc[0])):
            if mc[i][j]>=2:
                print("%2s"%(setval[mc[i][j]-2]),end="")
            elif mc[i][j]==1:
                print("%2s"%(str(mc[i][j])),end="")
            else:
                #pass
                #print("%2s"%(str(mc[i][j])),end="")
                print("  ",end="")
        print(" |%2d"%(i))
    print("--|",end="")
    for j in range(len(mc[0])):
        print("%2s"%("--"),end="")
    print(" |--")
    print("  |",end="")
    for j in range(len(mc[0])):
        print("%2s"%(j),end="")
    print(" |")

    
def MatrixCheck(mca):#检测拼上后的矩阵是否合理，不合理则返回false
    """
    不合理的情况包括:
    1. 形成一个包围的空腔，空腔内的方形数量小于所有可能的填充形状
    2. 第二种不是不合理的情况，而是为了减小搜索空间，即当一个形状填充后将剩余为填充的矩阵变为两个部分即认为它失败。
    """
    mc=copy.deepcopy(mca)
    #print("mc=",mc)
    countpart=0
    flagnone=0
    while not flagnone:
        
        #找第一个==1的位置
        flagnone=1#表示已经不存在==1的情况
        for i in range(len(mc)):
            outerbreak=0
            for j in range(i+1):
                #print(i,j,mc[i][j])
                if mc[i][j]==1:
                    row=i
                    col=j
                    countpart+=1
                    outerbreak=1
                    flagnone=0
                    break
            if outerbreak==1:
                break
                
        #把与所有该box连接的等于1的box设置成2
        if countpart>1:
            return False
        if flagnone==1:
            break
        SetBox(mc,row,col)
    #print("mc=",mc)
    return True

def SetBox(mc,row,col):
    #print("set box",row,col)
    mc[row][col]=2
    i=row+1
    j=col
    if i<len(mc) and mc[i][j]==1:
        SetBox(mc,i,j)
    i=row
    j=col-1
    if j>=0 and mc[i][j]==1:
        SetBox(mc,i,j)
    i=row-1
    j=col
    if i>=0 and mc[i][j]==1:
        SetBox(mc,i,j)
    i=row
    j=col+1
    if i>=j and mc[i][j]==1:
        SetBox(mc,i,j)
    return None    
    
def TestMatrixCheck():#测试矩阵是否被分为两个或以上部分

    ma=[[2,0,0,0],
        [2,1,0,0],
        [2,2,2,0],
        [2,2,2,2]]
    res=MatrixCheck(ma)
    print(res)
    
    ma=[[2,0,0,0],
        [2,1,0,0],
        [2,2,2,0],
        [2,1,1,1]]
    res=MatrixCheck(ma)
    print(res)
        

    
def MatchProcess(ma,mbs):
    """
    """
    rowsa=len(ma)
    #colsa=len(ma[0])
    nshapes=len(mbs)
    #print("")
    #print("ma =",ma)
    #print("mbs=",mbs)
    
    k=0
    countchoose=0
    countmatch=0
    lastchoose=0
    lastmatch=0
    flagcompleted=0
    while flagcompleted==0:
        k+=1
        mc=copy.deepcopy(ma)
        #print("")
        if k%10000 == 0:
            print("开始第%d次拼图"%(k))
        #print("开始第%d次拼图"%(k))
        
        dealed=[]
        counta=0 #形状选择次数 
        countb=0 #形状匹配次数 
        lasttwo=[]
        shapeidxold=0
        choosestart=1
        while len(dealed)<nshapes and counta<2*nshapes:
        
            #矩阵a中的起点选择
            # if choosestart==1:
                # rowa=random.randint(0,rowsa-1)
                # cola=random.randint(0,rowa)
                # #print("匹配焦点为[%d,%d]"%(rowa,cola))
                # while not mc[rowa][cola]==1:
                    # rowa=random.randint(0,rowsa-1)
                    # cola=random.randint(0,rowa)
                # choosestart=0#选择一个起点如果不能匹配则不变
            

                
            #另一种起点选择机制，这种选择有问题，当它被拼成一个空穴时可能本次拼图就彻底不行了。
            if choosestart==1:
                for i in range(rowsa):
                    outerbreak=0
                    for j in range(i+1):#这里i+1要特别注意的
                        #print("i=%d,j=%d,val=%d"%(i,j,mc[i][j]))
                        if mc[i][j]==1:
                            rowa=i
                            cola=j
                            outerbreak=1
                            choosestart=0#选择一个起点如果不能匹配则不变
                            break
                    if outerbreak==1:
                        break
                    
            #print("")    
            #print("待匹配矩阵a的匹配焦点为[%d,%d]"%(rowa,cola))
            #print("enter a key to continue")
            #tempa=input()
                        
                
            #选择一个形状
            shapeidx=random.randint(0,nshapes-1)
            while shapeidx in dealed:
                shapeidx=random.randint(0,nshapes-1)
                
            #当只剩下一个形状，且已经做过则退出
            if len(dealed)==nshapes-1:
                if shapeidxold==shapeidx:
                    break
                
            #当剩下2个形状时，且都已经做过则退出
            if len(dealed)==nshapes-2:
                if shapeidx not in lasttwo:
                    lasttwo.append(shapeidx)
                else:
                    if len(lasttwo)==2:
                        break
            counta+=1
            
            #print("要匹配矩阵b的索引为%d"%(shapeidx))
            shapeidxold=shapeidx
            
            #做匹配，如果需要，做矩阵变换
            for i in range(8):
                if i==0:
                    md=copy.deepcopy(mbs[shapeidx])
                else:
                    md=MatrixTransform(mbs[shapeidx],i//4,i%4)
                    #print("匹配失败做变换,mirror=%d,rotate=%d"%(i//4,i%4))
                    
                #print("md=",md)
                res=MatchCheck(mc,md,rowa,cola,shapeidx)
                countb+=1
                if res:
                    dealed.append(shapeidx)
                    choosestart=1#完成一次匹配则需要换起点
                    #print("匹配成功，结果为")
                    #DisplayMatrix(mc)
                    break
        countchoose+=counta
        countmatch+=countb
        lastchoose=counta
        lastmatch=countb
#        print("第%d次拼图，选择形状次数为%d"%(k,counta))
#        print("第%d次拼图，形状匹配次数为%d"%(k,countb))
        if len(dealed)==nshapes:
            flagcompleted=1
        #print("enter a key to continue")
        #tempa=input()
    
    #print("")
    #print("拼图结束")
    DisplayMatrix(mc)
    print("拼图所用次数为%d"%(k))
    print("形状选择总次数为%d"%(countchoose))    
    print("形状匹配总次数为%d"%(countmatch)) 
    return [lastchoose,countchoose,lastmatch,countmatch,k]


def MatchProcessa(ma,mbs):#old version
    """
    """
    rowsa=len(ma)
    #colsa=len(ma[0])
    nshapes=len(mbs)
    print("")
    print("ma =",ma)
    print("mbs=",mbs)
    
    k=0
    countchoose=0
    countmatch=0
    flagcompleted=0
    while flagcompleted==0:
        k+=1
        mc=copy.deepcopy(ma)
        print("")
        if k%10000 == 0:
            print("开始第%d次拼图"%(k))
        print("开始第%d次拼图"%(k))
        
        dealed=[]
        counta=0 #形状选择次数 
        countb=0 #形状匹配次数 
        lasttwo=[]
        shapeidxold=0
        while len(dealed)<nshapes and counta<2*nshapes:
        
            #矩阵a中的起点选择
            # rowa=random.randint(0,rowsa-1)
            # cola=random.randint(0,rowa)
            # #print("匹配焦点为[%d,%d]"%(rowa,cola))
            # while not mc[rowa][cola]==1:
                # rowa=random.randint(0,rowsa-1)
                # cola=random.randint(0,rowa)
            

                
            #另一种起点选择机制，这种选择有问题，当它被拼成一个空穴时可能本次拼图就彻底不行了。
            for i in range(rowsa):
                outerbreak=0
                for j in range(i+1):#这里i+1要特别注意的
                    print("i=%d,j=%d,val=%d"%(i,j,mc[i][j]))
                    if mc[i][j]==1:
                        rowa=i
                        cola=j
                        outerbreak=1
                        break
                if outerbreak==1:
                    break
                    
            print("")    
            print("待匹配矩阵a的匹配焦点为[%d,%d]"%(rowa,cola))
            #print("enter a key to continue")
            #tempa=input()
                        
                
            #选择一个形状
            shapeidx=random.randint(0,nshapes-1)
            while shapeidx in dealed:
                shapeidx=random.randint(0,nshapes-1)
                
            #当只剩下一个形状，且已经做过则退出
            if len(dealed)==nshapes-1:
                if shapeidxold==shapeidx:
                    break
                
            #当剩下2个形状时，且都已经做过则退出
            if len(dealed)==nshapes-2:
                if shapeidx not in lasttwo:
                    lasttwo.append(shapeidx)
                else:
                    if len(lasttwo)==2:
                        break
            counta+=1
            
            print("要匹配矩阵b的索引为%d"%(shapeidx))
            shapeidxold=shapeidx
            
            #做匹配，如果需要，做矩阵变换
            for i in range(8):
                if i==0:
                    md=copy.deepcopy(mbs[shapeidx])
                else:
                    md=MatrixTransform(mbs[shapeidx],i//4,i%4)
                    print("匹配失败做变换,mirror=%d,rotate=%d"%(i//4,i%4))
                    
                print("md=",md)
                res=MatchCheck(mc,md,rowa,cola,shapeidx)
                countb+=1
                if res:
                    dealed.append(shapeidx)
                    print("匹配成功，结果为")
                    DisplayMatrix(mc)
                    break
        countchoose+=counta
        countmatch+=countb
#        print("第%d次拼图，选择形状次数为%d"%(k,counta))
#        print("第%d次拼图，形状匹配次数为%d"%(k,countb))
        if len(dealed)==nshapes:
            flagcompleted=1
        #print("enter a key to continue")
        #tempa=input()
    
    print("")
    #print("拼图结束")
    DisplayMatrix(mc)
    print("拼图所用次数为%d"%(k))
    print("形状选择总次数为%d"%(countchoose))    
    print("形状匹配总次数为%d"%(countmatch)) 
            
def TestLargeJigsaw(filename):
    #读取形状矩阵
    f=open(filename,"r")
    data=json.load(f)
    f.close()
    print(data)
    print("length=",len(data))
    print("ma=",data[0])
    ma=data[0]
    mbs=[]
    for i in range(1,len(data)):
        print("mb=",data[i])
        mbs.append(data[i])
    print("")
    
    #拼图处理
    res=[]
    ntrys=2 #1000 #完成拼图次数，用于做多次拼图后取平均时间用
    start = time.clock()
   
    for i in range(ntrys):
        print("")
        print("the %d th try:"%(i+1))
        res.append(MatchProcess(ma,mbs))
        
    elapsed = (time.clock() - start)
    print("运行时间",elapsed,"秒") 
    
    timesassembly=0
    timeschoose=0
    timesmatch=0
    for i in range(ntrys):
        timesassembly+=res[i][4]
        timeschoose+=res[i][1]
        timesmatch+=res[i][3]
    
    timeavg=elapsed/ntrys
    assemblyavg=timesassembly/ntrys
    chooseavg=timeschoose/ntrys
    matchavg=timesmatch/ntrys
    
    print("%d %f %f %f %f\n"%(len(ma),timeavg,assemblyavg,chooseavg,matchavg))
    f=open("result-compare-matrix.dat","w")
    f.write("%d %f %f %f %f\n"%(len(ma),timeavg,assemblyavg,chooseavg,matchavg))
    f.close()
    
    #将拼图结果以json格式保存起来
    f = open("resjson.dat","w")
    json.dump(res,f)
    f.close()
    
        
def TestMatrixMatch():
    ma=[[1,0,0],
        [1,1,0],
        [1,1,1]]   
    mba=[[1,0],
        [1,1]]
    mbb=[[1,1,1]]
    MatchProcessS(ma,[mba,mbb])
    
def TestMatrixMatcha():
    ma=[[1,0,0,0],
        [1,1,0,0],
        [1,1,1,0],
        [1,1,1,1]]   
    mba=[[1,0],
         [1,1]]
    mbb=[[1,1,1],
         [1,0,0]]
    mbc=[[1,1,1]]
    MatchProcessS(ma,[mba,mbb,mbc])
    
def TestMatrixMatchb():#6-4
    ma=[[1,0,0,0,0,0],
        [1,1,0,0,0,0],
        [1,1,1,0,0,0],
        [1,1,1,1,0,0],
        [1,1,1,1,1,0],
        [1,1,1,1,1,1]]  
    mbs=[]
    mb=[[1],
        [1],
        [1]]
    mbs.append(mb)
    mb=[[1,0],
        [1,1],
        [0,1]]
    mbs.append(mb)
    mb=[[1,1],
        [1,1]]
    mbs.append(mb)
    mb=[[1,1,1],
        [1,0,0]]
    mbs.append(mb)
    mb=[[1,0],
        [1,1],
        [1,0]]
    mbs.append(mb)
    mb=[[1,1]]
    mbs.append(mb)
    start = time.clock()
    MatchProcess(ma,mbs)
    elapsed = (time.clock() - start)
    print("运行时间",elapsed,"秒") 

def TestMatrixMatchc():#7-4
    ma=[[1,0,0,0,0,0,0],
        [1,1,0,0,0,0,0],
        [1,1,1,0,0,0,0],
        [1,1,1,1,0,0,0],
        [1,1,1,1,1,0,0],
        [1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1]]  
    mbs=[]
    mb=[[1,0],
        [1,1],
        [0,1]]
    mbs.append(mb)
    mb=[[1,0],
        [1,1]]
    mbs.append(mb)
    mb=[[1,0],
        [1,1],
        [1,0]]
    mbs.append(mb)
    mb=[[1],
        [1]]
    mbs.append(mb)
    mb=[[1,1,1,1]]
    mbs.append(mb)
    mb=[[1,1,1],
        [1,0,0]]
    mbs.append(mb)
    mb=[[1,1,1]]
    mbs.append(mb)
    mb=[[1,1],
        [1,1]]
    mbs.append(mb)
    start = time.clock()
    MatchProcess(ma,mbs)
    elapsed = (time.clock() - start)
    print("运行时间",elapsed,"秒")

def TestMatrixMatchd():#8-5
    ma=[[1,0,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,1,1,0,0,0,0,0],
        [1,1,1,1,0,0,0,0],
        [1,1,1,1,1,0,0,0],
        [1,1,1,1,1,1,0,0],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1]]  
    mbs=[]
    mb=[[1,0,0],
        [1,1,0],
        [0,1,1]]
    mbs.append(mb)
    mb=[[1,0,0,0],
        [1,1,1,1]]
    mbs.append(mb)
    mb=[[1,1,1,1,1]]
    mbs.append(mb)
    mb=[[1,0,0],
        [1,0,0],
        [1,1,1]]
    mbs.append(mb)
    mb=[[1],
        [1]]
    mbs.append(mb)
    mb=[[1,0],
        [1,1],
        [0,1]]
    mbs.append(mb)
    mb=[[1,1],
        [1,1],
        [1,0]]
    mbs.append(mb)
    mb=[[0,1,1],
        [0,1,0],
        [1,1,0]]
    mbs.append(mb)
    start = time.clock()
    MatchProcess(ma,mbs)
    elapsed = (time.clock() - start)
    print("运行时间",elapsed,"秒")

def TestMatrixMatche():#9-5
    ma=[[1,0,0,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0,0],
        [1,1,1,0,0,0,0,0,0],
        [1,1,1,1,0,0,0,0,0],
        [1,1,1,1,1,0,0,0,0],
        [1,1,1,1,1,1,0,0,0],
        [1,1,1,1,1,1,1,0,0],
        [1,1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1,1]]  
    mbs=[]
    mb=[[1,1],
        [1,1],
        [1,0]]
    mbs.append(mb)
    mb=[[0,1,0],
        [0,1,1],
        [1,1,0]]
    mbs.append(mb)
    mb=[[1,0],
        [1,1],
        [0,1],
        [0,1]]
    mbs.append(mb)
    mb=[[1,0,0],
        [1,0,0],
        [1,1,1]]
    mbs.append(mb)
    mb=[[0,0,1,0],
        [1,1,1,1]]
    mbs.append(mb)
    mb=[[1,1]]
    mbs.append(mb)
    mb=[[0,1,0],
        [1,1,1]]
    mbs.append(mb)
    mb=[[1,1],
        [0,1],
        [1,1]]
    mbs.append(mb)
    mb=[[1,0,0],
        [1,1,0],
        [0,1,1]]
    mbs.append(mb)
    mb=[[1,1,1],
        [0,0,1]]
    mbs.append(mb)
    start = time.clock()
    MatchProcess(ma,mbs)
    elapsed = (time.clock() - start)
    print("运行时间",elapsed,"秒")
    
def TestMatrixMatchf():#10-5
    ma=[[1,0,0,0,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0,0,0],
        [1,1,1,0,0,0,0,0,0,0],
        [1,1,1,1,0,0,0,0,0,0],
        [1,1,1,1,1,0,0,0,0,0],
        [1,1,1,1,1,1,0,0,0,0],
        [1,1,1,1,1,1,1,0,0,0],
        [1,1,1,1,1,1,1,1,0,0],
        [1,1,1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1,1,1]]  
    mbs=[]
    mb=[[1,0,0],
        [1,1,0],
        [0,1,1]]
    mbs.append(mb)
    mb=[[1,0],
        [1,1],
        [0,1],
        [0,1]]
    mbs.append(mb)
    mb=[[1,1],
        [1,1],
        [1,0]]
    mbs.append(mb)
    mb=[[1],
        [1],
        [1],
        [1]]
    mbs.append(mb)
    mb=[[1,0,0],
        [1,0,0],
        [1,1,1]]
    mbs.append(mb)
    mb=[[1,0,0],
        [1,1,1]]
    mbs.append(mb)
    mb=[[0,1,0],
        [1,1,1],
        [0,1,0]]
    mbs.append(mb)
    mb=[[1,1],
        [1,0]]
    mbs.append(mb)
    mb=[[1,1],
        [0,1],
        [1,1]]
    mbs.append(mb)
    mb=[[1,1],
        [1,0],
        [1,0],
        [1,0]]
    mbs.append(mb)
    mb=[[1,1],
        [1,1]]
    mbs.append(mb)
    mb=[[0,0,1,0],
        [1,1,1,1]]
    mbs.append(mb)
    start = time.clock()
    MatchProcess(ma,mbs)
    elapsed = (time.clock() - start)
    print("运行时间",elapsed,"秒")
       
def TestMatrixTransform():
    mb=[[1,0],[1,0],[1,1]]
    print(mb)
    mbn=MatrixTransform(mb,0,1)
    print(mbn)
    mbn=MatrixTransform(mb,0,2)
    print(mbn)
    mbn=MatrixTransform(mb,0,3)
    print(mbn)
    mbn=MatrixTransform(mb,1,0)
    print(mbn)
    mbn=MatrixTransform(mb,1,1)
    print(mbn)
    mbn=MatrixTransform(mb,1,2)
    print(mbn)
    mbn=MatrixTransform(mb,1,3)
    print(mbn)
    mbn=MatrixTransform(mb,2,0)
    print(mbn)
    mbn=MatrixTransform(mb,2,1)
    print(mbn)
    mbn=MatrixTransform(mb,2,2)
    print(mbn)
    mbn=MatrixTransform(mb,2,3)
    print(mbn)
    
    

if __name__=="__main__":
	savedStdout = sys.stdout #保存标准输出流
	filename="datatopython.dat"
	outfile="out-matrixmethod"+filename
	file=open(outfile,'w+')
	sys.stdout = file #标准输出重定向至文件
	print(filename,"started!")
	TestLargeJigsaw(filename)
	sys.stdout = savedStdout #恢复标准输出流
	file.close()
	print(filename,"completed!")

    # savedStdout = sys.stdout #保存标准输出流
    # filename="datatopython6.dat"
    # outfile="out-matrixmethod"+filename
    # file=open(outfile,'w+')
    # sys.stdout = file #标准输出重定向至文件
    # print(filename,"started!")
    # TestLargeJigsaw(filename)
    # sys.stdout = savedStdout #恢复标准输出流
    # file.close()
    # print(filename,"completed!")
    
    # savedStdout = sys.stdout #保存标准输出流
    # filename="datatopython7.dat"
    # outfile="out-matrixmethod"+filename
    # file=open(outfile,'w+')
    # sys.stdout = file #标准输出重定向至文件
    # print(filename,"started!")
    # TestLargeJigsaw(filename)
    # sys.stdout = savedStdout #恢复标准输出流
    # file.close()
    # print(filename,"completed!")
    
    # savedStdout = sys.stdout #保存标准输出流
    # filename="datatopython8.dat"
    # outfile="out-matrixmethod"+filename
    # file=open(outfile,'w+')
    # sys.stdout = file #标准输出重定向至文件
    # print(filename,"started!")
    # TestLargeJigsaw(filename)
    # sys.stdout = savedStdout #恢复标准输出流
    # file.close()
    # print(filename,"completed!")
    
    # savedStdout = sys.stdout #保存标准输出流
    # filename="datatopython9.dat"
    # outfile="out-matrixmethod"+filename
    # file=open(outfile,'w+')
    # sys.stdout = file #标准输出重定向至文件
    # print(filename,"started!")
    # TestLargeJigsaw(filename)
    # sys.stdout = savedStdout #恢复标准输出流
    # file.close()
    # print(filename,"completed!")
    
    # savedStdout = sys.stdout #保存标准输出流
    # filename="datatopython10.dat"
    # outfile="out-matrixmethod"+filename
    # file=open(outfile,'w+')
    # sys.stdout = file #标准输出重定向至文件
    # print(filename,"started!")
    # TestLargeJigsaw(filename)
    # sys.stdout = savedStdout #恢复标准输出流
    # file.close()
    # print(filename,"completed!")
    
    
    
    #测试翻转和旋转
    #TestMatrixTransform()
    
    #测试矩阵匹配
    #TestMatchCheck()
    
    #测试简单的匹配
    #TestMatrixMatch()
    #TestMatrixMatcha()
    
    #测试矩阵是否被分为两个部分
    #TestMatrixCheck()
	
    #print("enter a key to continue")
    #tempa=input()
    # TestMatrixMatchb()
	
    # print("enter a key to continue")
    # tempa=input()
    # TestMatrixMatchc()
	
    # print("enter a key to continue")
    # tempa=input()
    # TestMatrixMatchd()
	
    # print("enter a key to continue")
    # tempa=input()
    # TestMatrixMatche()
	
    # print("enter a key to continue")
    # tempa=input()
    # TestMatrixMatchf()
    
    #计算
    #TestLargeJigsaw(filename)
    
    

