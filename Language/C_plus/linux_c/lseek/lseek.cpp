#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
    int fd = open("abc",O_RDWR);
    if(fd < 0)
    {
        perror("open abc");
        exit(-1);
    }
    //拓展文件大小,用od -tcx abc命令查看结果
    lseek(fd, 0X1000,SEEK_SET);
    write(fd, "a", 1);

    //用lseek获取文件大小
    printf("abc's size:%d\n",(int)lseek(fd,0,SEEK_END));

    close(fd);
    return 0;
}
