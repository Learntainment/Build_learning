//g++ -Wall ref_value.cpp -o run --std=c++11

#include <iostream>
using namespace std;

int main(){
    int a = 99;
    int &b = a;
    int const &c = a;
    b = 47;
    cout<<a<<", "<<b<<", "<<c<<endl;

    return 0;
}
