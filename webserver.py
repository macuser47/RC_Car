from flask import Flask, render_template, request, Response
import json
import time
import sys

app = Flask(__name__)

input = {
    "W" : False,
    "A" : False,
    "S" : False,
    "D" : False
}
last_car_time = time.time()
dc_timeout = 0.25
STREAM_FRAMERATE = 30

STREAM_SAMPLE_LENGTH = 30
last_mjpg_time = time.time()
mjpg_tick = 0

with open("static/tesla.jpg", "rb") as f:
    mjpg = f.read()

with open("car.key") as f:
    car_key = f.read()

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/fuck",  methods=["POST"])
def update_input():
    global input
    if not request.method == "POST":
        return "Fuck off ya fuckr"
    if not request.json["key"] == car_key:
        return "They key don't fit pardner"
    
    input = request.json
    return "False" if timed_out() else "True"

@app.route("/get_input", methods=["GET"])
def get_input():
    return json.dumps(input)

@app.route("/mjpg", methods=["POST"])
def update_stream():
    global mjpg, mjpg_tick, last_mjpg_time
    if not request.method == "POST":
        return "FUCC YE"
    mjpg = request.get_data()
    mjpg_tick += 1
    fps = float(mjpg_tick) / (time.time() - last_mjpg_time)
    if mjpg_tick > STREAM_SAMPLE_LENGTH:
        last_mjpg_time = time.time()
        mjpg_tick = 0
    f_print("STREAM FPS: {}".format(fps))
    if request.headers["timestamp"]:
        latency = time.time() - float(request.headers["timestamp"])
        f_print("STREAM LATENCY: {}".format(latency))
    return "EEEE"
    
@app.route("/ping", methods=["GET"])
def ping():
    global last_car_time
    last_car_time = time.time()
    return "Thank you for your ping. It is appreciated"

def timed_out():
    return time.time() - last_car_time > dc_timeout

@app.route("/stream.mjpg", methods=["GET"])
def render_stream():
    return Response(
		generate_stream(),
		mimetype="multipart/x-mixed-replace; boundary=jpgboundary"
    )
 
def generate_stream():
    global mjpg
    header = "--jpgboundary\nContent-Type: image/jpeg\n\n"
    while True:
        #mjpg could be bytes or string type, opencv vs file.read()
        if mjpg is str:
            yield header + mjpg
        else:
            yield header.encode() + mjpg
        time.sleep(1 / float(STREAM_FRAMERATE))

def f_print(string):
    print(string, file=sys.stderr)

if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)