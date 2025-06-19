#include <stddef.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <threads.h>

//========================= STRUCT DEFINITIONS =========================
typedef struct QueueNode {
    void* data;
    struct QueueNode* next;
} QueueNode;

typedef struct Queue {
    QueueNode* head;
    QueueNode* tail;
    size_t cntVisited; // "it is OK if the returned number is not exact due to concurrent threads taking their place" - No need to be atomic
    mtx_t queueLock;
} Queue;

typedef struct ThreadNode {
    cnd_t condition;
    struct ThreadNode* next;
} ThreadNode;

typedef struct ThreadList {
    ThreadNode* head;
    ThreadNode* tail;
} ThreadList;

//========================= FUNCTION DECLARATIONS =========================
void initQueue(void);
void destroyQueue(void);
void enqueue(void* item);
void* dequeue(void);
bool tryDequeue(void** item);
size_t visited(void);

//========================= GLOBAL VARIABLES =========================
static Queue* queue = NULL;
static ThreadList* waitingThreads = NULL;

//======================= ADDITIONAL FUNCTIONS =======================
static void freeQueue(void)
{
    QueueNode* tempNode; // Free all nodes in the queue
    while(queue->head != NULL)
    {
        tempNode = queue->head;
        queue->head = queue->head->next;
        free(tempNode);
    }
}

static void freeThreadsList(void)
{
    ThreadNode* tempNode;
    while(waitingThreads->head != NULL)
    {
        tempNode = waitingThreads->head;
        waitingThreads->head = waitingThreads->head->next;
        cnd_destroy(&tempNode->condition);
        free(tempNode);
    }
}

static void addToQueue(QueueNode* newNode)
{
    if (queue->head == NULL) { // queue is empty
        queue->head = newNode;
    } else {
        queue->tail->next = newNode;
    }
    queue->tail = newNode;
}

static void addWaitingThread(ThreadNode* newThread)
{
    if (waitingThreads->head == NULL) { // list is empty
        waitingThreads->head = newThread;
    } else {
        waitingThreads->tail->next = newThread;
    }
    waitingThreads->tail = newThread;
}

static void* removeFromQueue(void)
{
    QueueNode* tempNode = queue->head;
    void* item = tempNode->data; // Save the data before freeing the node
    queue->head = queue->head->next;
    free(tempNode);

    if (queue->head == NULL) { // queue is empty - set tail to NULL
        queue->tail = NULL;
    }

    return item;
}

//========================= FUNCTION DEFINITIONS =========================
void initQueue(void) {
    queue = (Queue*)malloc(sizeof(Queue));
    queue->head = NULL;
    queue->tail = NULL;
    queue->cntVisited = 0;
    mtx_init(&queue->queueLock, mtx_plain);

    waitingThreads = (ThreadList*)malloc(sizeof(ThreadList));
    waitingThreads->head = NULL;
    waitingThreads->tail = NULL;
}

void destroyQueue(void) {
    // "destroyQueue() will run solo" - no need to actiavte lock
    freeQueue();
    mtx_destroy(&queue->queueLock);
    free(queue);
    queue = NULL; // Prevent dangling pointer and prepare for next init

    // Because no other queue operation are active, this means that there are no threads waiting, otherwise some action would occur.
    // This is why we can free all waiting threads (this should be empty, but it's better to check anyway)
    freeThreadsList();
    free(waitingThreads);
    waitingThreads = NULL; // Prevent dangling pointer and prepare for next init    
}

void enqueue(void* item) {
    QueueNode* newNode = (QueueNode*)malloc(sizeof(QueueNode));
    newNode->data = item;
    newNode->next = NULL;

    mtx_lock(&queue->queueLock);

    addToQueue(newNode);

    if (waitingThreads->head != NULL) { // There is a thread waiting
        ThreadNode* threadToWake = waitingThreads->head; // Choose the first thread in the list
        waitingThreads->head = waitingThreads->head->next; // Remove the thread from the list
        if (waitingThreads->head == NULL) { // list is empty
            waitingThreads->tail = NULL;
        }
        
        cnd_signal(&threadToWake->condition); // Wake up the thread

        cnd_destroy(&threadToWake->condition); // Free the condition variable and thread node
        free(threadToWake);
    }

    mtx_unlock(&queue->queueLock);
}

void* dequeue(void) {
    mtx_lock(&queue->queueLock); // Recitation said that mutex must be locked before condition variable

    while (queue->head == NULL) { // Wait until queue is not empty
        ThreadNode* currThread = (ThreadNode*)malloc(sizeof(ThreadNode));
        cnd_init(&currThread->condition);
        currThread->next = NULL;
        
        addWaitingThread(currThread);

        cnd_wait(&currThread->condition, &queue->queueLock); // Wait until woken up by enqueue
        // No need to destroy the condition variable and free the memory here
        // as it was done in the enqueue function
    }

    void* item = removeFromQueue();
    queue->cntVisited++; // protected by lock to avoid race condition
    
    mtx_unlock(&queue->queueLock);

    return item;
}

