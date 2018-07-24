#include <stdio.h>
#include <string>
#include <iostream>
using namespace std;

int main() {
    string str1 = "hello world";
    string str2 = str1;

    printf ("Sharing the memory:\n");
    cout << "str1 is " << &str1 << endl;
    cout << "str2 is " << &str2 << endl;
    //printf ("str1's address: %x\n", str1.c_str());
    //printf ("str2's address: %x\n", str2.c_str());

    str1[1]='q';
    str2[1]='w';

    printf ("After Copy-On-Write:\n");
    cout << "str1 is " << &str1 << endl;
    cout << "str2 is " << &str2 << endl;
    //printf ("str1's address: %x\n", str1.c_str());
    //printf ("str2's address: %x\n", str2.c_str());
    return 0;
}
