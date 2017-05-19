//派生类析构函数的调用过程中会不会自动去调用基类的析构函数呢？答案是，肯定的，所以千万不要在派生类的析构函数中再去调用基类的析构函数，这种去释放已经释放的内存，系统是不允许的。
//print default constructor is called
//print Derive distructor is called
//print Base distructor is called
#include <iostream>
using namespace std;

class Base {
private:
    int n;

public:
    Base(){ cout<<"default constructor is called\n"; n = 8;}
    Base(int m):n(m){ cout<<"constructor is called\n";}
    ~Base(){ cout<<"Base distructor is called\n"; }
};

class Derive:public Base {
private:
    int n;

public:
    Derive(int m):Base(m),n(m){}
    ~Derive(){ cout<<"Derive distructor is called\n"; }
};

int main()
{
    Derive* a = new Derive(10);
    delete a;
    return 0;
}
