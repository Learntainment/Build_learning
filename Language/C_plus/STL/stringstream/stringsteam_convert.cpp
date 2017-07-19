#include <iostream>
#include <sstream>
#include <string>

using namespace std;

int main() {
  stringstream sstr;
  //--------int convert string-----------
  int a=100;
  string str;
  sstr<<a;
  sstr>>str;
  cout<<str<<endl;
  //--------string convert char[]--------
  sstr.clear();
  string name = "colinguan";
  char cname[200];
  sstr<<name;
  sstr>>cname;
  cout<<cname<<endl;
  return 0;
}
