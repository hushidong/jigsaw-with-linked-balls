#!/usr/bin/env python3
#_*_coding: utf-8 _*_

"""
基于链码的球链接形状拼图算法
"""

import random
import copy
import json
import math
import time
import sys

def IsInOrDealed(m,i,j):#判断指定位置的box是否是形状的一部分
    #print("i=%d,j=%d" %(i,j))
    if i<0 or i > len(m)-1:#index less than length 
        return 0
    if j<0 or j > len(m[0])-1:
        return 0
    if m[i][j] == 1 :#存在目标信息，且未处理过
        return 1
    elif m[i][j] > 1 :#存在目标信息，但已在递归处理中
        return 2
    else:#不存在目标信息
        return 0
    
def SetChainCodeInnerS(m,i,j,depth,direct):#给出结构化的链码表，可以看到扩展的过程
    """
    4方向链码:          |1
                 2<----|----->0
                       |3
    计算的链码由构成连接形状的box的边所构成。
    当只有一个box时，链码为0,3,2,1
                  __0__
                1|     |3
                  --2--   
    
    当存在多个连接的box时，链码从起点box开始，在不同方向搜索相邻的box进而扩展链码。
    处理的方向包括:
        right，用两个相邻box的边的链码表示方向，即3
        below，用2表示该方向
        left ，用1表示该方向
        above，用0表示该方向
        
    算法基本原理:根据当前box的处理构造递归
        首先根据输入参数direct判断当前要处理的box是否是起点box，或者是递归过程中前一个box在某个方向的相邻box
            direct=3时，表示当前处理box是前一box的右侧相邻box，当前box还需处理0,3,2三个方向是否有相邻box
            direct=2时，表示当前处理box是前一box的下方相邻box，当前box还需处理3,2,1三个方向是否有相邻box
            direct=1时，表示当前处理box是前一box的左侧相邻box，当前box还需处理2,1,0三个方向是否有相邻box
            direct=0时，表示当前处理box是前一box的上方相邻box，当前box还需处理1,0,3三个方向是否有相邻box
            direct=else时，表示当前处理box是起点box，需要处理0,3,2,1四个方向是否有相邻box
        构造当前处理单元需要返回的链码列表为空
        接着遍历所有需要处理的方向k
            利用IsInOrDealed判断k方向是否存在相邻box，
                如果存在且未处理过，则进行递归调用处理该相邻单元并保存返回的链码;
                如果存在但已处理过，则不做任何事情，直接pass;
                否则保存链码为k.
        最后返回保存的链码列表
    """
    #print("i=%d,j=%d,depth=%d" %(i,j,depth))
    if direct==3:#right
        directstodeal=[0,3,2]
    elif direct==2:#below
        directstodeal=[3,2,1]
    elif direct==1:#left
        directstodeal=[2,1,0]
    elif direct==0:#above
        directstodeal=[1,0,3]
    else:
        directstodeal=[0,3,2,1]
        
    m[i][j]=2#表示当前box已经在递归处理中了
    chaincodelist=[]
  
    for k in directstodeal:
        if k==3:
            a=i
            b=j+1
        elif k==2:
            a=i+1
            b=j
        elif k==1:
            a=i
            b=j-1
        elif k==0:
            a=i-1
            b=j
        flag=IsInOrDealed(m,a,b)
        #print("Matrix=",m)
        #print("k=%d,i=%d,j=%d,flag=%d" %(k,a,b,flag))
        #print("input a key to continue:")
        #vtemp=input()
        if flag==1:
            chaincodelist.append(SetChainCodeInnerS(m,a,b,depth+1,k))
        elif flag==0:#用append,extend均可，append可以看到结构，而extend得到最后的链码
            chaincodelist.append(k)
        else:
            pass
        print("depth=",depth," code=",chaincodelist)
                
    return chaincodelist

def SetChainCodeS(ma,iin,jin,depth,direct):
    #m=ma[:]#因为内部还有列表，所以仍然是浅复制
    m=copy.deepcopy(ma)#深复制避免改变原矩阵
    i=iin
    j=jin
    if m[i][j]==0:#起点做预处理，避免出错
        #print("start box is wrong,change it autumatically!")
        for i in range(len(m)):
            flagout=0
            for j in range(len(m[0])):
                if m[i][j]==1:
                    flagout=1
                    break
            if flagout:
                break
    res=SetChainCodeInnerS(m,i,j,depth,direct)
    return res

def SetChainCode(ma,iin,jin,depth,direct):
    #m=ma[:]#因为内部还有列表，所以仍然是浅复制
    m=copy.deepcopy(ma)#深复制避免改变原矩阵
    i=iin
    j=jin
    if m[i][j]==0:#起点做预处理，避免出错
        #print("start box is wrong,change it autumatically!")
        flagout=0
        for i in range(len(m)):
            for j in range(len(m[0])):
                if m[i][j]==1:
                    flagout=1
                    break
            if flagout:
                break
    res=SetChainCodeInner(m,i,j,depth,direct)
    return res

def SetChainCodeInner(m,i,j,depth,direct):#给出最后的链码
    """
    注意:递归就是要维护一个相同的矩阵才能保证正确判断处理过的box
    """
    if direct==3:#right
        directstodeal=[0,3,2]
    elif direct==2:#below
        directstodeal=[3,2,1]
    elif direct==1:#left
        directstodeal=[2,1,0]
    elif direct==0:#above
        directstodeal=[1,0,3]
    else:
        directstodeal=[0,3,2,1]
  
    m[i][j]=2#表示当前box已经在递归处理中
    chaincodelist=[]
  
    for k in directstodeal:
        if k==3:
            a=i
            b=j+1
        elif k==2:
            a=i+1
            b=j
        elif k==1:
            a=i
            b=j-1
        elif k==0:
            a=i-1
            b=j
        flag=IsInOrDealed(m,a,b)
        if flag==1:
            chaincodelist.extend(SetChainCodeInner(m,a,b,depth+1,k))
        elif flag==0:#用append,extend均可，append可以看到结构，而extend得到最后的链码
            chaincodelist.extend([k])
        else:
            pass
    #print("chain code of boundary=",chaincodelist)
    return chaincodelist

