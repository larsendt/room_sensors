#!/usr/bin/env python

from flask import Flask, Response

app = Flask(__name__)

@app.route("/sensors")
def sensors():
    r = json.dumps(["brightness", "humidity"])
    return Response(r, mimetype="application/json")

@app.route("/sensors/brightness")
def brightness():
    return Response("0.75", mimetype="application/json")

@app.route("/sensors/humidity")
def humidity():
    return Response("44", mimetype="application/json")



if __name__ == "__main__":
    app.run("localhost", 8080)
