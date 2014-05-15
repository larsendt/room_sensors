#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#include "adc.h"
#include "clap_detector.h"

#define CLAP_WARNINGS
#define ftime(t) ((double)t.tv_sec + (t.tv_nsec / 1e9))

int main(void) {
    while(1) {
        wait_for_clap();
        printf("double clap!\n");
    }
    return 0;
}
