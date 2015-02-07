#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define ADC_FILE "/sys/devices/ocp.2/helper.14/AIN_"

int adc_read(int adc_idx, int *ok) {
    if(adc_idx < 0 || adc_idx > 7) {
#ifdef CLAP_WARNINGS
        fprintf(stderr, "error: adc_idx must be between 0 and 7\n");
#endif
        *ok = 0;
        return -1;
    }

    char adc_file[48];
    char adc_value[8];

    memset(adc_file, 0, sizeof(adc_file));
    memset(adc_value, 0, sizeof(adc_value));

    memcpy(adc_file, ADC_FILE, strlen(ADC_FILE)+1);

    // replace the last _ in the file path with a char corresponding to the
    // specified adc_idx 
    adc_file[strlen(adc_file)-1] = adc_idx + 48;

    FILE *f = fopen(adc_file, "r");

    if(!f) {
#ifdef CLAP_WARNINGS
        fprintf(stderr, "error: adc file '%s' was not found\n", adc_file);
#endif
        *ok = 0;
        return -1;
    }

    fread(adc_value, 1, sizeof(adc_value)-1, f);
    fclose(f);
    *ok = 1;
    return atoi(adc_value);
}

double adc_norm(int adc_idx, int max_value, int *ok) {
    return adc_read(adc_idx, ok) / (double) max_value;
}
