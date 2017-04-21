//g++ -Wall ref_class.cpp -o run --std=c++11

#include <iostream>

using namespace std;

class A {
public:
    A(int i=3):m_i(i){}
    void print()
    {
        cout<<"m_i="<<m_i<<endl;
    }
private:
    int m_i;
};

class B {
public:
    B(A& a):m_a(a){}
    void display()
    {
        m_a.print();
    }
private:
    A& m_a;

};
int main(int argc,char** argv) {
    A a(10);
    B b(a);
    b.display();
    return 0;
}
