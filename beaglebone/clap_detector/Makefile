CFLAGS = -Wall -g -std=gnu99

all: clap

clap: main.c libclap.so
	gcc $(CFLAGS) main.c -lclap -o clap -lrt

libclap.so: clap_detector.o adc.o
	gcc -shared -fPIC clap_detector.o adc.o -o libclap.so -lrt

clap_detector.o: clap_detector.c clap_detector.h
	gcc $(CFLAGS) -fPIC -c clap_detector.c -o clap_detector.o -lrt

adc.o: adc.c adc.h
	gcc $(CFLAGS) -fPIC -c adc.c -o adc.o -lrt


clean:
	rm -f *.o clap libclap.so
