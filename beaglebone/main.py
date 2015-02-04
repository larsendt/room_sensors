#!/usr/bin/env python

import scheduler
import svg_gen
import time
import json
import zmq
import base64
import traceback
import random

def main_loop():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5556")
    print "Connected to server"

    def upload_svg():
        print "Generating svg"
        svg = svg_gen.get_svg()
        obj = {"target":"display", 
               "params": {"image": base64.b64encode(svg)}}
        s = json.dumps(obj)
        socket.send(s)
        msg = socket.recv()
        print msg

    def signal_backlight():
        print "Setting backlight"
        obj = {"target":"backlight", 
               "params":{"on":random.choice((True, False)),
                         "room_brightness":random.uniform(0, 1)}}
        s = json.dumps(obj)
        socket.send(s)
        msg = socket.recv()
        print msg

    s = scheduler.Scheduler()
    s.add_function(upload_svg, 5)
    s.add_function(signal_backlight, 30)
    while True:
        try:
            s.ping()
        except Exception as e:
            print traceback.format_exc(e)
            break
        time.sleep(0.1)



if __name__ == "__main__":
    main_loop()
