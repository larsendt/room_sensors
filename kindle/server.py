#!/usr/bin/env python
import zmq
import json
import traceback

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")


def backlight_route(params):
    if params["on"]:
        if "room_brightness" in params:
            print "Room brightness is", params["room_brightness"]
        print "Backlight turned on"
    else:
        print "Backlight turned off"


def display_route(params):
    data = params["image"]
    print "Image data:", data[:10] + "..." + data[-10:]
    

route = {"backlight":backlight_route,
         "display":display_route}

while True:
    msg = socket.recv()
    try:
        obj = json.loads(msg)
        route[obj["target"]](obj["params"])
        socket.send("ok")
    except ValueError as e:
        print traceback.format_exc(e)
        socket.send(json.dumps({"err":str(e)}))
    except KeyError as e:
        print traceback.format_exc(e)
        errmsg = "missing key " + str(e)
        socket.send(json.dumps({"err":errmsg}))
        

