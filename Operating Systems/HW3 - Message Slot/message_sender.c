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
    
    if (argc != 4) {
        perror("Invalid number of arguments: <device file> <channel id> <message>\n");
        exit(1);
    }

    fd = open(argv[1], O_WRONLY);
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

    if (write(fd, argv[3], strlen(argv[3])) != strlen(argv[3])) {
        perror("Failed to write complete message to device\n");
        close(fd);
        exit(1);
    }

    close(fd);
    exit(0);
}

/*
Resources:
Recitations 5+6 - provided files
*/