==============
**ONE**
==============

**Get**
============
Google test这个项目在Github上面，具体请见 `这里`_


.. _这里: https://github.com/google/googletest


git clone https://github.com/google/googletest


**Install**
==============
google test的编译方式有些区别。具体如下：


编译生成gtest-all.o文件

g++ -I./include -I./ -c ./src/gtest-all.cc

再生成.a的静态库文件

ar -rv libgtest.a gtest-all.o

最后将include下的gtest 和 libgtest.a 一起copy到自己的项目中去。环境安装完成


**Compile**
==========
google test的具体编译过程如下：
参考 `测试用例`_ 你可以拷贝这些在你的环境中。

.. _测试用例: test_example/

个人习惯，我将libgtest.a 放在了lib这个文件夹中，并将gtest放在了include文件夹下


文件编译 g++ -isystem include/ -pthread addsubfunc.cpp muldivfunc.cpp testall.cpp -o main -std=c++11 lib/libgtest.a

**Run**
==========
执行编译好的文件
./main

本文版权归个人所有，如需转载，请注明出处
=====================