def MatchChainCode(codea,codeb):
    """
    codea待匹配长链
    codeb要匹配短链
    """
    #print("")
    #print("src codea=",codea)
    #print("tmc codeb=",codeb)
    savedmaxcount=0 #起点变换后，匹配数量可能相同，相同的情况记录下，该变量记录相同的情况数
    savedstartptk=[]#匹配数量相同情况的起点记录
    savedidxlista=[]#匹配数量相同情况的长链中匹配链码的索引记录
    savedidxlistb=[]#匹配数量相同情况的短链中匹配链码的索引记录
    
    lensa=len(codea)
    lensb=len(codeb)
    for k in range(lensa):
        samecount=0
        samelista=[]
        samelistb=[]
        j=0
        start=k
        for i in range(lensb):#在codeb中找匹配当前codea中的链码的位置
            if codea[k]==codeb[i]:
                samecount+=1;
                samelista.append(k)
                samelistb.append(i)
                j=i
                break
        #print("compare idx:")
        #print("k=",k,"j=",j)
        
        matched=0
        for i in range(1,lensb):
            if k+i>lensa-1:
                l=k+i-lensa#循环的匹配，超出范围后从索引0开始匹配
            else:
                l=k+i
            if j+i>lensb-1:
                m=j+i-lensb
            else:
                m=j+i  
            if codea[l]==codeb[m]:
                #print("l=",l,"m=",m,"ac")
                samecount+=1;
                samelista.append(l)
                samelistb.append(m)
                if samecount==lensb:
                    matched=lensb-1
            else:
                matched=i-1#记录索引增大方向匹配了多少位
                break
        #print("matched idx num=",matched+1)
        #print("rest    idx num=",len(codeb)-matched-1)
        #索引增大方向,匹配了matched+1位，包括起点自身，那么
        #索引减小方向,最大的匹配数量就是:len(codeb)-(matched+1)
        for i in range(1,lensb-matched):
            if k-i<0:
                l=lensa+k-i#循环的匹配，超出范围后从索引负值开始匹配
            else:
                l=k-i
            if j-i<0:
                m=lensb+j-i
            else:
                m=j-i
            if codea[l]==codeb[m]:
                #print("l=",l,"m=",m,"dc")
                start=l
                samecount+=1;
                samelista.insert(0,l)
                samelistb.insert(0,m)
            else:                
                break     
        #print('number of same code=%d,k=%d,start=%d' %(samecount,k,start))
        if samecount>savedmaxcount:#做记录
            savedmaxcount=samecount
            savedstartptk=[start]
            savedidxlista=[samelista]
            savedidxlistb=[samelistb]
        elif samecount==savedmaxcount and start not in savedstartptk:
            savedstartptk.append(start)
            savedidxlista.append(samelista)
            savedidxlistb.append(samelistb)
            
    #print("matched,start idx in codea, saved k:",savedstartptk)#记录匹配的信息
    #print("matched,samecode number saved count:",savedmaxcount)
    #print("matched,codeidx in codea saved list",savedidxlista)
    #print("matched,codeidx in codeb saved list",savedidxlistb)
    
    
    #fa=lambda idx : lensa+idx if idx<0 else idx #lambda 函数将负的索引值换成正的
    #fb=lambda idx : lensb+idx if idx<0 else idx
    randi=random.randrange(len(savedstartptk))
    #print("choose random list to match real number= idx+1 :",randi+1)
    #idxlista=[fa(x) for x in savedidxlista[randi]]
    #idxlistb=[fb(x) for x in savedidxlistb[randi]]
    idxlista=savedidxlista[randi] #前面取得索引均已经大于0所以，不要再用lambda函数做处理了。
    idxlistb=savedidxlistb[randi]
    #print(idxlista)
    #print(idxlistb)
    #print("待匹配链码中匹配链段的索引列表:",idxlista)
    #print("要匹配链码中匹配链段的索引列表:",idxlistb)

    
    #取消a链中匹配的链码，留下未匹配的链码
    # codec=[]
    # for i in range(lensa):
        # if i in idxlista:
            # pass
        # else:
            # codec.append(codea[i])
    codec=[codea[i] for i in range(lensa) if i not in idxlista]
    #print("matched,code left in codea    list:",codec)
    #print("待匹配链码中剩余链码:",codec)
    
    #取出要插入的剩下的b链,起点是匹配链码首位的前一个
    #要重点注意:B链的插入顺序和起点正确与否也很关键
    #如果原链码是从左到右表示正顺序，那么插入应是反方向，从右到左
    #同时插入起点必须是匹配段前的一个链码开始:
    coded=[]
    istposb=idxlistb[0]-1#起点是匹配链前一位，然后反向获取剩余链码
    for i in range(lensb):
        restidx=istposb-i
        if restidx<0:
            restidx=lensb+restidx
        if restidx in idxlistb:
            break
        else:#未匹配部分方向相反，即0和2互相变换,1和3互相变换
            coded.append(codeb[restidx]%2+(2+codeb[restidx]%2-codeb[restidx]))
    #print("matched,code left in codeb inversed",coded)
    #print("待匹配链码中剩余链码反向:",coded)
    
    #对匹配进行判断，如果要匹配链剩下的代码不合理，那么说明匹配失败
    #比如:剩下[2,1,3]，显然1后面不可能接3，所以匹配失败:
    if len(coded)>0:
        if not CheckLeftCode(coded):
            #print("chain code direction wrong")
            #print("match failed!!!")
            return [False] 

    #将链码b中留下的链码加入到链码a中
    #确定未匹配链码的插入位置:
    #插入的位置应是在codea中匹配链码的最小索引位置
    istposa=lensa
    for i in idxlista:
        if(i<istposa):
            istposa=i
    #print("insert pos=",istposa)
    coderes=codec
    for i in range(len(coded)):
        coderes.insert(istposa+i,coded[i])
        
    if len(coderes)==0:#当匹配完成后直接返回了
        #print("all matched, good job!!!")
        return [True,coderes,idxlista[0],idxlistb[0],istposa]
    
    if not istposa:#当插入点是索引0时，剩余链码的起点已经移到匹配链段前一个链码上，
       item= coderes.pop() #将该码移到最前面确保其对应box做为剩余链码矩阵的起点
       coderes.insert(0,item)
    #print("rest codes after match:",coderes)
    
    #对匹配剩余的链码进行判断，如果不合理，那么说明匹配失败
    #一种不合理情况，构成循环一个box:
    if CheckCodeSkew(coderes):
        #print("chain code twisted")
        #print("match failed!!!")
        return [False]
        
    #不合理情况实际较多，比如因为匹配把剩余拼图分成两个部分
    #但是因为这里的链码仅考虑一个，所以分成两部分的情况可能带来问题
    #因此这里不考虑分成两个部分的情况，直接检测并排除
    #排除方法由两种:
    #1是链码转矩阵然后再转回链码，如果不相同那么就需要排除
    #2是链码中的数据一对02或13之间，不能有成对的13或02，存在则需排除，比如
    #box:(0,0)，(1,0)，(1,2)，(1,3)这样的情况实际上是两个部分了，
    #如果用一个链码表示，那么接下来的匹配就会存在问题
    #这里采用第一种方法
    if len(coderes)>0:
        mres=MatrixFromChainCodeM(coderes,0)
        #print("box-id  from rest code:",mres)
        mres1=DisplayMatrixBDS(mres[0],1)
        #print("mat bd  from rest code:",mres1)
        mres2=DisplayMatrixAllS(mres1[0],1) #加入辅助单元后不需要再做中间单元判断了。
        #print("mat all from rest code:",mres2)
        coderes1=SetChainCode(mres2,0,0,0,5)
        #coderes1=SetChainCode(mres1[0],0,0,0,5)
        #print("regen-code from matrix:",coderes1)
        if not CheckCodeSame(coderes,coderes1):
            #print("regenerate code not equal")
            #print("match failed!!!")
            return [False]
        
    if len(coderes)> lensa:
        #print("match failed!!!")
        return [False]   
    else:
        #print("合成新的链码为:",coderes," 剩余链码插入位置为:",istposa)
        return [True,coderes,idxlista[0],idxlistb[0],istposa]
    
def CheckLeftCode(codeb):#检查链码是否正确,是否存在相反方向连续的情况。
    for i in range(len(codeb)-1):
        if codeb[i]%2==0:#偶数情况，0,2
            if codeb[i]+codeb[i+1]==2:
                return False #0后面不能跟2,2后面不能跟0
        else:#奇数情况，1,3
            if codeb[i]+codeb[i+1]==4:
                return False
    return True

def CheckCodeSkew(codeb):#检查链码是否有扭曲的，比如构成了一个box通常是扭曲的
    length=len(codeb)
    if length>=4:
        for k in range(length):
            # codea=[] #用下面3句代替
            # for i in range(4):
                # j=k+i
                # if j>length-1:
                    # j=j-length
                # codea.append(codeb[j])
            codea=codeb[k:k+4]
            if k+4>length:
                codea.extend(codeb[0:k+4-length])
            
            if codea==[0,3,2,1] or codea==[1,0,3,2] or codea==[2,1,0,3] or codea==[3,2,1,0]:
                return True

            # if codea[0]==0:
                # if codea==[0,3,2,1]:
                    # return True
            # elif codea[0]==1:
                # if codea==[1,0,3,2]:
                    # return True
            # elif codea[0]==2:
                # if codea==[2,1,0,3]:
                    # return True
            # elif codea[0]==3:
                # if codea==[3,2,1,0]:
                    # return True
    return False
    

