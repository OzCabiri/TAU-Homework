#include "message_slot.h"   

#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    int fd;
    unsigned int channelID;
    char buffer[BUF_LEN];
    ssize_t bytes_read;

    if (argc != 3) {
        perror("Invalid number of arguments: <device file> <channel id>\n");
        exit(1);
    }

    fd = open(argv[1], O_RDONLY);
    if (fd < 0) {
        perror("Can't open device file\n");
        exit(1);
    }

    channelID = atoi(argv[2]);
    if (ioctl(fd, MSG_SLOT_CHANNEL, channelID) < 0) {
        perror("Failed to set channel ID using ioctl\n");
        close(fd);
        exit(1);
    }
    
    bytes_read = read(fd, buffer, BUF_LEN);
    if (bytes_read < 0) {
        perror("Error reading from device");
        close(fd);
        exit(1);
    }

    close(fd);

    if (write(STDOUT_FILENO, buffer, bytes_read) != bytes_read) {
        perror("Failed to write to message to stdout\n");
        close(fd);
        exit(1);
    }

    exit(0);
}

/*
Resources:
Recitations 5+6 - provided files
*/