#include <iostream>

using namespace std;

template <typename T>
T add(T left, T right) {
    return left+right;
}

int main() {
    add(1,2);
    return 0;
}
