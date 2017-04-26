#include "muldiv.h"
#include "gtest/gtest.h"

int multiply(int one,int two){
    return one*two;
}

int divide(int one,int two){
    return one/two;
}

TEST(MultiplyTest,MutilplyTestCase){
    ASSERT_EQ(12,multiply(3,4));
}

TEST(DivideTest,DivideTestCase){
    ASSERT_EQ(4,divide(7,3));
}
