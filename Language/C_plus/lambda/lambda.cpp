//g++ lambda.cpp -o run --std=c++11
//匿名函数

#include <iostream>
using namespace std;
int main()
{
    auto foo = []() { cout << "Hello, Lambda!\n"; };
    foo();  // call the function
    auto foo2 = [](int x)
    {
        cout << x << endl;
    };
    foo2(9);  // 9
    int y = 2;
    auto foo3 = [y](int x)
    {
        cout << x * y << endl;
    };
    foo3(5);  // 10
    return 0;
}
