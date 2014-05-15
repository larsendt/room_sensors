#include "stepper.h"
#include "gpio.h"
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>

#define ftime(t) ((double)t.tv_sec + (t.tv_nsec / 1e9))

void *_stepper_main_function(void *params);

void start_stepper_thread(stepper_control *s) {
    s->dir = 0;
    s->enabled = 0;
    int ok = pthread_create(&(s->thread_handle), NULL, &_stepper_main_function, s);
    if(ok != 0) {
        fprintf(stderr, "Error on stepper thread start!\n");
        fprintf(stderr, "%s\n", strerror(errno));
        s->has_error = 1;
    }
    s->has_error = 0;
}


void stop_stepper_thread(stepper_control *s) {
    s->enabled = 0;
    pthread_cancel(s->thread_handle);
}

void *_stepper_main_function(void *params) {
    stepper_control *s = params;
    gpio g;
    gpio_init(&g, 30, WRITE);

    struct timespec samplestart;
    struct timespec samplestop;
    struct timespec loopstart;
    struct timespec loopstop;

    clock_gettime(CLOCK_MONOTONIC, &samplestart);
    clock_gettime(CLOCK_MONOTONIC, &loopstart);

    int on = 0;
    double min_diff = 0.00005;

    while(1) {
        if(s->enabled) {
            clock_gettime(CLOCK_MONOTONIC, &samplestop);
            if(ftime(samplestop) - ftime(samplestart) > min_diff) {
                clock_gettime(CLOCK_MONOTONIC, &samplestart);

                if(on) {
                    gpio_set_value(&g, HIGH);
                    on = 0;
                }
                else {
                    gpio_set_value(&g, LOW);
                    on = 1;
                }
            }
        }
        else {
            gpio_set_value(&g, LOW);
        }
    }
}
