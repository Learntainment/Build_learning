// g++ boost_bind.cpp -o run -std=c++11

#include <iostream>
#include <boost/bind.hpp>
#include <algorithm>

using namespace std;

class F
{
public:
    int operator()(int a, int b)
    {
        cout << a+b <<endl;
        return a+b;
    }
    double operator()(double a, double b)
    {
        cout << a+b<< endl;
        return a +b;
    }
};

int main()
{
    F f;
    int a[] = {1, 2, 3, 4, 5, 6,7};
    double aDouble[] = {1.1, 2.2, 3.3, 4.4,5.5,6.6,7.7};
    for_each(a, a+5, boost::bind<int>(f, _1, _1));
    for_each(aDouble, aDouble+5, boost::bind<double>(f, _1, _1));
    return 0;
}


