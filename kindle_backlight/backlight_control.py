#!/usr/bin/env python

import requests

BACKLIGHT_FILE = "/sys/devices/system/fl_tps6116x/fl_tps6116x0/fl_intensity"
ROOM_BRIGHTNESS_URL = "http://localhost/sensors/brightness"

def set_backlight(value):
    with open(BACKLIGHT_FILE, "r") as f:
        f.write(str(value))


def get_backlight():
    with open(BACKLIGHT_FILE, "r") as f:
        return int(f.read())


def get_room_brightness():
    try:
        r = requests.get(ROOM_BRIGHTNESS_URL)
        if r.status_code == 200:
            brightness = float(r.text)
        else:
            brightness = 1.0
    except:
        brightness = 1.0

    return brightness


def scale_backlight(on):
    if on:
        brightness = get_room_brightness()
        set_backlight(100)
    else:
        set_backlight(0)




