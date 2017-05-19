//在派生类中成员初始化列表先初始化派生类的私有成员，显示的调用基类的构造函数
//print constructor is called
#include <iostream>
using namespace std;

class Base {
private:
    int n;

public:
    Base(){ cout<<"default constructor is called\n"; n = 8;}
    Base(int m):n(m){ cout<<"constructor is called\n";}
    ~Base(){}
};

class Derive:public Base {
private:
    int n;

public:
    Derive(int m):Base(m),n(m) {}
    ~Derive(){}
};

int main() {
    Derive* a = new Derive(10);
    return 0;
}
