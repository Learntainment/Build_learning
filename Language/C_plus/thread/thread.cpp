//g++ thread.cpp -pthread/-lpthread -std=c++11

#include <iostream>       // std::cout
#include <thread>         // std::thread, std::this_thread::sleep_for
#include <chrono>         // std::chrono::seconds
#include <array>
#include <mutex>
#include <atomic>

using namespace std;

const int N = 1000000000;
int num = 0;
mutex m;
atomic_int ato_num{0};

void run() {
    for(int i=0; i<N; i++) {
        /*m.lock();
        num++;
        m.unlock();*/
        //ato_num++;
        num++;
    }
}

void pause_thread(int n) {
    std::this_thread::sleep_for (std::chrono::seconds(n));
    std::cout << "pause of " << n << " seconds ended\n";
}

void show(const char *str, const int id) {
    std::cout << "thread=" << id+1 << " : " << str << std::endl;
}

void print() {
    cout << "hello test!" << endl;
}

void fun1(int n)  //初始化构造函数
{
	cout << "Thread " << n << " executing\n";
	n += 10;
	this_thread::sleep_for(chrono::milliseconds(10));
}

void fun2(int & n) //拷贝构造函数
{
	cout << "Thread " << n << " executing\n";
	n += 20;
	this_thread::sleep_for(chrono::milliseconds(10));
}

int main() {
    // join thread
    std::cout << "Spawning 3 threads...\n";
    std::thread t3(pause_thread, 3);
    std::thread t1(pause_thread, 1);
    std::thread t2(pause_thread, 2);
    std::cout << "Done spawning threads. Now waiting for them to join:\n";
    t1.join();
    t2.join();
    t3.join();
    std::cout << "All threads joined!\n";
    // thread detach
    std::cout << "Spawning and detaching 3 threads...\n";
    std::thread t4(pause_thread, 3);
    std::thread t5(pause_thread, 1);
    std::thread t6(pause_thread, 2);
    t4.detach();
    t5.detach();
    t6.detach();
    std::cout << "Done spawning threads.\n";

    std::cout << "(the main thread will now pause for 5 seconds)\n";
    //give the detached threads time to finish (but not guaranteed!):
    pause_thread(5);

    // thread joinable usage
    std::cout << "thread joinable usage \n";
    std::thread t;
    std::cout << "before starting joinable: " << t.joinable() << "\n";
    t = std::thread(pause_thread, 5);
    std::cout << "after starting, joinable: " << t.joinable() << "\n";
    t.join();
    std::cout << "after join, joinable: " << t.joinable() << "\n";

    // swap thread
    std::thread t7(pause_thread, 10);
    std::thread::id t7_id = t7.get_id();

    std::thread t8(pause_thread, 20);
    std::thread::id t8_id = t8.get_id();

    std::cout << "t7 id: " << t7_id << "\n";
    std::cout << "t8 id: " << t8_id << "\n";

    swap(t7, t8);

    std::cout << "t7 id: " << t7.get_id() << "\n";
    std::cout << "t8 id: " << t8.get_id() << "\n";

    t7.join();
    t8.join();

    // thread different thread input
    int n = 0;
    thread t11;               //t11不是一个thread
    thread t12(fun1, n + 1);  //按照值传递
    t12.join();
    cout << "n=" << n << '\n';
    n = 10;
    thread t13(fun2, ref(n)); //引用
    thread t14(move(t13));     //t14执行t13，t13不是thread
    t14.join();
    cout << "n=" << n << '\n';

    array<thread, 3> thread_array = {thread(print), thread(print), thread(print)};
    for(int i=0; i<3; i++) {
        cout << thread_array[i].joinable() << endl;
        thread_array[i].join();
    }

    //thread cpu number
    auto cpu = thread::hardware_concurrency();
    cout << "thread cpu num " << cpu << endl;

    // mutex usage
    clock_t start = clock();
    thread t15(run);
    //thread t16(run);
    t15.join();
    thread t16(run);
    t16.join();
    clock_t end = clock();
    cout << "num = " << num << " time = " << end-start << " ms" << endl;
    //cout << "ato num = " << ato_num << " time = " << end-start << " ms" << endl;



    return 0;
}


