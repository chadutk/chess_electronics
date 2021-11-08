from adafruit_motorkit import MotorKit
kit = MotorKit()

import time
from Encoder import Encoder

try:
    print("Testing")
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

