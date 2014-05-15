#ifndef _ADC_H_
#define _ADC_H_

// returns the raw ADC value for the ADC pin specified by 'adc_idx'
// 'adc_idx' must be between 0 and 7
// ok is 1 if everything is ok, 0 otherwise (in which case the value should not
// be trusted)
int adc_read(int adc_idx, int *ok);

// convenience function that returns the adc on a 0-1 scale
// for 'ok', see above
double adc_norm(int adc_idx, int max_value, int *ok);

#endif
