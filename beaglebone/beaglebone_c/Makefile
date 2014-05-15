CFLAGS = -Wall -g -std=gnu99 -pthread

all: beaglebone 

beaglebone: main.c libutil.so
	gcc $(CFLAGS) main.c -fPIC -o beaglebone -lrt -lutil

libutil.so: clap_detector.o adc.o gpio.o stepper.o
	gcc -shared -fPIC clap_detector.o adc.o gpio.o stepper.o -o libutil.so -lrt

clap_detector.o: clap_detector.c clap_detector.h
	gcc $(CFLAGS) -fPIC -c clap_detector.c -o clap_detector.o -lrt

stepper.o: stepper.c stepper.h
	gcc $(CFLAGS) -fPIC -c stepper.c -o stepper.o -lrt

adc.o: adc.c adc.h
	gcc $(CFLAGS) -fPIC -c adc.c -o adc.o -lrt

gpio.o: gpio.c gpio.h
	gcc $(CFLAGS) -fPIC -c gpio.c -o gpio.o -lrt

clean:
	rm -f *.o beaglebone libutil.so
