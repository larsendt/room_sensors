#!/usr/bin/python

# open a microphone in pyAudio and listen for taps

import pyaudio
import struct
import math
import time

INITIAL_TAP_THRESHOLD = 0.005
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 16000
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 30.0/INPUT_BLOCK_TIME
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME

WAITING = 1
FIRST_CLAP = 2
SECOND_CLAP = 3

MIN_CLAP_INTRA_SEPARATION = 0.15
MAX_CLAP_INTRA_SEPARATION = 0.75
MIN_CLAP_INTER_SEPARATION = 1.0


def get_rms( block ):
    # RMS amplitude is defined as the square root of the
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into
    # a string of 16-bit samples...

    # we will get one short out for each
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768.
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

class TapTester(object):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisycount = MAX_TAP_BLOCKS+1
        self.quietcount = 0
        self.errorcount = 0
        self.last_clap = 0
        self.state = WAITING

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None
        for i in range( self.pa.get_device_count() ):
            devinfo = self.pa.get_device_info_by_index(i)
            print( "Device %d: %s"%(i,devinfo["name"]) )

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def open_mic_stream( self ):
        device_index = self.find_input_device()
        print FORMAT, CHANNELS, RATE, INPUT_FRAMES_PER_BLOCK

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError, e:
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )
            return

        amplitude = get_rms( block )
        if self.state == WAITING:
            if amplitude > self.tap_threshold:
                print "state = FIRST_CLAP"
                self.state = FIRST_CLAP
                self.last_clap = time.time()
        elif self.state == FIRST_CLAP:
            diff = time.time() - self.last_clap
            if diff < MAX_CLAP_INTRA_SEPARATION:
                if amplitude > self.tap_threshold and diff > MIN_CLAP_INTRA_SEPARATION:
                    print "state = SECOND_CLAP"
                    print "="*80
                    print " "*30, "TRIGGER"
                    print "="*80
                    self.state = SECOND_CLAP
                    self.last_clap = time.time()
                elif amplitude > self.tap_threshold:
                    print "too soon:", diff
            else:
                print "state = WAITING"
                self.state = WAITING
        elif self.state == SECOND_CLAP:
            if (time.time() - self.last_clap) > MIN_CLAP_INTER_SEPARATION:
                print "state = WAITING"
                self.state = WAITING
        else:
            print "unknown state!", self.state




if __name__ == "__main__":
    tt = TapTester()

    while True:
        tt.listen()
