#ifndef _CLAP_DETECTOR_H
#define _CLAP_DETECTOR_H

// read 'window_size' samples, and then return the max amplitude of the waveform
double window_max_amplitude(unsigned int window_size, int *ok);

#endif
