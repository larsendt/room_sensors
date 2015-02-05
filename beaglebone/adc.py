#!/usr/bin/env python

import os
import time

ADC_PATH = "/sys/devices/ocp.2/helper.14"

def get(n):
    assert 0 <= n <= 7, "ADC number must be between 0 and 7"

    with open(os.path.join(ADC_PATH, "AIN%d" % n), "r") as f:
        return int(f.read())


if __name__ == "__main__":
    c = 0
    start = time.time()

    try:
        while True:
            c += 1
            print "=" * get(0)
            time.sleep(0.1)
    except:
        pass

    elapsed = time.time() - start
    print c / elapsed, "per second"
