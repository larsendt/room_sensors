#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#include "clap_detector.h"
#include "stepper.h"

#define CLAP_WARNINGS
#define ftime(t) ((double)t.tv_sec + (t.tv_nsec / 1e9))

int main(void) {
    clap_detector d;
    start_clap_thread(&d);

    stepper_control s;
    start_stepper_thread(&s);

    int clapcount = 0;
    while(1) {
        if(d.has_error) {
            printf("d has error!\n");
            break;
        }
        else if(d.last_clap > 0) {
            d.last_clap = 0;
            clapcount += 1;
            printf("clap!\n");
            s.enabled = !s.enabled;
        }
    }
    stop_clap_thread(&d);
    stop_stepper_thread(&s);
    return 0;
}
