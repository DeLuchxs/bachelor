import os
from time import sleep

throttleL = 0
throttleR = 0
rudderAngle = 0
backwards = False
key = ""
value = 0

import sys

# Continuously read data from stdin
while True:
    line = sys.stdin.readline()  # Read a single line of input
    if not line:
        break  # Exit if input stream is closed
    line = line.strip()  # Remove leading/trailing whitespace
    if not line:
        continue  # Skip empty lines
    if ":" not in line:
        continue
    try:
        key, value = line.split(": ", 1)  # Split into key and value, allow extra colons in value
        match key:
            case "throttleL":
                throttleL = float(value)
            case "throttleR":
                throttleR = float(value)
            case "rudderAngle":
                rudderAngle = float(value)
            case "backwards":
                backwards = bool(value) 
            case _:
                print(f"Unknown key: {key}")
                continue
    except ValueError as e:
        print(f"Error processing line: {line} ({e})")
        continue

    # Print the received data
    #print(f"throttleL: {throttleL},\nthrottleR: {throttleR},\nrudderAngle: {rudderAngle},\nbackwards: {backwards}")
    
    # Send the received data to the CAN-Bus
    