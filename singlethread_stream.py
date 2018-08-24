import cv2
import time
import requests
from threading import Thread
from multiprocessing import Process, Manager
import sys

cam = cv2.VideoCapture(0)
ret, frame = cam.read()

time.sleep(0.5)

while True:
    start = time.time()

    ret, frame = cam.read()
    if not ret:
        print("FRAME READ FAILURE")
        continue
    mjpg = cv2.imencode(".jpg", frame)[1].tostring()
    requests.post("http://" + sys.argv[1] + "/mjpg", data=mjpg, headers={"timestamp": str(time)})

    if (time.time() - start) != 0:
        fps = 1. / (time.time() - start)
    print("FPS: {}".format(fps))