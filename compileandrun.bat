::形状划分及拼图算法测试


::编译

cls

del /q pt.exe 

g++ pt.cpp -o pt.exe


::运行，两个整数参数是网格大小和球链接形状的大小

pt.exe 10 5


::python下的拼图测试

::基于矩阵填充的算法

python puzzle.py

::基于边界链码的算法

python chaincode.py

pause