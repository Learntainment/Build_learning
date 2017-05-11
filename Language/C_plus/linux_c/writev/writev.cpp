#include <sys/types.h>
#include <sys/uio.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <iostream>

using namespace std;

int main() {
    ssize_t bytes_written;
    int fd;
    char pathname[128] = "test";
    fd = open(pathname, O_WRONLY);
    char *buf0 = "short string\n";
    char *buf1 = "This is a longer string\n";
    char *buf2 = "This is the longest string in this example\n";
    int iovcnt;
    struct iovec iov[3];

    iov[0].iov_base = buf0;
    iov[0].iov_len = strlen(buf0);
    iov[1].iov_base = buf1;
    iov[1].iov_len = strlen(buf1);
    iov[2].iov_base = buf2;
    iov[2].iov_len = strlen(buf2);
    iovcnt = sizeof(iov) / sizeof(struct iovec);
    cout << "iovcnt is " << iovcnt << endl;
    bytes_written = writev(fd, iov, iovcnt);
    return 0;
}
