#include <iostream>
#include <sstream>
#include <string>

using namespace std;

int main() {
  stringstream ostr("ccc");
  ostr.put('d');
  ostr.put('e');
  ostr<<"fg";
  string gstr = ostr.str();
  cout<<gstr<<endl;

  char a;
  ostr>>a;
  cout<<a<<endl;
  return 0;
}
