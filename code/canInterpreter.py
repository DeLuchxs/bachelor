import os
from time import sleep

throttleL = 0
throttleR = 0
rudderAngle = 0
backwards = False

import sys

# Continuously read data from stdin
while True:
    line = sys.stdin.readline()  # Read a single line of input
    if not line:
        break  # Exit if input stream is closed
    key, value = line.split(": ")
    match key:
        case "throttleL":
            throttleL = int(value)
        case "throttleR":
            throttleR = int(value)
        case "rudderAngle":
            rudderAngle = int(value)
        case "backwards":
            backwards = value == "True"

    # Print the received data
    print(f"throttleL: {throttleL},\nthrottleR: {throttleR},\n rudderAngle: {rudderAngle},\n backwards: {backwards}")
    