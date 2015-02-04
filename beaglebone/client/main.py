#!/usr/bin/env python

import scheduler
import svg_gen
import time

def upload_svg():
    print "upload"

def signal_backlight():
    print "backlight"


def main_loop():
    s = scheduler.Scheduler()
    s.add_function(upload_svg, 5)
    s.add_function(signal_backlight, 30)
    while True:
        try:
            s.ping()
        except:
            pass
        time.sleep(0.1)



if __name__ == "__main__":
    main_loop()
