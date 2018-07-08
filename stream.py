import cv2
import time
import requests
from threading import Thread
from multiprocessing import Process, Manager
import sys

cam = cv2.VideoCapture(0)
ret, frame = cam.read()

time.sleep(0.5)

def read():
    return cam.read()[1]

def process(img, time):
    manager = Manager()
    d = manager.list(range(1))
    proc = Process(target=encode, args=(img, d))
    proc.daemon = True
    proc.start()
    proc.join()
    encoded_image = d[0]

    t = Thread(target=post, args=(encoded_image, time))
    t.daemon = True
    t.start()

def encode(img, d):
    d[0] = cv2.imencode(".jpg", img)[1].tostring()


def post(img, time):
    requests.post("http://" + sys.argv[1] + "/mjpg", data=img, headers={"timestamp": str(time)})
        #time.sleep(1.0 / 30)


while True:
    start = time.time()

    img = read()

    t = Thread(target=process, args=(img, start))
    t.daemon = True
    t.start()

    if (time.time() - start) != 0:
        fps = 1 / (time.time() - start)
    print("FPS: {}".format(fps))
#print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
