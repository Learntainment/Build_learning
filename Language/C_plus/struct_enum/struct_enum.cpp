#include <stdio.h>
#include <atomic>
#include <iostream>

using namespace std;

enum objectcacher{
    l_objectcacher_first = 25000,

    l_objectcacher_cache_ops_hit, // ops we satisfy completely from cache
    l_objectcacher_cache_ops_miss, // ops we don't satisfy completely from cache

    l_objectcacher_cache_bytes_hit, // bytes read directly from cache

    l_objectcacher_cache_bytes_miss, // bytes we couldn't read directly

  				   // from cache

    l_objectcacher_data_read, // total bytes read out
    l_objectcacher_data_written, // bytes written to cache
    l_objectcacher_data_flushed, // bytes flushed to WritebackHandler
    l_objectcacher_overwritten_in_flush, // bytes overwritten while
  				       // flushing is in progress

    l_objectcacher_write_ops_blocked, // total write ops we delayed due
  				    // to dirty limits
    l_objectcacher_write_bytes_blocked, // total number of write bytes
  				      // we delayed due to dirty
  				      // limits
    l_objectcacher_write_time_blocked, // total time in seconds spent
  				     // blocking a write due to dirty
  				     // limits

    l_objectcacher_last,
};

struct{
    char *name;  //姓名
    int num;  //学号
    int age;  //年龄
    char group;  //所在小组
    float score;  //成绩
} stu1;

int main()
{
    atomic<int> ato_num(0);
    cout << "ato num " << ato_num << endl;
    atomic_int ato_int(10);
    cout << "ato int " << ato_int << endl;
    enum objectcacher test = l_objectcacher_data_read;
    printf("test enum %d \n", test);
    //给结构体成员赋值

    stu1.name = "Tom";
    stu1.num = 12;
    stu1.age = 18;
    stu1.group = 'A';
    stu1.score = 136.5;

    printf("%s的学号是%d，年龄是%d，在%c组，今年的成绩是%.1f！\n", stu1.name, stu1.num, stu1.age, stu1.group, stu1.score);
    return 0;
}
