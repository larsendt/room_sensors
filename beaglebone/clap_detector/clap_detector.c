#include <stdlib.h>
#include <stdio.h>
#include "adc.h"

#define ADC_MAX 4096
#define ADC_PIN 0

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
