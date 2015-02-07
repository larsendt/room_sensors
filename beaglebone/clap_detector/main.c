#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#include "adc.h"
#include "clap_detector.h"

#define CLAP_WARNINGS
#define ftime(t) ((double)t.tv_sec + (t.tv_nsec / 1e9))

int main(void) {
    /*
    int ok = 0;
    double maxamp = window_max_amplitude(25, &ok);
    if(!ok) {
        fprintf(stderr, "ok was not 1, something went wrong...\n");
    }
    printf("%f\n", maxamp);
    */

    int ok = 0;
    struct timespec start;
    struct timespec stop;
    int sample_count = 100000;

    clock_gettime(CLOCK_MONOTONIC, &start);
    for(int i = 0; i < sample_count; i++) {
        window_max_amplitude(10, &ok);
    }
    clock_gettime(CLOCK_MONOTONIC, &stop);

    double diff = ftime(stop) - ftime(start);
    printf("elapsed: %f\n", diff);
    printf("samples/sec: %f\n", (sample_count / diff));

    return 0;
}