bool tryDequeue(void** item) {
    mtx_lock(&queue->queueLock);

    if (queue->head == NULL) {
        mtx_unlock(&queue->queueLock); // don't block if queue is empty
        return false;
    }

    QueueNode* tempNode = queue->head;
    *item = tempNode->data;
    queue->head = queue->head->next;
    
    if (queue->head == NULL) { // queue is empty
        queue->tail = NULL;
    }

    free(tempNode);

    queue->cntVisited++; // protected by lock to avoid race condition

    mtx_unlock(&queue->queueLock);

    return true;
}

size_t visited(void) {
    return queue->cntVisited;
}

/*
Resources:
Recitation 9

conditions:
https://www.ibm.com/docs/en/aix/7.2?topic=c-cnd-broadcast-cnd-destroy-cnd-init-cnd-signal-cnd-timedwait-cnd-wait-subroutine
https://moodle.tau.ac.il/mod/forum/discuss.php?d=34944 = cnd does not guarantee wake-up order

mutex:
https://www.ibm.com/docs/en/aix/7.2?topic=m-mtx-destroy-mtx-init-mtx-lock-mtx-timedlock-mtx-trylock-mtx-unlock-subroutine



ChatGPT (is student > no money > no account > no link > copy-paste of chat):

i am implementing a queue that needs to be thread safe. i want threads to be woken up in FIFO order but cnd_signal does not guarantee this. how can i assure that my threads wake up in order? don't provide code and be brief
ChatGPT said:
ChatGPT
To ensure threads wake up in FIFO order, use a condition variable along with a queue to track the waiting threads. Each thread should be assigned a unique identifier or sequence number. When signaling threads, you can use a mechanism like a priority queue or a sequence number to wake up threads in the correct order, ensuring FIFO behavior.


You said:
but cnd_signal does not accept any other argument besides a condition. how can i pass the unique identifier?
ChatGPT said:
ChatGPT
You can use a condition variable in combination with a shared data structure, like a queue or a list, to manage the order of threads. Instead of passing a unique identifier directly to cnd_signal, you can maintain the order by storing thread-specific information (e.g., a unique ID or a timestamp) in a structure that the threads can check when they are awakened. Use cnd_signal to wake the next thread in the desired order, ensuring FIFO behavior by having threads signal the next one explicitly when they finish their work.


You said:
so basically keep a FIFO queue of threads, and each thread has it's own condition? then i do cnd_signal(firstThread->condition)?
ChatGPT said:
ChatGPT
Yes, exactly. You can maintain a FIFO queue of threads, and each thread will have its own associated condition variable. When a thread finishes its task and it's ready to signal the next thread, you can call cnd_signal on the condition variable of the next thread in the queue. This way, you ensure that threads wake up in the correct order.

Here's a high-level breakdown:

Queue of threads: Maintain a FIFO queue (e.g., a linked list or other data structure) of threads that are waiting to proceed.
Thread-specific conditions: Each thread has its own condition variable (e.g., thread_cond_t).
Signaling: When it's time for a thread to wake up, you signal the next thread in the queue using cnd_signal(nextThread->condition).
Synchronization: Threads will wait on their own condition variable until they are signaled in the correct order.
This ensures proper FIFO behavior while maintaining thread safety.


You said:
when i finish with a thread (it woke up and now takes the queue's lock) i need to free the node that saved it. do i also need to destroy the condition manually?
ChatGPT said:
ChatGPT
Yes, when you're finished with a thread and you free the node that saved it, you should manually destroy the condition variable associated with that thread to avoid memory leaks or dangling resources. In many implementations, condition variables are initialized with a specific attribute or resource, and it's good practice to clean them up after they're no longer needed.

So, after you signal and allow the thread to take the queue's lock and process its task, once you're done, you should:

Destroy the condition variable: Use cnd_destroy to release any resources associated with the thread's condition variable.
Free the node: After destroying the condition variable, safely free the memory associated with the node that contained the thread's condition variable and other data.
This cleanup step ensures that resources are properly freed, and you don't risk leaking memory or leaving unused synchronization primitives around.


You said:
so just like every malloc requires a free to prevent memory leaks, every cnd_init requires cnd_destroy yeah?
ChatGPT said:
ChatGPT
Yes, that's correct! Just as every malloc requires a corresponding free to prevent memory leaks, every cnd_init (or equivalent initialization) requires a corresponding cnd_destroy to properly clean up the resources associated with the condition variable.

Failing to call cnd_destroy after you're done with a condition variable can lead to resource leaks, just as forgetting to free dynamically allocated memory can lead to memory leaks. Always ensure that you destroy the condition variable once it is no longer needed.
*/