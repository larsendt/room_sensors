#!/usr/bin/env python

from flask import Flask, Response, request
import svg_display
import base64

app = Flask(__name__)

@app.route("/control")
def sensors():
    r = json.dumps(["backlight", "display"])
    return Response(r, mimetype="application/json")

@app.route("/control/backlight", methods=["POST"])
def backlight():
    if "level" in request.form:
        backlight_level = int(request.form["level"])
        return Response("ok", mimetype="application/json")
    else:
        return "'level' required", 400


@app.route("/control/display", methods=["POST"])
def display():
    if "svg" in request.form:
        svgdata = base64.b64decode(request.form["svg"])
        svg_display.display(svgdata)
        return Response("ok", mimetype="application/json")
    else:
        return "'svg' required", 400


if __name__ == "__main__":
    app.run("localhost", 8080)
