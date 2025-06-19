#ifndef MESSAGE_SLOT_H
#define MESSAGE_SLOT_H

#include <linux/ioctl.h>

#define MAJOR_NUM 235

#define MSG_SLOT_CHANNEL _IOW(MAJOR_NUM, 0, unsigned int)

#define DEVICE_NAME "message_slot"
#define BUF_LEN 128
#define SUCCESS 0

typedef struct channelNode {
    unsigned int channelId;
    char msg[BUF_LEN];
    int lenMsg;
    struct channelNode* next;
} channelNode;

typedef struct channelList {
    channelNode* head;
} channelList;

#endif

/*
Resources:
# Recitation 5+6 - provided header file chardev.h (in CHARDEV2) and slides
# See reseources in mesage_slot.c, some of them are relevant here as well
*/