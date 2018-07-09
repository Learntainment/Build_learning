#include <iostream>
#include <vector>
#include <map>
using namespace std;

class Base
{
public:
    void menfcn()
    {
        cout << "Base function" << endl;
    }
    void menfcn(int n)
    {
        cout << "Base function with int" << endl;
    }
};

class Derived : public Base
{
public:
    using Base::menfcn;
    int menfcn(int num)
    {
        cout << "Derived functin with int: " << num << endl;
        return num;
    }

};

using IntVec = std::vector<int>;

void testUsing()
{
    IntVec vec = {1, 2, 3, 4, 5};
    vec.push_back(123);
    for (int num : vec)
        cout << "vec num " << num << endl;
    cout << is_same < std::vector<int>, IntVec>::value << endl;
}

template <typename T>
using MapStr = std::map<T, std::string>;
void testUsing2()
{
    MapStr<int> intStrMap;
    intStrMap.insert(make_pair(123, "aaa"));
    intStrMap.insert(make_pair(456, "bbb"));
    MapStr<int>::iterator iter;

    for (iter = intStrMap.begin(); iter != intStrMap.end(); iter++)
        cout << iter->first << " " << iter->second << endl;

    MapStr<std::string> strStrMap;
    strStrMap.insert(make_pair("ccc", "ddd"));
    strStrMap.insert(make_pair("eee", "fff"));
    MapStr<std::string>::iterator striter;

    for (striter = strStrMap.begin(); striter != strStrMap.end(); striter++)
        cout << striter->first << " " << striter->second << endl;
}

int main()
{
    Base b;
    Derived d;
    b.menfcn();
    d.menfcn();
    d.menfcn(123);

    testUsing();
    testUsing2();

    return 0;
}

