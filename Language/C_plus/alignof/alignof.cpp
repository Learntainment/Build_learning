#include <iostream>

struct Foo {
    int   i;
    float f;
    char  c;
};

struct Empty {};

struct alignas(64) Empty64 {};

int main()
{
    std::cout << "Alignment of"  "\n"
        "- char             : " << alignof(char)    << "\n"
        "- char size of     : " << sizeof(char)    << "\n"
        "- int              : " << sizeof(int)      << "\n"
        "- float             : " << sizeof(float)      << "\n"
        "- pointer          : " << alignof(int*)    << "\n"
        "- pointer size of  : " << sizeof(int*)    << "\n"
        "- class Foo        : " << alignof(Foo)     << "\n"
        "- class Foo size of: " << sizeof(Foo)     << "\n"
        "- empty class      : " << alignof(Empty)   << "\n"
        "- empty class size : " << sizeof(Empty)   << "\n"
        "- alignas(64) Empty: " << alignof(Empty64) << "\n";
}
