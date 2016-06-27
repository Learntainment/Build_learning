#include <iostream>
#include "gtest/gtest.h"

using namespace std;

int main(int argc,char* argv[])
{
    //testing::GTEST_FLAG(output) = "xml:"; //若要生成xml结果文件
    testing::InitGoogleTest(&argc,argv); //初始化
    return RUN_ALL_TESTS();
}