def CheckCodeSame(codea,codeb):#检查两个链码是否一致，起点可以不同，即需要循环判断
    #codea=codec[:]
    #codeb=coded[:]
    lensa=len(codea)
    lensb=len(codeb)
    if not lensa==lensb:#链长不一致那么必然不同
        return False
    if not sum(codea)==sum(codeb):#如果链码值相加不等，那么必然不同
        return False
    for k in range(lensa):#做循环匹配判断
        samecount=0
        j=0
        for i in range(lensb):#在codeb中找匹配当前codea中的链码的位置
            if codea[k]==codeb[i]:
                samecount+=1;
                j=i
                break
        #print("compare idx:")
        #print("k=",k,"j=",j)
        
        matched=0
        for i in range(1,lensb):
            if k+i>lensa-1:
                l=k+i-lensa#循环的匹配，超出范围后从索引0开始匹配
            else:
                l=k+i
            if j+i>lensb-1:
                m=j+i-lensb
            else:
                m=j+i  
            if codea[l]==codeb[m]:
                #print("l=",l,"m=",m,"ac")
                samecount+=1;
                if samecount==lensb:
                    return True
            else:
                matched=i-1#记录索引增大方向匹配了多少位
                break
        #print("matched idx num=",matched+1)
        #print("rest    idx num=",len(codeb)-matched-1)
        #索引增大方向,匹配了matched+1位，包括起点自身，那么
        #索引减小方向,最大的匹配数量就是:len(codeb)-(matched+1)
        for i in range(1,len(codeb)-matched):
            if k-i<0:
                l=lensa+k-i#循环的匹配，超出范围后从索引0开始匹配
            else:
                l=k-i
            if j-i<0:
                m=lensb+j-i
            else:
                m=j-i
            if codea[l]==codeb[m]:
                #print("l=",l,"m=",m,"dc")
                samecount+=1;
                if samecount==lensb:
                    return True
            else:                
                break  
    return False
    
    
    
def MatrixTransformation(codeb,ptshift,mirror,rotation):
    """
    四个输入参数分别是:
        原始链码，
        起点前移的链码数，=0表示起点不变，=1表示起点前移一个链码
        是否做翻转(镜像)，=0表示不做翻转，=1表示做上下翻转，=2表示做左右翻转
        作逆时针旋转90度的次数，=0表示不旋转，=1表示逆时针旋转90度，=2表示180度，=3表示270度
    """
    #print('orig chaincode=',codeb)
    #strlist=["no mirror","up-down mirror","left-right mirror"]
    #print("startpoint shift forward %d codes, do %s, anticlockwise rotate %d degree" %(ptshift,strlist[mirror],rotation*90))
    
    #首先做起点前移
    if(ptshift<len(codeb)):#移动长度小于整个链码长度，那么直接把后面的ptshift位移动最前面
        shift=-ptshift
        codeshift=codeb[shift:]
    else:#移动长度大于整个链码长度，那么实际移动的是len(codeb)-ptshift位
        shift=len(codeb)-ptshift
        codeshift=codeb[shift:]
    codeshift.extend(codeb[:shift])
    #print("shifted code=",codeshift)
        
    #接着做翻转
    if mirror==0:
        coded=codeshift #直接引用codeshift,#注意赋值和复制的差异
    elif mirror==1:
        codeshift.reverse()
        coded=[x%2*x+(1-x%2)*(2-x) for x in codeshift]#上下翻转，0和2相互交换，1和3不变
    elif mirror==2:
        codeshift.reverse()
        coded=[(1-x%2)*x+(x%2)*(4-x) for x in codeshift]#左右翻转，0和2不变，1和3相互交换
        
    #接着根据旋转角度做旋转
    codediff=CodeToDiffcode(coded)
    #print('diff chaincode=',codediff)
    if rotation==0:#新方向与原链起始方向相差0，逆时针旋转0度，等于不旋转
        #print('tran chaincode=',coded)
        return coded
    elif rotation==1:
        direct=(coded[0]+1)%4#新方向与原链起始方向相差1，逆时针旋转90度，等于顺时针旋转270度
        codec=DiffcodeToCode(codediff,direct)
        #print('tran chaincode=',codec)
    elif rotation==2:
        direct=(coded[0]+2)%4#新方向与原链起始方向相差2，逆时针旋转180度，等于顺时针旋转180度
        codec=DiffcodeToCode(codediff,direct)
        #print('tran chaincode=',codec)
    elif rotation==3:
        direct=(coded[0]+3)%4#新方向与原链起始方向相差3，逆时针旋转270度，等于顺时针旋转90度
        codec=DiffcodeToCode(codediff,direct)
        #print('tran chaincode=',codec)

    return codec


def DiffcodeToCode(codediff,direct):#差分链到链码
    """
    #direct 表示起始链码的方向
    """
    length=len(codediff)
    coderes=[direct]
    code=direct #第一个链码方向
    for i in range(1,length):
        code=(code+codediff[i])%4 #逆时针方向加上差值后，取对4的余数就是新方向
        coderes.append(code)
    return coderes
    

def CodeToDiffcode(codeb):#链码到差分链
    length=len(codeb)
    coderes=[]
    for i in range(length):
        #coderes.append(DiffofFourDirect(codeb[i-1],codeb[i]))
        code=(codeb[i]-codeb[i-1]+4)%4
        coderes.append(code)
    return coderes
   


def DisplayMatrixAlpha(mc):
    rows=len(mc)
    cols=len(mc[0])
    setval="ABCDEFGHIJKLMNOPQRST"
    print("  |",end="")
    for j in range(cols):
        print("%2s"%(j),end="")
    print(" |")
    print("--|",end="")
    for j in range(cols):
        print("%2s"%("--"),end="")
    print(" |--")
    for i in range(rows):
        print("%2d|"%(i),end="")
        for j in range(cols):
            if mc[i][j]>=1:
                print("%2s"%(setval[mc[i][j]-1]),end="")
            else:
                #pass
                #print("%2s"%(str(mc[i][j])),end="")
                print("  ",end="")
        print(" |%2d"%(i))
    print("--|",end="")
    for j in range(cols):
        print("%2s"%("--"),end="")
    print(" |--")
    print("  |",end="")
    for j in range(cols):
        print("%2s"%(j),end="")
    print(" |")

 
   
def DisplayMatrix(boxmatrix):
    rows=len(boxmatrix)
    cols=len(boxmatrix[0])
    
    #print("matirx list:")
    print("显示矩阵:")
    for row in range(rows):
        for col in range(cols):
            print(" %2s" %(str(boxmatrix[row][col])),end='')
        print("")
    return None

def CheckInnerDirect(matrixbd,row,col,drow,dcol,rows,cols):
	#判断某个方向上是否在边界内
    while row<rows and row>=0 and col<cols and col>=0:
        if matrixbd[row][col]==0:#当前方形为0时表示当前box不属于形状，并检查某个方向的单元是否也是0
            row=row+drow
            col=col+dcol
        else:#当遇到是1表示在该方向上，边界是1，那么在该方向上输入的row，col方形是在内部
            return True
    return False

def DisplayMatrixAllS(matrixbd,setval):#边界内部可能还有空格，找出并设置为1
    boxmatrix=copy.deepcopy(matrixbd)
    #print("boxmatrix=",boxmatrix)
    rows=len(boxmatrix)
    cols=len(boxmatrix[0])
    #print(rows,cols)
    for i in range(1,rows-1):#注意range的stop的用法
        for j in range(1,cols-1):
            if(boxmatrix[i][j]==0):
                flag=[CheckInnerDirect(boxmatrix,i,j,-1,0,rows,cols)
                and CheckInnerDirect(boxmatrix,i,j,1,0,rows,cols) 
                and CheckInnerDirect(boxmatrix,i,j,0,-1,rows,cols)
                and CheckInnerDirect(boxmatrix,i,j,0,+1,rows,cols)]
                #print("flag=",flag[0])
                if flag[0]:
                    boxmatrix[i][j]=setval
    return boxmatrix

def DisplayMatrixBDS(ijlist,setval):#ijlist is the i and j info of the matrix
    #print(ijlist)
    imin=100000
    jmin=100000
    imax=-100000
    jmax=-100000
    nbox=len(ijlist)
    for k in range(nbox):
        if imin>ijlist[k][0]:
            imin=ijlist[k][0]
        if jmin>ijlist[k][1]:
            jmin=ijlist[k][1]
        if imax<ijlist[k][0]:
            imax=ijlist[k][0]
        if jmax<ijlist[k][1]:
            jmax=ijlist[k][1]
    rows=imax-imin+1
    cols=jmax-jmin+1
    
    #处理使得最小的行列号为0
    for k in range(nbox):
        ijlist[k][0]-=imin

    for k in range(nbox):
        ijlist[k][1]-=jmin
    
    #先给出一个rows*cols的矩阵
    # boxmatrix=[]
    # for row in range(rows):
        # matrixrow=[]
        # for col in range(cols):
            # matrixrow.append(0)
        # boxmatrix.append(matrixrow)
    boxmatrix=[[0 for col in range(cols)] for row in range(rows)]
    #print("boxmatrix=",boxmatrix)
        
    for k in range(nbox):
        i=ijlist[k][0]
        j=ijlist[k][1]
        boxmatrix[i][j]=setval
    #print("boxmatrix=",boxmatrix)
    return [boxmatrix,imin,jmin]
     

