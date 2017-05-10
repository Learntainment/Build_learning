#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <iostream>

using namespace std;

int main(){
    int fd;
    int length = 24;
    int count = 2;
    int offset = 28;
    int ret;
    char buf[1024];
    char pathname[128] = "test";
    fd = open( pathname, O_RDONLY);
    while (count < length) {
        ret = pread64(fd, buf, length - count, offset + count);
        cout << "ret is " << ret << endl;
        count += ret;
        cout << "buffer is " << buf << endl;
    }
    cout << "count is " << count << endl;
    return 0;
}
