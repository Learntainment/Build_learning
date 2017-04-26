#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include <string>
#include "MockFoo.h"
#include <iostream>

using namespace std;
using ::testing::AtLeast;
using ::testing::Return;

TEST(MockFoo, getNum) {
    int value = 3;
    MockFoo mockfoo;
    EXPECT_CALL(mockfoo, getNum(2)).Times(AtLeast(1)).WillOnce(Return(value));
    Call_Foo callFoo;
    callFoo.showString(mockfoo, 2);
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