def MatchProcess(ma,mbs):
    """
    参数:
        ma:被匹配的大矩阵
        mbs:要匹配的多个小矩阵
    
    显示矩阵:mdpl:display
    原始(初)矩阵:morg:origin
    被(待)匹配矩阵:msrc:source
    要匹配矩阵:mtmc:to match
    
    对于某个box:
    初矩阵与显示矩阵之间差imin和jmin，idpl=iorg-imin
    被匹配矩阵与初矩阵之间有匹配起点的对应关系:
        iorg=isrc-isrc0+iorg0
    要匹配矩阵与被匹配矩阵之间有匹配起点的对应关系:
        isrc=itmc-itmc1+isrc1
    
    """
    flagsuccess=0
    k=0
    # countmatch=[]
    # countchoose=[]
    countmatch=0
    countchoose=0
    choosesum=0
    matchsum=0
    lenmbs=len(mbs)
    while flagsuccess==0:#k<20 and 
        k=k+1
        #print("\n")
        #print("-----start to match,time sn=%d------"%k)
        #print("---开始第%d次拼图----"%k)
        c=SetChainCode(ma,0,0,0,5)    
        #print("ma=",ma)
        #print("chain code of matrix a boundary=",c)
        #print("网格矩阵为:",ma)
        #print("网格链码为:",c)
        
        #显示处理
        # 一种显示方式
        # res=MatrixFromChainCodeM(c,0)#链码对应初矩阵计算
        # morg=res[0]#初矩阵
        # res=DisplayMatrixBDS(morg,"m")#用于全局显示的矩阵
        # imin=res[1]#初矩阵中的ij最小值，因为可能是负的，但显示矩阵已经处理为0
        # jmin=res[2]
        # res=DisplayMatrixAllS(res[0],"m")#用于全局显示的矩阵
        # mdpl=res#显示矩阵
        # DisplayMatrix(mdpl)
        
        #另一种显示方式
        mdpl=copy.deepcopy(ma)
        #DisplayMatrix(mdpl)
        imin=0
        jmin=0
        iorg0=0 #被匹配矩阵起点在初矩阵中的ij位置
        jorg0=0
        #print("待匹配矩阵起点在初矩阵中的ij位置:[%d,%d]"%(iorg0,jorg0))
        
        
        dealed=[]#用于记录已经匹配完的小矩阵的索引号
        counta=0 #用于统计形状选择次数
        countb=0 #用于统计形状匹配次数
        countc=0 #用于剩下一个形状时的退出判断
        lasttwo={}
        undealed=[]
        countd=0 #用于剩下两个形状时的退出判断
        oldi=0
        while len(dealed)<lenmbs and counta<lenmbs*2:

            if lenmbs==len(dealed)+1:#剩下一个形状的时候countc计数，当次数大于1时，即可以退出了
                countc+=1              #因为已经做过一遍尝试已经不行，无需再匹配了。
            if countc > 1:
                break
            
            i=random.randrange(lenmbs)#随机找一个未匹配的codeb
            while i in dealed or i==oldi:#当随机选择的i已经处理过，或和前一次的选择相同，则重新选择
                i=random.randrange(lenmbs)#但当只剩一个选择的时候，这里会导致死循环，但前面已经通过统计处理掉。
            oldi=i
            
            # if lenmbs==len(dealed)+2:#剩下两个的时候，如果两个都已经做过一遍，那么就可以退出了
                # undealed=[x for x in range(lenmbs) if x not in dealed]
            # if i in undealed:
                # countd+=1
            # if countd>2:
                # break
                
            # if lenmbs==len(dealed)+2:
                # if i in lasttwo and len(lasttwo)==2:
                    # break
                # else:
                    # lasttwo.add(i)
                
            if len(dealed)==lenmbs-2:
                if i not in undealed:
                    undealed.append(i)
                else:
                    if len(undealed)==2:
                        break
            
            counta+=1
            d=SetChainCode(mbs[i],0,0,0,5)
            #print(" ")
            #print("--b[%d]--"%(i))
            #print("mb=",mbs[i])
            #print("chain code of matrix b boundary=",d)
            # print("")
            # print("---选择一个形状开始匹配----")
            # print("待匹配形状链码为:",c)
            # print("要匹配形状索引为:",i)
            # print("要匹配形状为:",mbs[i])
            # print("要匹配形状链码为:",d)
            
            for transtimes in range(8):#变换加原链码总共8中变化
                if transtimes%8:#首先3次旋转，翻转后再做3次旋转
                    #print("")
                    #print("match failed,do transformation")
                    #print("")
                    #print("形状匹配失败，做一次变换")
                    dtrans=MatrixTransformation(d,0,transtimes//4,transtimes%4)
                    #print("要匹配形状，变换后链码为:",dtrans)
                else:
                    dtrans=d
                e=MatchChainCode(c,dtrans)
                countb+=1
                
                if e[0]:
                    dealed.append(i)
                    msrc=MatrixFromChainCodeM(c,e[2])
                    mtmc=MatrixFromChainCodeM(dtrans,e[3])
                    istpos=e[4]
                    #print("match result=",e)
                    #print("matrix:src:",msrc)
                    #print("matrix:tmc:",mtmc)
                    # print("")
                    # print("匹配是否成功？",e[0])
                    # print("匹配后剩余链码为:",e[1])
                    # print("待匹配链码中匹配链段第一个码索引是:",e[2])
                    # print("要匹配链码中匹配链段第一个码索引是:",e[3])
                    # print("待匹配链码中插入点位置索引是:",e[4])
                    # print("待匹配链码转成各box坐标为:",msrc[0])
                    # print("待匹配链码第一个匹配码对应box的索引为:%d，坐标为:%s"%(msrc[1],str(msrc[0][msrc[1]])))
                    # print("待匹配链码第一个匹配码前一个码对应box的索引为:%d，坐标为:%s"%(msrc[2],str(msrc[0][msrc[2]])))
                    # print("要匹配链码转成各box坐标为",mtmc[0])
                    # print("要匹配链码第一个匹配码对应box的索引为%d，坐标为%s"%(mtmc[1],str(mtmc[0][mtmc[1]])))
                    # print("要匹配链码第一个匹配码前一个码对应box的索引为%d，坐标为%s"%(mtmc[2],str(mtmc[0][mtmc[2]])))
                    
                    
                    c=e[1]#更新待匹配链码
                    
                    #显示处理
                    #print("待匹配矩阵自身起点在初矩阵中的坐标为:[%d,%d]"%(iorg0,jorg0))
                    ijsrc=msrc[0][0]#被匹配矩阵中自身起点的i，j号，起点总是链码第一个码对应的box，因为插入点为0时也已经将a链剩余链码的最后一个码移到最前面
                    isrc0=ijsrc[0]
                    jsrc0=ijsrc[1]
                    #print("ijsrc0",ijsrc)
                    #print("待匹配链码矩阵的自身起点坐标为:%s"%(str(ijsrc)))
                    ijsrc=msrc[0][msrc[1]]#被匹配矩阵中匹配起点box的ij号       
                    isrc1=ijsrc[0]  
                    jsrc1=ijsrc[1]
                    #print("ijsrc1",ijsrc)
                    #print("待匹配链码矩阵的匹配起点坐标为:%s"%(str(ijsrc)))
                    ijtmc=mtmc[0][mtmc[1]]#要匹配矩阵中匹配起点box的ij号
                    itmc1=ijtmc[0]
                    jtmc1=ijtmc[1]
                    #print("ijtmc1",ijtmc)
                    #print("要匹配链码矩阵的匹配起点坐标为:%s"%(str(ijtmc)))
                    #print("ijorg0",[iorg0,jorg0])#被匹配矩阵起点在初矩阵中的ij位置
                    #print("ijmin",[imin,jmin])#初矩阵与显示矩阵的ij差
                    for ijtmc in mtmc[0]:
                        itmc=ijtmc[0]
                        jtmc=ijtmc[1]
                        idpl=itmc-itmc1+isrc1-isrc0+iorg0-imin
                        jdpl=jtmc-jtmc1+jsrc1-jsrc0+jorg0-jmin
                        mdpl[idpl][jdpl]=i+1#显示的是索引号加1
                    #DisplayMatrix(mdpl)

                    #剩余链码插入起点为0，表示剩下的链码的起点，已经不同于初链码的起点，需要做处理
                    if not istpos:
                        ijsrc=msrc[0][msrc[2]]#被匹配矩阵中匹配起点前一个box的i，j号,就是下一次的起点
                        isrc=ijsrc[0]
                        jsrc=ijsrc[1]
                        #剩余矩阵也就是下一次的被匹配矩阵的起点，
                        #为这次的匹配起点前一个box在初矩阵中的ij号
                        #print("待匹配链码矩阵的自身起点坐标为ijsrc0:[%d,%d]"%(isrc0,jsrc0))
                        #print("该旧起点对应在初矩阵中的坐标为ijorg0:[%d,%d]"%(iorg0,jorg0))
                        iorg0=isrc-isrc0+iorg0
                        jorg0=jsrc-jsrc0+jorg0
                        #print("待匹配链码剩余矩阵的起点坐标为ijsrc:[%d,%d]"%(isrc,jsrc))
                        #print("该新起点对应在初矩阵中的坐标为ijorg0:[%d,%d]"%(iorg0,jorg0))
                    if not len(c):
                        flagsuccess=1
                    break
            #print ("len(dealed)=",len(dealed),"len(mbs)=",len(mbs))
            #print("匹配完毕的形状数为:",len(dealed),"形状总数为:",len(mbs))
        # countchoose.append(counta)
        # countmatch.append(countb)
        countchoose=counta
        countmatch=countb
        choosesum+=counta
        matchsum+=countb
        #print("第%d次拼图，形状随机选择次数为countchoose[%d]=%d"%(k,k,counta))
        #print("第%d次拼图，形状匹配的总次数为countchoose[%d]=%d"%(k,k,countb))
    #DisplayMatrix(mdpl)
    DisplayMatrixAlpha(mdpl)
    print("拼图次数n=",k)
    #print("形状选择次数:",countchoose)
    #print("形状匹配次数:",countmatch)
    #choosesum=sum(countchoose)
    #matchsum=sum(countmatch)
    print("形状选择总次数:",choosesum)
    print("形状匹配总次数:",matchsum)
    #return [countchoose[-1],choosesum,countmatch[-1],matchsum,k]
    return [countchoose,choosesum,countmatch,matchsum,k]
            

def CheckDirectM(precode,poscode):#参数为前一个box的最后一个链码和后一个box的第一个链码
    #print(precode,poscode)
    di=0
    dj=0
    dia=0#两个box之间补充的连接box
    dja=0
    if precode==0:
        if poscode==1:
            di=-1
            dj=1
            dia=0
            dja=1
        elif poscode==0:
            di=0
            dj=1
    elif precode==3:
        if poscode==0:
            di=1
            dj=1
            dia=1
            dja=0
        elif poscode==3:
            di=1
            dj=0
    elif precode==2:
        if poscode==3:
            di=1
            dj=-1
            dia=0
            dja=-1
        elif poscode==2:
            di=0
            dj=-1
    elif precode==1:
        if poscode==2:
            di=-1
            dj=-1
            dia=-1
            dja=0
        elif poscode==1:
            di=-1
            dj=0
    #print(di,dj)
    return [di,dj,dia,dja]
    
def MatrixFromChainCodeM(codea,idxforboxid):
    """
    参数:
        codea:输入的链码
        idxforboxid:指定code的idx，用于确定该code对应的box

        输出:
        各链码段对应的box的坐标，插入点链码对应的box的索引，和前一个box的索引
        
    形状矩阵方向行增加为正方向，列增加为正方向
    比较序列:描述一个box的链码是有规律的，因此从比较序列来进行比较
    """
    #根据链码数据确定有多少个box转换(边的方向转折)，以及包围该box的链码
    codeb=[0,3,2,1,0,3,2,1,0,3,2]#比较序列，用于判断方向转折
    boxnm=1#转折所确定的box的数量，有链码必然有一个box，设置起点为1
    start=codeb.index(codea[0])#找第一个链码的在比较序列中的位置
    boundary=0 #一个box中的边的序号
    
    boxid=0  #预设一个给定idxforboxid对应的boxid，索引
    boxidm=-1#注意idxforboxid前一个码对应的box可能是-1，就是在链码末尾的码对应的box
    
    boxcode=[]#每个box对应的码的列表
    boxcodelist=[]#所有box对应的码列表构成的列表
    for i in range(len(codea)):
        x=codea[i]
        if x==codeb[start+boundary]:
            boxcode.append(x)
            boundary+=1
        else:
            boxnm+=1
            boxcodelist.append(boxcode)
                       
            start=codeb.index(x)
            boundary=1#新的一个box的第一个码
            boxcode=[x]
        if idxforboxid==i:#确定输入的边的码对应的边界box的序号-从0开始计算
            boxid=boxnm-1
        if (idxforboxid-1)==i:#确定输入的边的前一个码对应的边界box的序号-从0开始计数
            boxidm=boxnm-1    #当idxforboxid=0时，这个判断无结果，那么boxidm=前面预设的-1，即最后一个box
                              #当idxforboxid=0时，boxid=0即对应的是第一个box，那么是否最后一个box与第一个box
                              #会是同一个box？从实践看是不太可能，因为匹配的链码必然是属于同一box，因此当
                              #第一个链码和最后一个码是同一个box时，匹配时，插入点不会是0而会是最后一个码
    
    #处理最后一段链码        
    boxcodelist.append(boxcode)
    #注意:根据边的转折确定的box可能会大于实际的边界的box数，因为会有重复
    #print('boxnm=',boxnm)
    #print('boxid=',boxid,"boxidm=",boxidm)
    #print('boundary boxcodelist=',boxcodelist)
    
    i=0
    j=0
    ijofmatrix=[[i,j]]#设置第一个box对应的坐标为(0,0)
    boxrealsn=0#边界加补充box的序号,是索引从0开始计数
    if boxid==0:
        boxidx=boxrealsn
    if boxidm==0:
        boxidxm=boxrealsn
    if boxidm==-1:
        boxidxm=-1

    for k in range(1,boxnm):
        #print(boxcodelist[k-1][-1],boxcodelist[k][0])
        didj=CheckDirectM(boxcodelist[k-1][-1],boxcodelist[k][0])
        if(abs(didj[2]+didj[3])>0):#把过渡的box加入进去，当box行列同时增加时，需要增加一个过渡的box来保证box的邻接
            ia=i+didj[2]
            ja=j+didj[3]
            boxrealsn+=1
            ijofmatrix.append([ia,ja])
        i=i+didj[0]
        j=j+didj[1]
        boxrealsn+=1
        ijofmatrix.append([i,j])
        if boxid==k:
            boxidx=boxrealsn
        if boxidm==k:
            boxidxm=boxrealsn
    
    return [ijofmatrix,boxidx,boxidxm]#注意:输出的box号是索引号

def TestChainCodeGeneration():
    mat = [#形状矩阵
     [1, 0, 0,0],
     [1, 1, 0,0],
     [0, 0, 0,0],
     [0, 0, 0,0]]

    mat = [#形状矩阵
     [1, 1, 0,0],
     [1, 1, 1,0],
     [1, 1, 1,0],
     [0, 1, 0,0]]
    
    mat = [#形状矩阵
     [0, 1, 0,0],
     [1, 0, 1,0],
     [0, 1, 0,0],
     [0, 0, 0,0]]
    
    print("")
    print("-------test case1:------------")
    print("box 不是完全邻接的情况")
    print("matrix list=",mat)
    DisplayMatrix(mat)
    d=SetChainCode(mat,0,0,0,5)#起点的方向不能是0,1,2,3，只要是其它数即可。
    print("chain code of matrix boundary=",d)
    d=SetChainCode(mat,1,1,0,5)#起点改变
    print("chain code of matrix boundary=",d)
    MatrixFromChainCodeM(d,0)
    
    
    mat=[[0, 1, 0, 0, 0, 0], #从验证看，中间空缺可能会出现问题
         [1, 0, 1, 0, 0, 0], 
         [1, 0, 0, 1, 0, 0], 
         [1, 0, 0, 0, 1, 0], 
         [1, 1, 1, 1, 1, 1]]
    print("")
    print("-------test case2:------------")
    print("box 不是完全邻接的情况")
    d=SetChainCode(mat,0,0,0,5)
    print("chain code of matrix boundary=",d)
    print("box 不是完全邻接的情况，填充完毕变邻接")
    mat1=DisplayMatrixAllS(mat,1)#将矩阵内部空格填充完毕再生成链码
    d=SetChainCode(mat1,0,0,0,5)
    print("chain code of matrix boundary=",d)
        
    mat = [#形状矩阵
     [1, 1, 0,0],
     [1, 0, 1,0],
     [1, 1, 1,0],
     [0, 0, 0,0]]
    print("")
    print("-------test case3:------------")
    print("box 不是完全邻接的情况")
    d=SetChainCode(mat,0,0,0,5)
    print("chain code of matrix boundary=",d)
    d=SetChainCode(mat,0,1,0,5)
    print("chain code of matrix boundary=",d)
    
    mat=[[1,0],[1,0],[1,1]]
    print("")
    print("-------test case4:------------")
    print("结构化的链码，显示出递归的结构")
    d=SetChainCodeS(mat,0,0,0,5)
    print("chain code of matrix boundary=",d)
    d=SetChainCode(mat,0,0,0,5)
    print("chain code of matrix boundary=",d)
    d1=MatrixTransformation(d,0,0,1)
    print("new code after transformation:",d1)
    d1=MatrixTransformation(d,0,1,0)
    print("new code after transformation:",d1)
    d1=MatrixTransformation(d,0,2,0)
    print("new code after transformation:",d1)
    
def TestBoundaryMatrixToCode():
    #当矩阵内部存在空洞，但边界单元也是连续的时，链码的生成
    ma=[[0,  0,  1,  0,  0],
     [0,  1 , 1,  1,  0],
     [1,  1 , 0,  1,  1],
     [0,  1,  1,  1,  0],
     [0,  0,  1,  0,  0]]
    res=SetChainCode(ma,0,0,0,5)
    print(res)
    ma=[[0,  0,  1,  0,  0],
     [0,  1 , 1,  1,  0],
     [1,  1 , 1,  1,  1],
     [0,  1,  1,  1,  0],
     [0,  0,  1,  0,  0]]
    res=SetChainCode(ma,0,0,0,5)
    print(res)  

def TestChainCodeTransformation():
    m3 = [#形状矩阵
     [1, 0, 0,0],
     [1, 0, 0,0],
     [1, 1, 0,0],
     [0, 0, 0,0]]
    
    print("")
    print("-------test case1:------------")
    print("matrix =",m3)
    e=SetChainCode(m3,0,0,0,5)
    print("org code=",e)
    e1=MatrixTransformation(e,1,0,0)
    print("new code=",e1)
    e1=MatrixTransformation(e,2,0,0)
    print("new code=",e1)
    e1=MatrixTransformation(e,0,0,1)
    print("new code=",e1)
    e1=MatrixTransformation(e,0,0,2)
    print("new code=",e1)
    e1=MatrixTransformation(e,0,0,3)
    print("new code=",e1)
    e1=MatrixTransformation(e,0,1,0)
    print("new code=",e1)
    e1=MatrixTransformation(e,0,1,1)
    print("new code=",e1)
    e1=MatrixTransformation(e,0,1,2)
    print("new code=",e1)
    e1=MatrixTransformation(e,0,1,3)
    print("new code=",e1)
    e1=MatrixTransformation(e,0,2,0)
    print("new code=",e1)
    e1=MatrixTransformation(e,0,2,1)
    print("new code=",e1)
    e1=MatrixTransformation(e,0,2,2)
    print("new code=",e1)
    e1=MatrixTransformation(e,0,2,3)
    print("new code=",e1)

def TestChainCodeIsSame():
    codea=[0, 0, 1, 0, 0, 3, 0, 3, 0, 3, 2, 2, 2, 2, 2, 2, 1, 1]
    codeb=[0, 0, 3, 0, 3, 0, 3, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 1]
    res=CheckCodeSame(codea,codeb)
    print("")
    print("-------test case1:------------")
    print("codea=",codea)
    print("codeb=",codeb)
    print("is same?",res)
    
def TestChainCodeIsTwisted():
    a=[3, 0, 1, 0, 3, 2, 1, 2]
    b=CheckCodeSkew(a)
    print("")
    print("-------test case1:------------")
    print("code=",a)
    print("is skrew?",b)
    
    a=[0, 0, 1, 0, 0, 3, 0, 3, 0, 3, 2, 2, 2, 2, 2, 2, 1, 1]
    b=CheckCodeSkew(a)
    print("")
    print("-------test case2:------------")
    print("code=",a)
    print("is skrew?",b)
    
    a=[0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 2, 2, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1]
    b=CheckCodeSkew(a)
    print("")
    print("-------test case3:------------")
    print("code=",a)
    print("is skrew?",b)
    
    a=[0,0,3,0,3,0,3,2,2,2,1,2,1,1]
    b=CheckCodeSkew(a)
    print("")
    print("-------test case4:------------")
    print("code=",a)
    print("is skrew?",b)
    
    a=[0, 0, 0, 3, 0, 3, 3, 2, 2, 2, 1, 2, 1, 1]
    b=CheckCodeSkew(a)
    print("")
    print("-------test case5:------------")
    print("code=",a)
    print("is skrew?",b)
    
def TestMutualTransbtwMCA():#测试链码和矩阵之间的相互转化
    e=[0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 2, 2, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1]
    f=MatrixFromChainCodeM(e,12)
    print("")
    print("-------test case1:------------")
    print("orig code :",e)
    print("matrix =",f)
    
    e=[0,0,3,0,3,0,3,2,2,2,1,2,1,1]    
    f=MatrixFromChainCodeM(e,12)
    print("")
    print("-------test case2:------------")
    print("orig code :",e)
    print("matrix =",f)
    
    
    e=[0, 0, 0, 3, 0, 3, 3, 2, 2, 2, 1, 2, 1, 1]
    f=MatrixFromChainCodeM(e,11)
    f1=DisplayMatrixBDS(f[0],1)
    f2=DisplayMatrixAllS(f1[0],1)
    e1=SetChainCode(f2,0,0,0,5)
    print("")
    print("-------test case3:------------")
    print("orig code :",e)
    print("matrix =",f)
    print("matria from code:",f1)
    DisplayMatrix(f1[0])
    print("mat all from rest code:",f2)
    DisplayMatrix(f2)
    print("coda from matrix:",e1)
    print("")
    
    #测试一个错误情况,扭在一起的匹配:
    e=[3, 0, 1, 0, 3, 2, 1, 2]
    f=MatrixFromChainCodeM(e,0)
    f1=DisplayMatrixBDS(f[0],1)
    f2=DisplayMatrixAllS(f1[0],1)
    e1=SetChainCode(f2,0,0,0,5)
    print("")
    print("-------test case4:------------")
    print("orig code :",e)  
    print("matrix from code:",f)
    print("matria from code:",f1)
    DisplayMatrix(f1[0])
    print("mat all from rest code:",f2)
    DisplayMatrix(f2)
    print("coda from matrix:",e1)
    
        
    m1 = [#形状矩阵
     [1, 1, 0,0],
     [1, 1, 1,0],
     [0, 1, 1,0],
     [0, 0, 0,0]]
    e=SetChainCode(m1,0,0,0,5)
    f=MatrixFromChainCodeM(e,0)
    f1=DisplayMatrixBDS(f[0],1)
    f2=DisplayMatrixAllS(f1[0],1)
    e1=SetChainCode(f2,0,0,0,5)
    print("")
    print("-------test case5:------------")
    print("orig code :",e)  
    print("matrix from code:",f)
    print("matria from code:",f1)
    DisplayMatrix(f1[0])
    print("mat all from rest code:",f2)
    DisplayMatrix(f2)
    print("coda from matrix:",e1)

   
    mat = [#形状矩阵
     [1, 1, 0,0],
     [1, 1, 1,0],
     [1, 1, 1,0],
     [0, 0, 0,0]]
    e=SetChainCode(mat,0,0,0,5)
    f=MatrixFromChainCodeM(e,0)
    f1=DisplayMatrixBDS(f[0],1)
    f2=DisplayMatrixAllS(f1[0],1)
    e1=SetChainCode(f2,0,0,0,5)
    print("")
    print("-------test case6:------------")
    print("orig code :",e)  
    print("matrix from code:",f)
    print("matria from code:",f1)
    DisplayMatrix(f1[0])
    print("mat all from rest code:",f2)
    DisplayMatrix(f2)
    print("coda from matrix:",e1)
    
    mat = [#形状矩阵
     [0,0,1,0,0],
     [0,1,1,1,0],
     [1,1,1,1,1],
     [0,1,1,1,0],
     [0,0,1,0,0]]
    e=SetChainCode(mat,0,0,0,5)
    f=MatrixFromChainCodeM(e,0)
    f1=DisplayMatrixBDS(f[0],1)
    f2=DisplayMatrixAllS(f1[0],1)
    e1=SetChainCode(f2,0,0,0,5)
    print("")
    print("-------test case7:------------")
    print("orig code :",e)  
    print("matrix from code:",f)
    print("matria from code:",f1)
    DisplayMatrix(f1[0])
    print("mat all from rest code:",f2)
    DisplayMatrix(f2)
    print("coda from matrix:",e1)
    
def TestMutualTransbtwMC():#测试链码和矩阵之间的相互转化
    """
    要注意:在链码和矩阵的相互转化过程中:
    从链码到矩阵，再从矩阵到链码，可能会导致起点变化
    """
    #注意本例中矩阵内部空格的情况
    m1 = [#形状矩阵
     [1, 1, 0,0],
     [1, 0, 1,0],
     [1, 1, 1,0],
     [0, 0, 0,0]]
    e=SetChainCode(m1,0,0,0,5)
    f=MatrixFromChainCodeM(e,0)
    print("")
    print("-------test case1:------------")
    print("orig code :",e) 
    print("matrix from code:",f)
    f1=DisplayMatrixBDS(f[0],1)
    print("matria from code:",f1)
    DisplayMatrix(f1[0])
    #注意:1.中间空格不补全的情况
    e1=SetChainCode(f1[0],0,0,0,5)
    print("coda from matrix:",e1)
    
    #注意:2.中间空格补全的情况
    f2=DisplayMatrixAllS(f1[0],1)
    print("mat all from rest code:",f2)
    DisplayMatrix(f2)
    e1=SetChainCode(f2,0,0,0,5)
    print("coda from matrix:",e1)
    print("")
    
    #这是链码中间存在一条线的情况:
    #如下图所示4个box，中间有一段是重合的线
    #  box
    #  box___boxbox
    e=[0,3,3,0,1,0,0,3,2,2,2,2,1,1]
    print("")
    print("-------test case2:------------")
    print("orig code :",e)
    f=MatrixFromChainCodeM(e,0)
    print("matrix from code:",f)
    f1=DisplayMatrixBDS(f[0],1)
    print("matria from code:",f1)
    f2=DisplayMatrixAllS(f1[0],1)
    print("mat all from rest code:",f2)
    e1=SetChainCode(f2,0,0,0,5)
    print("coda from matrix:",e1)
    res=CheckCodeSame(e,e1)
    print("codea=",e)
    print("codeb=",e1)
    print("is same?",res)
    
    #这是链码中间存在一条线的情况:
    #如下图所示4个box，bx3和bx4中间有一段是重合的线
    #        bx3
    #  boxboxbx4
    #转换到矩阵过程中已经发生改变，得到的链码已经完全不同
    e=[0,0,0,1,2,3,0,3,2,2,2,1]
    print("")
    print("-------test case3:------------")
    print("orig code :",e)
    f=MatrixFromChainCodeM(e,0)
    print("matrix from code:",f)
    f1=DisplayMatrixBDS(f[0],1)
    print("matria from code:",f1)
    f2=DisplayMatrixAllS(f1[0],1)
    print("mat all from rest code:",f2)
    e1=SetChainCode(f2,0,0,0,5)
    print("coda from matrix:",e1)
    res=CheckCodeSame(e,e1)
    print("codea=",e)
    print("codeb=",e1)
    print("is same?",res)
    
    #case:
    #   box
    #box
    #   box
    #   box 
    e=[1,1,0,3,2,2,3,0,0,3,3,2,1,1]
    print("")
    print("-------test case4:------------")
    print("orig code :",e)
    f=MatrixFromChainCodeM(e,0)
    print("matrix from code:",f)
    f1=DisplayMatrixBDS(f[0],1)
    print("matria from code:",f1)
    f2=DisplayMatrixAllS(f1[0],1)
    print("mat all from rest code:",f2)
    e1=SetChainCode(f2,0,0,0,5)
    print("coda from matrix:",e1)
    res=CheckCodeSame(e,e1)
    print("codea=",e)
    print("codeb=",e1)
    print("is same?",res)
    
def TestChainCodeMatch():
    m1 = [#形状矩阵
     [1, 0, 0,0],
     [1, 1, 0,0],
     [1, 1, 1,0],
     [0, 0, 0,0]]
    
    m1a = [#形状矩阵
     [1, 0, 0,0],
     [1, 1, 0,0],
     [0, 0, 0,0],
     [0, 0, 0,0]]
    
    m1b = [#形状矩阵
     [1, 0, 0,0],
     [1, 0, 0,0],
     [1, 0, 0,0],
     [0, 0, 0,0]]
    
    print("")
    print("-------test case1:------------")
    c=SetChainCode(m1,0,0,0,5)    
    print("chain code of matrix boundary c =",c)
    ca=SetChainCode(m1a,0,0,0,5)
    print("chain code of matrix boundary ca=",ca)
    cb=SetChainCode(m1b,0,0,0,5)
    print("chain code of matrix boundary cb=",cb)
    c1=MatchChainCode(c,ca)
    print("after match c & ca rest code  c1=",c1)
    c2=MatchChainCode(c1[1],cb)
    print("after match c & cb rest code  c2=",c2)
    ce=MatrixTransformation(cb,0,0,1)
    c2=MatchChainCode(c1[1],ce)
    print("after match c & cb rest code  c2=",c2)
    
def TestSimpleJigsaw():
    m1 = [#形状矩阵
     [1, 0, 0,0],
     [1, 1, 0,0],
     [1, 1, 1,0],
     [0, 0, 0,0]]
    
    m1a = [#形状矩阵
     [1, 0, 0,0],
     [1, 1, 0,0],
     [0, 0, 0,0],
     [0, 0, 0,0]]
    
    m1b = [#形状矩阵
     [1, 1, 1,0],
     [0, 0, 0,0],
     [0, 0, 0,0],
     [0, 0, 0,0]]
    
    print("")
    print("-------test case1:------------")
    print("SimpleJigsaw:")
    MatchProcess(m1,[m1a,m1b])
    
    m1 = [#形状矩阵
     [1, 1, 1,0],
     [1, 1, 1,0],
     [1, 1, 1,0],
     [0, 0, 0,0]]
    
    m1a = [#形状矩阵
     [1, 0, 0,0],
     [1, 1, 1,0],
     [0, 0, 0,0],
     [0, 0, 0,0]]
    
    m1b = [#形状矩阵
     [1, 0, 0,0],
     [1, 0, 0,0],
     [0, 0, 0,0],
     [0, 0, 0,0]]
    
    m1c = [#形状矩阵
     [1, 1, 1,0],
     [0, 0, 0,0],
     [0, 0, 0,0],
     [0, 0, 0,0]]
    
    print("")
    print("-------test case2:------------")
    print("SimpleJigsaw:")
    MatchProcess(m1,[m1a,m1b,m1c])
    
def TestLargeJigsawA():
    #读取形状矩阵
    f=open("datatopython.dat","r")
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
    ntrys=1000
    for i in range(ntrys):
        res.append(MatchProcess(ma,mbs))
    f=open("result1.dat","w")
    for i in range(ntrys):
        f.write("%d %d %d %d %d %d\n"%(i,res[i][0],res[i][1],res[i][2],res[i][3],res[i][4]))
    f.close()
    
    #将拼图结果以json格式保存起来
    f = open("resjson.dat","w")
    json.dump(res,f)
    f.close()
    
    DataAnalysis(len(data)-1)
    
def TestSpecialJigsaw():
    #读取形状矩阵
    f=open("datatopython.dat","r")
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
    ntrys=1
    for i in range(ntrys):
        res.append(MatchProcess(ma,mbs))
    f=open("result1.dat","w")
    for i in range(ntrys):
        f.write("%d %d %d %d %d %d\n"%(i,res[i][0],res[i][1],res[i][2],res[i][3],res[i][4]))
    f.close()
    
    #将拼图结果以json格式保存起来
    f = open("resjson.dat","w")
    json.dump(res,f)
    f.close()
    
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
    f=open("result-compare-chaincode.dat","w")
    f.write("%d %f %f %f %f\n"%(len(ma),timeavg,assemblyavg,chooseavg,matchavg))
    f.close()
    
    #将拼图结果以json格式保存起来
    f = open("resjson.dat","w")
    json.dump(res,f)
    f.close()
    
def DataAnalysis(nshapes):
    f=open("resjson.dat","r")
    res=json.load(f)
    f.close()
    
    length=len(res)
    
    
    nchooselmt=sum([i for i in range(1,nshapes+1)])#极限的选择次数
    
    #成功拼图的选择次数6-21
    lista=[]
    for x in range(nshapes,nchooselmt+1):
        a=0
        for i in range(length):
            if x==res[i][0]:
                a+=1
        lista.append([x,a/length])
    f=open("result2.dat","w")
    for i in range(len(lista)):
        if lista[i][1]:
            f.write("%d %f\n"%(lista[i][0],lista[i][1]))
    f.close()
        
   
    #一次尝试多次拼图最后一次成功拼图的选择次数6-21*20
    lista=[]
    for x in range(nshapes,nchooselmt*20):
        a=0
        for i in range(length):
            if x==res[i][1]:
                a+=1
        lista.append([x,a/length])
    f=open("result3.dat","w")
    for i in range(len(lista)):
        if lista[i][1]:
            f.write("%d %f\n"%(lista[i][0],lista[i][1]))
    f.close()
    
    #成功拼图的匹配次数6-21*8
    lista=[]
    for x in range(nshapes,nchooselmt*8):
        a=0
        for i in range(length):
            if x==res[i][2]:
                a+=1
        lista.append([x,a/length])
    f=open("result4.dat","w")
    for i in range(len(lista)):
        if lista[i][1]:
            f.write("%d %f\n"%(lista[i][0],lista[i][1]))
    f.close()
    
    #一次尝试多次拼图最后一次成功拼图的匹配次数6-21*20*8
    lista=[]
    for x in range(nshapes,nchooselmt*20*8):
        a=0
        for i in range(length):
            if x==res[i][3]:
                a+=1
        lista.append([x,a/length])
    f=open("result5.dat","w")
    for i in range(len(lista)):
        if lista[i][1]:
            f.write("%d %f\n"%(lista[i][0],lista[i][1]))
    f.close()
    
    #一次成功拼图的做的拼图次数1-20*8
    lista=[]
    for x in range(1,100):
        a=0
        for i in range(length):
            if x==res[i][4]:
                a+=1
        lista.append([x,a/length])
    f=open("result6.dat","w")
    for i in range(len(lista)):
        if lista[i][1]:
            f.write("%d %f\n"%(lista[i][0],lista[i][1]))
    f.close()
    
def Gaussdis():
    f=open("resultgauss.dat","w")
    u=6
    sigma=2
    a=1.5
    b=5
    for x in range(6,101):
        fp=a*1.0/math.sqrt(2*3.1415926)/sigma*math.exp((-((x-u)/b)**2/2/sigma**2))
        f.write("%d %f\n"%(x,fp))
    f.close()
 
    
if __name__ == "__main__":

    savedStdout = sys.stdout #保存标准输出流
    filename="datatopython.dat"
    outfile="out-chaincodemethod"+filename
    file=open(outfile,'w+')
    sys.stdout = file #标准输出重定向至文件
    print(filename,"started!")
    TestLargeJigsaw(filename)
    sys.stdout = savedStdout #恢复标准输出流
    file.close()
    print(filename,"completed!")

    # savedStdout = sys.stdout #保存标准输出流
    # filename="datatopython6.dat"
    # outfile="out-chaincodemethod"+filename
    # file=open(outfile,'w+')
    # sys.stdout = file #标准输出重定向至文件
    # print(filename,"started!")
    # TestLargeJigsaw(filename)
    # sys.stdout = savedStdout #恢复标准输出流
    # file.close()
    # print(filename,"completed!")
    
    # savedStdout = sys.stdout #保存标准输出流
    # filename="datatopython7.dat"
    # outfile="out-chaincodemethod"+filename
    # file=open(outfile,'w+')
    # sys.stdout = file #标准输出重定向至文件
    # print(filename,"started!")
    # TestLargeJigsaw(filename)
    # sys.stdout = savedStdout #恢复标准输出流
    # file.close()
    # print(filename,"completed!")
    
    # savedStdout = sys.stdout #保存标准输出流
    # filename="datatopython8.dat"
    # outfile="out-chaincodemethod"+filename
    # file=open(outfile,'w+')
    # sys.stdout = file #标准输出重定向至文件
    # print(filename,"started!")
    # TestLargeJigsaw(filename)
    # sys.stdout = savedStdout #恢复标准输出流
    # file.close()
    # print(filename,"completed!")
    
    # savedStdout = sys.stdout #保存标准输出流
    # filename="datatopython9.dat"
    # outfile="out-chaincodemethod"+filename
    # file=open(outfile,'w+')
    # sys.stdout = file #标准输出重定向至文件
    # print(filename,"started!")
    # TestLargeJigsaw(filename)
    # sys.stdout = savedStdout #恢复标准输出流
    # file.close()
    # print(filename,"completed!")
    
    # savedStdout = sys.stdout #保存标准输出流
    # filename="datatopython10.dat"
    # outfile="out-chaincodemethod"+filename
    # file=open(outfile,'w+')
    # sys.stdout = file #标准输出重定向至文件
    # print(filename,"started!")
    # TestLargeJigsaw(filename)
    # sys.stdout = savedStdout #恢复标准输出流
    # file.close()
    # print(filename,"completed!")
    
   
    #测试链码生成
    #TestChainCodeGeneration()
    
    #测试中空矩阵的链码生成
    #TestBoundaryMatrixToCode()

    #测试形状变换导致的链码变化
    #TestChainCodeTransformation()
    
    #测试两个链码是否相同
    #TestChainCodeIsSame()
    
    #测试扭曲的链码，即形成独立box的链码情况:
    #TestChainCodeIsTwisted()
    
    #测试链码和形状矩阵相互转化
    #TestMutualTransbtwMCA()
    
    #测试链码和形状矩阵相互转化
    #TestMutualTransbtwMC()
    
    #测试链码匹配
    #TestChainCodeMatch()
    
    #测试简单形状拼图
    #TestSimpleJigsaw()
    
    #测试复杂形状拼图，从json数据文件读入的复杂拼图
    #TestLargeJigsaw(filename)
    
    #利用记录的json数据处理信息,输入参数为网格大小
    #DataAnalysis(8)
    
    #高斯分布
    #Gaussdis()
    
    #测试一个特殊的复杂形状拼图，从json数据文件读入的复杂拼图
    #TestSpecialJigsaw()
    
    
 