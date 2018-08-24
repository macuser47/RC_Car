import socket
import RPi.GPIO as GPIO
import sys
import json
import time
from threading import Thread
import request

CLIENT_IP = sys.argv[1]
TARGET_PORT = 6624 #FRC 6624 ftw
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PIN_FORWARD = 37
PIN_BACKWARD = 35
PIN_LEFT = 33
PIN_RIGHT = 31

currentTime = time.time()
previousTime = time.time()

startTime = time.time()

def main():
    try:
        setupGPIO()
        #sendIPPacket()
        #listenForPackets()
    except KeyboardInterrupt():
        print("Keyboard interrupt detected: resetting GPIO and exiting...")
        resetGPIOPins([PIN_LEFT, PIN_RIGHT, PIN_FORWARD, PIN_BACKWARD])
        GPIO.cleanup()
        exit()



def update_motor_controller():
    pass

def get_input():
    r = requests.get('192.168.1.11/get_input')
    print(r.json())


    # except (socket.timeout, socket.error):
    #     #print "Socket timed out: resetting GPIO and exiting..."
    #     #resetGPIOPins([PIN_LEFT, PIN_RIGHT, PIN_FORWARD, PIN_BACKWARD])
    #     #GPIO.cleanup()
    #     #exit()
    #     print("Disconect between client and server. Retrying in 5 seconds.")
    #     time.sleep(5)
    #     main()

# def sendIPPacket():

#     sock.connect((CLIENT_IP, TARGET_PORT))
#     sock.send("CONNECT")

# def listenForPackets():
#     try:
#         while True:
#             data = sock.recv(1024)

#             dict = json.loads(data)

#             if dict["W"]:
#                 driveForward()
#             else:
#                 resetGPIOPins([PIN_FORWARD])

#             if dict["A"]:
#                 turnLeft()
#             else:
#                 resetGPIOPins([PIN_LEFT])


#             if dict["S"]:
#                 driveBackward()
#             else:
#                 resetGPIOPins([PIN_BACKWARD])


#             if dict["D"]:
#                 turnRight()
#             else:
#                 resetGPIOPins([PIN_RIGHT])

#             sock.send('OK') #echo for confirmation
#     except (socket.timeout, socket.error):
#         main()

def turnLeft():
    resetGPIOPins([PIN_RIGHT])
    GPIO.output(PIN_LEFT, GPIO.HIGH)


def turnRight():
    resetGPIOPins([PIN_LEFT])
    GPIO.output(PIN_RIGHT, GPIO.HIGH)

def driveForward():
    resetGPIOPins([PIN_BACKWARD])
    GPIO.output(PIN_FORWARD, GPIO.HIGH)

def driveBackward():
    resetGPIOPins([PIN_FORWARD])
    GPIO.output(PIN_BACKWARD, GPIO.HIGH)

def setupGPIO():
    GPIO.setmode(GPIO.BOARD)
    for pin in [PIN_FORWARD, PIN_BACKWARD, PIN_RIGHT, PIN_LEFT]:
        GPIO.setup(pin, GPIO.OUT)

def resetGPIOPins(pins):
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)

if __name__ == "__main__":
    main()