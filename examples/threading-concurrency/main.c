#include <stdio.h>
#include <string.h>

#include "thread.h"
#include "ztimer.h"

/* Include the mutex header here */
#include "mutex.h"

/* Declare here the struct used to handle the buffer and the mutex */
typedef struct {
    char buffer[128];
    mutex_t lock;
} data_t;
static data_t data;

/* Allocate the writer stack here */
static char writer_stack[THREAD_STACKSIZE_MAIN];

static void *writer_thread(void *arg)
{
    (void) arg;

    while (1) {
        /* acquire the lock here */
        mutex_lock(&data.lock);


        /* slowly print some content in the buffer here */
        size_t p = sprintf(data.buffer, "start: %"PRIu32"", ztimer_now(ZTIMER_MSEC));
        ztimer_sleep(ZTIMER_MSEC, 200);
        p += sprintf(&data.buffer[p], " - end: %"PRIu32"", ztimer_now(ZTIMER_MSEC));


        /* release the mutex here */
        mutex_unlock(&data.lock);


        ztimer_sleep(ZTIMER_MSEC, 100);
    }

    return NULL;
}

int main(void)
{
    puts("RIOT application with thread safe concurrency");

    /* Create the write thread here */
    thread_create(writer_stack, sizeof(writer_stack), THREAD_PRIORITY_MAIN - 1, 0, writer_thread, NULL, "writer thread");


    while (1) {
        /* safely read the content of the buffer here */
        mutex_lock(&data.lock);
        printf("%s\n", data.buffer);
        mutex_unlock(&data.lock);


        ztimer_sleep(ZTIMER_MSEC, 200);
    }

    return 0;
}