import cv2
import time
import requests
from threading import Thread
from multiprocessing import Process, Manager
import sys

cam = cv2.VideoCapture(0)
ret, frame = cam.read()

time.sleep(0.5)

current_frame = frame
current_image = cv2.imencode(".jpg", current_frame)[1].tostring()
tick = 0
start = time.time()

def read():
    return cam.read()[1]

def process():
    manager = Manager()
    d = manager.list()
    proc = Process(target=encode, args=(img, d))
    proc.daemon = True
    proc.start()
    proc.join()
    encoded_image = d[0]

    t = Thread(target=post, args=(encoded_image,))
    t.daemon = True
    t.start()

def encode(img, d):
    d[0] = cv2.imencode(".jpg", current_frame)[1].tostring()


def post(img):
        requests.post("http://" + sys.argv[1] + "/mjpg", data=current_image)
        #time.sleep(1.0 / 30)


while True:
    start = time.time()

    img = read()

    t = Thread(target=process)
    t.daemon = True
    t.start()

    if (time.time() - start) != 0:
        fps = 1 / (time.time() - start)
    print("FPS: {}".format(fps))
#print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
