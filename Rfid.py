#!/usr/bin/env python

# When wiring, use this to map from the reader to board.
# Pins are numbered with their GPIO number.
# (SDA ... 5v) -> (p8, p11, p10, p9, -, gnd, p25, 3.3, -)

import RPi.GPIO as GPIO
from SimpleMFRC522 import SimpleMFRC522

reader = SimpleMFRC522()
try:
  print("Waiting for rfid/nfc")
  id, text = reader.read()
  print(id)
  print(text)
finally:
  GPIO.cleanup()
