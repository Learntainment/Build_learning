//g++ -g temp_convert.cpp -o run --std=c++11
//debug to see template convert
//gdb ./run
//break main
//display /3i $pc
//r
//Add<double> (left=1.2, right=3.3999999999999999) at temp_convert.cpp:6
//use new template add<double> not add<int>

#include <iostream>

template <typename T>
T Add(T left, T right)
{
    return left + right;
}

int Add(int left, int right)
{
    return left + right;
}

int main()
{
    Add(1.2, 3.4);
    return 0;
}
