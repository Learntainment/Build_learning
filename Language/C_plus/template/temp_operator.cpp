#include <iostream>
#include <string>
#include <vector>
using namespace std;


template <typename object> 
class MemoryCell
{
public:
    explicit MemoryCell(const object& initvalue = object())
        :storedvalue(initvalue) {}
    const object& read() const
    {return storedvalue;}
    void write(const object& x)
    {storedvalue = x;}

private:
    object storedvalue;
};

template <typename comparable>
const comparable& findMax( const vector<comparable>& a)
{
    int Maxindex = 0;
    for (int i = 0; i < a.size(); i++)
    {
        if(a[Maxindex] < a[i])
        {
            Maxindex = i;
        }
    }
    return a[Maxindex];
}

class employee
{
    public:
    void setValue(const string& n, int s){
        name = n;
        salary = s;
    }
    
    const string getName() const{
        return name;
    }
    
    void print(ostream & out) const{
        out << name << "(" << salary << ")";
    }
    
    bool operator< (const employee& rhs) const{
        return salary < rhs.salary;
    }
    
    private:
    string name;
    int salary;
    
};

ostream & operator<< (ostream& out, const employee& rhs){
    rhs.print(out);
    return out;
}

int main()
{
    /*MemoryCell<int> m1;
    m1.write(32);
    MemoryCell<string> m2("hello");
    m2.write(m2.read() + " world");
    cout << m1.read() << endl;
    cout << m2.read() << endl;*/
    vector<employee> v(3);
    v[0].setValue("a", 100);
    v[1].setValue("b", 200);
    v[2].setValue("c", 300);
    cout << findMax(v) << endl;
    return 0;
}
