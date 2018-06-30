import socket
import RPi.GPIO as GPIO
import sys
import json
import time
from threading import Thread

CLIENT_IP = sys.argv[1]
TARGET_PORT = 6624 #FRC 6624 ftw
BUFFER_SIZE = 512

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
        sendIPPacket()
        listenForPackets()
    except KeyboardInterrupt():
        print "Keyboard interrupt detected: resetting GPIO and exiting..."
        resetGPIOPins([PIN_LEFT, PIN_RIGHT, PIN_FORWARD, PIN_BACKWARD])
        GPIO.cleanup()
        exit()
    except (socket.timeout, socket.error):
        #print "Socket timed out: resetting GPIO and exiting..."
        #resetGPIOPins([PIN_LEFT, PIN_RIGHT, PIN_FORWARD, PIN_BACKWARD])
        #GPIO.cleanup()
        #exit()
        print "Oh fuck we DC'd immma do something in 5 seconds"
        time.sleep(5)
        main()

# desync checking thread
class DesyncCheck(Thread):
    desync_timeout = 0.3
    active = True
    start_time = 0.0

    desync = False
    desync_time = 0.0

    def __init__(self):
        super(DesyncCheck, self).__init__()
        self.daemon = True

    def run(self):
        self.start_time = time.time()
        # keep updating while active
        while self.active:
            time.sleep(0.01)
            self.update()

    def stop(self):
        if self.desync:
            self.desync_time = time.time() - self.start_time - self.desync_timeout
        self.active = False

    def update(self):
        # do nothing if not active
        if not self.active:
            return
        # if timed out, then we desync'd
        if time.time() - self.start_time > self.desync_timeout:
            # stop the car
            resetGPIOPins([PIN_LEFT, PIN_RIGHT, PIN_FORWARD, PIN_BACKWARD])
            # we desync'd
            self.desync = True
            self.stop()

def sendIPPacket():
    ip = getIP()

    sock.connect((CLIENT_IP, TARGET_PORT))
    sock.send("CONNECT")


def listenForPackets():
    try:
        while True:

            desync_checker = DesyncCheck()
            desync_checker.start()
            data = sock.recv(1024)

            desync_checker.stop()
            if desync_checker.desync:
                print 'We desyncd for', desync_checker.desync_time, 'seconds.'
                sock.send(str(desync_checker.desync_time))
                continue

            dict = json.loads(data)

            if dict["W"]:
                driveForward()
            else:
                resetGPIOPins([PIN_FORWARD])

            if dict["A"]:
                turnLeft()
            else:
                resetGPIOPins([PIN_LEFT])


            if dict["S"]:
                driveBackward()
            else:
                resetGPIOPins([PIN_BACKWARD])


            if dict["D"]:
                turnRight()
            else:
                resetGPIOPins([PIN_RIGHT])

            sock.send('OK') #echo for confirmation
    except (socket.timeout, socket.error):
        main()

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



def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    s.connect(("8.8.8.8", 80));
    ip = (s.getsockname()[0]);
    s.close();

    return ip;

if __name__ == "__main__":
    main()