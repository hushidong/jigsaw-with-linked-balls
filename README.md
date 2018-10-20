<b>Date of last change: 2018-08-14 to version v1.0m</b>


# 球链接形状拼图算法
---------------------------------------------------------

    

## 简介

Maintainer: huzhenzhen <hzzmail@163.com>

Homepage: <https://github.com/hushidong/>

License: 

为二维[球链接形状拼图游戏](https://github.com/hushidong/)，完整设计了形状拆分和形状拼接算法。

如果用数字表示一个球，那么一个10*10的下三角拼图如下图所示，共有55个球构成了一个球的矩阵。

     1
     2     3
     4     5     6
     7     8     9    10
    11    12    13    14    15
    16    17    18    19    20    21
    22    23    24    25    26    27    28
    29    30    31    32    33    34    35    36
    37    38    39    40    41    42    43    44    45
    46    47    48    49    50    51    52    53    54    55
	
这个球矩阵可以利用拆分算法拆分成由若干个球链接在一起的小的形状，并且这些小的形状都是独一无二的，这些形状用于玩家进行拼图。
比如拆分成如下12个小的形状：

total number of shapes in grid is 12
shape No.=1 ,serial number of balls in shape:34 42 43 44 36
shape No.=2 ,serial number of balls in shape:6 9 8 5 12
shape No.=3 ,serial number of balls in shape:52 53 54 55 45
shape No.=4 ,serial number of balls in shape:20 19 26 33 41
shape No.=5 ,serial number of balls in shape:25 32 24 18 17
shape No.=6 ,serial number of balls in shape:13 14 15 10
shape No.=7 ,serial number of balls in shape:40 39 38 47 46
shape No.=8 ,serial number of balls in shape:4 7 11 16 22
shape No.=9 ,serial number of balls in shape:35 28 27 21
shape No.=10 ,serial number of balls in shape:37 29 30 23 31
shape No.=11 ,serial number of balls in shape:1 2 3
shape No.=12 ,serial number of balls in shape:50 51 49 48

也就是把球链接矩阵变成为了12个形状构成的拼图：
    11
    11    11
     8     2     2
     8     2     2     6
     8     2     6     6     6
     8     5     5     4     4     9
     8    10     5     5     4     9     9
    10    10    10     5     4     1     9     1
    10     7     7     7     4     1     1     1     3
     7     7    12    12    12    12     3     3     3     3
	 
拆分出来后，小的形状可以通过各种组合来完成对原来下三角球链接形状的拼接，这可以让玩家来完成，也可以用拼接算法自动完成这一工作。
比如经过拼接算法计算得到一种拼图结果为：

    4
    4    5
    4    5    5
    4    4    5    5
   10   10    1    1    2
    8   10   10    1    2    2
    8   10    1    1    2    2    9
    8    6   12   12   12   12    9    9
    8    6    6    7    7    7    3    9   11
    8    6    7    7    3    3    3    3   11   11

可以看到形状的拼接与原来的拆分图是不同的，可以知道形状的有很多不同的拼接方案。玩家只要找到其中一种就可以完成拼图了。拼接算法也就是是自动找寻这种拼接方案的。

其中拆分算法已经用在[拼图游戏]中，这里主要目的是给出拼接的算法。



## 用法

共分两个程序，一个是cpp，两个py的。
cpp提供了整个球链接形状拼图的拆分程序，以及一个基于形状填充的拼接程序。
py提供了一个基于形状填充的拼接程序和一个基于边界连码的拼接程序。

cpp变成成的程序为pt，需要两个整数参数：分别是拼图总的大小，即拼图的球网格大小
和拼图中连接球形状大小，即一个形状中的连接球数

运行方式为：

`pt 10 5`

输出包括命令行的信息以及一个给python程序的拆分后的形状列表（datatopython.dat，为json格式）。还包括sn-grid.dat（拼图的最终形状表示），sn-timesc.csv（拼图的时间统计）。其中
times  : 为把所有形状拼成一幅图的次数，可能完成拼图，也可能尝试多次后无法拼成功进行下一次拼图
cputime: 为完成正确的拼图或完成指定上限的拼图次数的时间。

py程序直接利用python解析器运行，在命令行下，命令为：

`python puzzle.py`

`python chaincode.py`

输入的需要拼图的形状列表直接在程序内指定，比如：

```
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
```

---------------------------------------------------------

## need to do:

* 把数据结果说明清楚

---------------------------------------------------------

## Version history:

* 2018/04/20 v1.0  
* 2018/10/20 v1.1

---------------------------------------------------------
## 更新历史:


date of update: 2018-10-20 to version v1.1


* 介绍了用法，放到github上来

add an introduction, and upload to github.




