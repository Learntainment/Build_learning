// g++ -g temp_override.cpp -o run --std=c++11
// 1.对于非模板函数和同名函数模板,如果其他条件都相同,在调动时会优先调动非模板函数而不会从该模板产生出一个实例。如果模板可以产生一个具有更好匹配的函数,那么将选择模板
// 2.模板函数不允许自动类型转换,但普通函数可以进行自动类型转换

#include <iostream>

int Max(const int& left, const int & right) {
    return left>right? left:right;
}
template<typename T>
T Max(const T& left, const T& right) {
    return left>right? left:right;
}
template<typename T>
T Max(const T& a, const T& b, const T& c) {
    return Max(Max(a, b), c);
};
int main() {
    Max(10, 20, 30); // using template
    Max<>(10, 20); // using template not int Max
    Max(10, 20); // using int Max not template
    Max(10, 20.12); // using int Max not template
    Max<int>(10.0, 20.0); // using template
    Max(10.0, 20.0); //using template with double type
    return 0;
}
