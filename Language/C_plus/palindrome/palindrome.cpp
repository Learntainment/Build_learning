#include <iostream>

using namespace std;

int palindrome(int value) {
    int temp = value;
    int number = value;
    int sum = 0;
    while (number) {
        sum = sum*10 + number%10;
        number = number/10;
    }
    if (sum == temp) {
        return 0;
    }
    return -1;
}

int main() {
    cout << "palindrome" << endl;
    int result = palindrome(12321);
    cout << "result is " << result << endl;
    int fail = palindrome(12345);
    cout << "fail is " << fail << endl;
    return 0;
}

