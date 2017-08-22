//g++ serialization.cpp -o run -std=c++11 -lboost_serialization
#include <boost/archive/text_iarchive.hpp>
#include <boost/archive/text_oarchive.hpp>
#include <iostream>
#include <fstream>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include <iterator>
#include <boost/serialization/list.hpp>
#include <boost/serialization/vector.hpp>

void xml_save()
{
  std::ofstream file("archive.xml");
  boost::archive::xml_oarchive oa(file);
  std::string s = "Hello World!\n";
  oa & BOOST_SERIALIZATION_NVP(s);
}

void xml_load()
{
  std::ifstream file("archive.xml");
  boost::archive::xml_iarchive ia(file);
  std::string s;
  ia & BOOST_SERIALIZATION_NVP(s);
  std::cout << s << std::endl;
}


void array_save()
{
  std::ofstream file("archive.xml");
  boost::archive::xml_oarchive oa(file);
  int array1[] = {34, 78, 22, 1, 910};
  oa & BOOST_SERIALIZATION_NVP(array1);
}

void array_load()
{
  std::ifstream file("archive.xml");
  boost::archive::xml_iarchive ia(file);
  int restored[5]; // Need to specify expected array size
  ia >> BOOST_SERIALIZATION_NVP(restored);
  std::ostream_iterator<int> oi(std::cout, " ");
  std::copy(restored, restored+5, oi);
}

void save() {
  std::ofstream file("archive.txt");
  boost::archive::text_oarchive oa(file);
  std::string s = "Hello World!\n";
  oa << s;
}

void load() {
  std::ifstream file("archive.txt");
  boost::archive::text_iarchive ia(file);
  std::string s;
  ia >> s;
  std::cout << s << std::endl;
}

void stl_save()
{
  std::ofstream file("archive.xml");
  boost::archive::xml_oarchive oa(file);
  float array[] = {34.2, 78.1, 22.221, 1.0, -910.88};
  std::list<float> L1(array, array+5);
  std::vector<float> V1(array, array+5);
  oa & BOOST_SERIALIZATION_NVP(L1);
  oa & BOOST_SERIALIZATION_NVP(V1);
}

void stl_load()
{
  std::ifstream file("archive.xml");
  boost::archive::xml_iarchive ia(file);
  std::list<float> L2;
  ia >> BOOST_SERIALIZATION_NVP(L2); // No size/range needed

  std::vector<float> V2;
  ia >> BOOST_SERIALIZATION_NVP(V2); // No size/range needed

  std::ostream_iterator<float> oi(std::cout, " ");
  std::copy(L2.begin(), L2.end(), oi);
  std::copy(V2.begin(), V2.end(), oi);
}

int main() {
    save();
    load();
    xml_save();
    xml_load();
    array_save();
    array_load();
    stl_save();
    stl_load();
    return 0;
}
