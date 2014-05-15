#include <stdio.h>
#include <time.h>
#define WARNINGS
#include "gpio.h"

#define ftime(t) ((double)t.tv_sec + (t.tv_nsec / 1e9))

int main(void) {
    gpio g;
    gpio_init(&g, 30, WRITE);

    struct timespec samplestart;
    struct timespec samplestop;
    struct timespec loopstart;
    struct timespec loopstop;

    int count = 0;
    int on = 0;
    int maxcount = 100000;
    double min_diff = 0.0005;
    clock_gettime(CLOCK_MONOTONIC, &samplestart);
    clock_gettime(CLOCK_MONOTONIC, &loopstart);
    while(1) {
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

            count += 1;
        }

        /*
        clock_gettime(CLOCK_MONOTONIC, &loopstop);
        if(ftime(loopstop) - ftime(loopstart) > 1.0) {
            min_diff /= 1.1;
            printf("1 second elapsed - min diff is now %f\n", min_diff);
            clock_gettime(CLOCK_MONOTONIC, &loopstart);
        }
        */
    }

    /*diff = ftime(stop) - ftime(start);
    printf("elapsed: %f\n", diff);
    printf("samples/sec: %f\n", (sample_count / diff));
    */

    return 0;
}
