import RPi.GPIO as GPIO
import sys
import json
import time
from threading import Thread
import requests

CLIENT_IP = sys.argv[1]

PIN_FORWARD = 37
PIN_BACKWARD = 35
PIN_LEFT = 33
PIN_RIGHT = 31

currentTime = time.time()
previousTime = time.time()
startTime = time.time()

def main():

    #setup gpio
    try:
        #GPIO.cleanup()
        setupGPIO()
    except Exception as e:
        print(e)

    while 1:
        try:
            user_input = get_input()
            update_motor_controller(user_input)
        except KeyboardInterrupt():

            print("Keyboard interrupt detected: resetting GPIO and exiting...")
            resetGPIOPins([PIN_LEFT, PIN_RIGHT, PIN_FORWARD, PIN_BACKWARD])
            GPIO.cleanup()
            # exit()
        

def update_motor_controller(json_data):

    try:
        print(json_data)
        if json_data["W"]:
            driveForward()
        else:
            resetGPIOPins([PIN_FORWARD])

        if json_data["A"]:
            turnLeft()
        else:
            resetGPIOPins([PIN_LEFT])

        if json_data["S"]:
            driveBackward()
        else:
            resetGPIOPins([PIN_BACKWARD])

        if json_data["D"]:
            turnRight()
        else:
            resetGPIOPins([PIN_RIGHT])
    except Exception as e:
        print("server offline?")
        print(e)

def get_input():
    try:
        r = requests.get('http://192.168.1.11:5000/get_input')
        return r.json()
    except Exception as e:
        print(e)
        GPIO.cleanup()

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