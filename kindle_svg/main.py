#!/usr/bin/env python
# -*- coding: utf-8 -*-

import svgwrite
import random
import math
import arrow
import requests
import json

DEVICE_SIZE = (1024, 758)
MARGIN = 25
HEADER_HEIGHT = 65
HEADER = "font-size: 80pt; text-anchor: middle;"
CHART_TITLE_HEIGHT = 25
CHART_TITLE = "font-size: 20pt; text-anchor: middle;"
CHART_HEIGHT = 250
CHART_MARGIN = 15
MEASUREMENT_HEIGHT = 40
MEASUREMENT = "font-size: 40pt; text-anchor: middle;"
LINE_STYLE = "stroke-width: 2px;"


def render_chart(dwg, points, position, size, title):
    tl = position
    tr = position[0] + size[0], position[1]
    bl = position[0], position[1] + size[1]
    br = position[0] + size[0], position[1] + size[1]
    dwg.add(dwg.line(start=tl, end=tr, stroke="black", style=LINE_STYLE))
    dwg.add(dwg.line(start=tr, end=br, stroke="black", style=LINE_STYLE))
    dwg.add(dwg.line(start=br, end=bl, stroke="black", style=LINE_STYLE))
    dwg.add(dwg.line(start=bl, end=tl, stroke="black", style=LINE_STYLE))

    dwg.add(dwg.text(title, 
                     insert=(bl[0] + (size[0] / 2), position[1] + size[1] + CHART_TITLE_HEIGHT),
                     fill="black",
                     style=CHART_TITLE))
    
    xsize = size[0] / float(len(points) - 1)
    ymin = min(points)
    ymax = max(points)
    ydomain = float(ymax - ymin)
    for i in range(0, len(points)-1):
        ystart = (((points[i] - ymin) / ydomain) * size[1]) + position[1]
        ystop = (((points[i+1] - ymin) / ydomain) * size[1]) + position[1]
        xstart = (xsize * i) + position[0]
        xstop = (xsize * (i+1)) + position[0]
        start = (xstart, ystart)
        stop = (xstop, ystop)
        dwg.add(dwg.line(start=start, end=stop, stroke="black", style=LINE_STYLE))


def render_charts(dwg, data_arrays, titles):
    num_charts = len(data_arrays)
    perchart_w = (DEVICE_SIZE[0] / num_charts)
    ypos = DEVICE_SIZE[1] - CHART_HEIGHT - CHART_TITLE_HEIGHT - MARGIN
    for i, (data, title) in enumerate(zip(data_arrays, titles)):
        xpos = i * perchart_w
        xpos += CHART_MARGIN
        render_chart(dwg, data, (xpos, ypos), (perchart_w - (CHART_MARGIN * 2), CHART_HEIGHT), title)


def render_time(dwg):
    now = arrow.now()
    text = dwg.text(now.format("MMM DD, hh:mm A"), 
                     insert=(DEVICE_SIZE[0]/2, HEADER_HEIGHT + MARGIN), 
                     fill='black', 
                     style=HEADER)
    dwg.add(text)


def render_measurement(dwg, text, y_index, x_offset, y_offset):
    x = ((DEVICE_SIZE[0] - x_offset) / 2) + x_offset
    y = (y_index * MEASUREMENT_HEIGHT) + y_offset
    text = dwg.text(text,
                    insert=(x, y), 
                    fill='black', 
                    style=MEASUREMENT)
    dwg.add(text)


def format_weather(weather_obj):
    obj = weather_obj
    base_str = "Boulder: "

    temp = (obj["main"]["temp"] - 273.15) * (9 / 5.0) + 32
    base_str += "%.1f°F " % temp

    hum = obj["main"]["humidity"]
    base_str += "%d%%RH " % hum

    if "clouds" in obj:
        clouds = obj["clouds"]["all"]
        if clouds == 0:
            base_str += "Clear "
        elif clouds < 75:
            base_str += "Some Clouds "
        else:
            base_str += "Overcast "

    if "rain" in obj:
        rain = obj["rain"]["3h"]
        if rain > 0:
            base_str += "Recent Rain "

    if "snow" in obj:
        snow = obj["snow"]["3h"]
        if snow > 0:
            base_str += "Recent Snow "

    if "wind" in obj:
        wind = obj["wind"]["speed"]
        base_str += " Wind: %.2fm/s " % wind

    return base_str



def render_weather(dwg, position):
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Boulder,us")
    if r.status_code != 200:
        text = "Unknown Weather"
    else:
        obj = json.loads(r.text)
        text = format_weather(obj)

    x = ((DEVICE_SIZE[0] - position[0]) / 2) + position[0]
    y = position[1]

    text_elem = dwg.text(text,
                         insert=(x, y),
                         fill='black',
                         style=MEASUREMENT)
    dwg.add(text_elem)


dwg = svgwrite.Drawing('kindle_display.svg', size=DEVICE_SIZE)
dwg.add(dwg.rect(insert=(0, 0), size=DEVICE_SIZE, fill='white'))

render_time(dwg)

points1 = map(lambda x: math.sin(x*0.1), range(0, 300))
points2 = map(lambda x: math.sin(x*0.05), range(0, 300))
render_charts(dwg, [points1, points2], ["Relative Humidity", "Temperature"])

render_measurement(dwg, "RH: 42%   Temp: 65°F", 1, 0, HEADER_HEIGHT + 25 + MARGIN)

render_weather(dwg, (0, MARGIN + HEADER_HEIGHT + MEASUREMENT_HEIGHT + 100))

dwg.save()
