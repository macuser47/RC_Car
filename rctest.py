import cv2
import time
import requests
from threading import Thread
import sys

cam = cv2.VideoCapture(0)
ret, frame = cam.read()

time.sleep(0.5)

current_frame = frame
current_image = cv2.imencode(".jpg", current_frame)[1].tostring()

def read():
    global current_frame
    while True:
        _, current_frame = cam.read()

def encode():
    global current_image
    while True:
        current_image = cv2.imencode(".jpg", current_frame)[1].tostring()

def post():
    while True:
        requests.post("http://" + sys.argv[1] + "/mjpg", data=current_image)
        time.sleep(1.0 / 30)

while True:
    t = [Thread(target=read), Thread(target=encode), Thread(target=post)]
    for th in t: th.daemon = True
    for th in t: th.start()
    #print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
