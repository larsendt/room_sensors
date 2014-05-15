#ifndef _CLAP_DETECTOR_H
#define _CLAP_DETECTOR_H

#include <pthread.h>

typedef struct clap_detector {
    int last_clap;
    int has_error;
    int running;
    pthread_t thread_handle;
} clap_detector;


// read 'window_size' samples, and then return the max amplitude of the waveform
double window_max_amplitude(unsigned int window_size, int *ok);
int wait_for_clap();

void start_clap_thread(clap_detector *d);
void stop_clap_thread(clap_detector *d);


#endif
