#!/usr/bin/python

# Library for encoder monitoring. Works on a separate thread
# from m1 to m2: ml, grd, pin1, pin2, 3v3, mr

import RPi.GPIO as GPIO
import threading

positions = [[0, 3], [1, 2]]

# Read Encoder.position to find differential since initialization
# A high multistep_count may indicate possible miscalculation - this could
# be significantly addressed by adding more directionality knowledge.

class Encoder:
    # Specify pins according to gpio number
    def __init__(self, pin1, pin2):
        self.position = 0
        GPIO.setup(pin1, GPIO.IN)
        GPIO.setup(pin2, GPIO.IN)
        self.pin1 = pin1
        self.pin2 = pin2
        self.multistep_count = 0
        self.thread = threading.Thread(target = self.monitor)
        self.thread.start()
        self.dict = {}

    def monitor(self):
        p1 = GPIO.input(self.pin1)
        p2 = GPIO.input(self.pin2)
        pos = positions[p1][p2]
        count = 0
        while True:
            input1 = GPIO.input(self.pin1)
            input2 = GPIO.input(self.pin2)
            count += 1
            if (p1 != input1 or p2 != input2):
                this_count = self.dict.get(count, 0)
                self.dict[count] = this_count + 1
                p1 = input1
                p2 = input2
                newpos = positions[p1][p2]
                change = (newpos + 4 - pos) % 4
                if change <= 2:
                    self.position += change
                else:
                    change = (pos + 4 - newpos) % 4
                    self.position -= change
                if change > 1:
                    self.multistep_count += 1
                pos = newpos
                count = 0
        
# Example usage

from adafruit_motorkit import MotorKit
kit = MotorKit()

import time

def main():
    print("Default test")
    try:
        e1 = Encoder(4, 17)
        print("Moving Forward ")
        kit.motor1.throttle = -1.0
        print("position: " + str(e1.position) + " multistep: " + str(e1.multistep_count))
        time.sleep(1)
        print("position: " + str(e1.position) + " multistep: " + str(e1.multistep_count))
        print(str(e1.dict))
        kit.motor1.throttle = 0

    except KeyboardInterrupt:
        kit.motor1.throttle = 0
        GPIO.cleanup()

if __name__ == "__main__":
    main()
