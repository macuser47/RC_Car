import cv2
import time
import requests
from threading import Thread
import sys

cam = cv2.VideoCapture(1)
ret, frame = cam.read()

time.sleep(0.5)

current_frame = frame
current_image = cv2.imencode(".jpg", current_frame)[1].tostring()
tick = 0
start = time.time()

def read():
    global current_frame, tick
    while True:
        _, current_frame = cam.read()

def encode():
    global current_image, tick
    while True:
        current_image = cv2.imencode(".jpg", current_frame)[1].tostring()
        tick += 1

def post():
    global tick
    while True:
        requests.post("http://" + sys.argv[1] + "/mjpg", data=current_image)
        #time.sleep(1.0 / 30)

t = [Thread(target=read), Thread(target=encode), Thread(target=post)]
for th in t: th.daemon = True
for th in t: th.start()

while True:
    if (time.time() - start) != 0:
        fps = float(tick) / (time.time() - start)
    print("FPS: {}".format(fps))
    if (time.time() - start) > 2.0:
        start = time.time()
        tick = 0
#print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
