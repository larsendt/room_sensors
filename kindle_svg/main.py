#!/usr/bin/env python

import svgwrite
import random
import math

DEVICE_SIZE = (758, 1024)
MARGIN = 25
HEADER = "font-size: 40pt"

def render_chart(dwg, points, position, size):
    tl = position
    tr = position[0] + size[0], position[1]
    bl = position[0], position[1] + size[1]
    br = position[0] + size[0], position[1] + size[1]
    dwg.add(dwg.line(start=tl, end=tr, stroke="black"))
    dwg.add(dwg.line(start=tr, end=br, stroke="black"))
    dwg.add(dwg.line(start=br, end=bl, stroke="black"))
    dwg.add(dwg.line(start=bl, end=tl, stroke="black"))
    
    xsize = size[0] / float(len(points) - 1)
    ymin = min(points)
    ymax = max(points)
    ydomain = float(ymax - ymin)
    for i in range(0, len(points)-1):
        ystart = (((points[i] - ymin) / ydomain) * size[1]) + position[1]
        ystop = (((points[i+1] - ymin) / ydomain) * size[1]) + position[1]
        xstart = (xsize * i) + MARGIN
        xstop = (xsize * (i+1)) + MARGIN
        start = (xstart, ystart)
        stop = (xstop, ystop)
        dwg.add(dwg.line(start=start, end=stop, stroke="black"))
        


dwg = svgwrite.Drawing('test.svg', size=DEVICE_SIZE)
dwg.add(dwg.rect(insert=(0, 0), size=DEVICE_SIZE, fill='white'))
dwg.add(dwg.text('Test', insert=(25, 60), fill='black', style=HEADER))


points = map(lambda x: math.sin(x*0.25), range(0, 100))

render_chart(dwg, points, (25, 100), (250, 250))

dwg.save()
