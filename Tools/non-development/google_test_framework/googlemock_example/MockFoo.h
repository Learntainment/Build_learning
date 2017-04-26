#include "gmock/gmock.h"
#include <iostream>
#include <string>

using namespace std;

class FooInterface {
public:
    virtual ~FooInterface() {}
    virtual int getNum(int newNumber) {
        cout << "get number" << endl;
        return (newNumber << 2);
    }
};

class Call_Foo {
public:
    int showString(FooInterface& oFoo, int callNumber) {
        cout << "test call foo get number function" << endl;
        int return_value = oFoo.getNum(callNumber);
        cout << return_value << endl;
        return return_value;
    }
};

class MockFoo:public FooInterface {
public:
    MOCK_METHOD1(getNum, int(int));
};

