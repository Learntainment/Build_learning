#include <iostream>
#include <sstream>
#include <string>

using namespace std;

int main() {
  ostringstream ostr;
  ostr.put('d');
  ostr.put('e');
  ostr<<"fg";
  string gstr = ostr.str();
  cout<<gstr<<endl;
  return 0;
}
