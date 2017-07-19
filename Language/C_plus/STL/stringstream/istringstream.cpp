#include <iostream>
#include <sstream>

using namespace std;
int main() {
  istringstream istr;
  istr.str("1 56.7");
  cout << istr.str()<<endl;
  int a;
  float b;
  istr>>a;
  cout<<a<<endl;
  istr>>b;
  cout<<b<<endl;
  return 0;
}
