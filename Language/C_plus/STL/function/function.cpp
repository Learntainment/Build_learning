#include <iostream>
#include <functional>
double f(int x, char y, double z) {
    return x + y + z;
}
void print_num(int num) {
    std::cout << num << std::endl;
}
struct Dog {
    int id;
    explicit Dog(int id): id(id) {}
    void print_add(int i) const {
        std::cout << id + i << std::endl;
    }
};
class PrintString {
public:
    void operator()(std::string&& s) const {
        std::cout << s << std::endl;
    }
};
int main(int argc, char **argv) {
    // common function
    std::function<void(int)> func_display_num = print_num;
    func_display_num(9);
    // common function
    std::function<double(int, char, double)> func_display = f;
    std::cout << func_display(3, 'a', 1.7) << "\n";
    // lambda expression
    std::function<void(const char*)> lbd_dsp_str = [](const char *s) {std::cout << s << std::endl;};
    lbd_dsp_str("Scala");
    // bind expression
    auto func_num_bind = std::bind(&f, std::placeholders::_1, 'c', 2.4);
    std::cout << func_num_bind(24) << "\n";
    // function object
    std::function<void(std::string&&)> func_obj_print = PrintString();
    func_obj_print("C++ 17 Nice!");
    // member function
    const Dog dog(2424);
    std::function<void(const Dog&, int)> func_mem_display_num = &Dog::print_add;
    func_mem_display_num(dog, 24);
    return 0;
}

