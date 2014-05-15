#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include "adc.h"
#include "clap_detector.h"

#define ADC_MAX 4096
#define ADC_PIN 0

void *_clap_poll_function(void *params);

void start_clap_thread(clap_detector *d) {
    d->last_clap = -1;
    d->has_error = 0;
    d->running = 0;
    int ok = pthread_create(&(d->thread_handle), NULL, &_clap_poll_function, d);
    if(ok != 0) {
        d->has_error = 1; 
        fprintf(stderr, "Failed to create clap thread\n");
        fprintf(stderr, "%s\n", strerror(errno));
    }
    else {
        d->running = 1;
    }
}


void stop_clap_thread(clap_detector *d) {
    d->last_clap = -1;
    d->has_error = 0;
    d->running = 0;

    pthread_cancel(d->thread_handle);
}


void *_clap_poll_function(void *params) {
    clap_detector *d = params;
    while(1) {
        d->last_clap = wait_for_clap();        
    }
}


double window_max_amplitude(unsigned int window_size, int *ok) {
    double min = 1.0;
    double max = -1.0;

    for(unsigned int i = 0; i < window_size; i++) {
        // since we're reading the raw waveform, "0" is actually at 0.5
        // scale it to a -1 to 1 range
        double sample = (adc_norm(ADC_PIN, ADC_MAX, ok) * 2.0) - 1.0;

        if(sample < min) {
            min = sample;
        }

        if(sample > max) {
            max = sample;
        }
    }

    return max - min;
}

int wait_for_clap() {
    const int min_clap_spacing = 1;
    const int max_clap_spacing = 5;
    const double min_clap_amplitude = 0.1;
    int ok;
    int state = 0;
    int window_count = 0;

    while(1) {
        double amp = window_max_amplitude(50, &ok);
        if(state == 0) {
            if(amp >= min_clap_amplitude) {
                state = 1;
                window_count = 0;
            }
        }
        else if(state == 1) {
            if(window_count > max_clap_spacing) {
                state = 0;
            }
            if(amp >= min_clap_amplitude) {
                if(window_count >= min_clap_spacing && window_count <= max_clap_spacing) {
                    return 1;
                }
            }

            window_count += 1;
        } 
    }
    return 0;
}
