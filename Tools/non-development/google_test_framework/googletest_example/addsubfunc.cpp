#include "addsub.h"
#include "gtest/gtest.h"

int add(int one,int two){
    return one+two;
}

int subduction(int one,int two){
    return one-two;
}

TEST(AddTest,AddTestCase){
    ASSERT_EQ(2,add(1,1));
}

TEST(SubductionTest,SubductionTestCase){
    ASSERT_EQ(10,subduction(25,15));
}

