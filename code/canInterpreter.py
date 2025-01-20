import os
import cantools
import can
from time import sleep

import cantools.database

throttleL = 0
throttleR = 0
rudderAngle = 0
backwardsL = False
backwardsR = False
key = ""
value = 0

import sys

os.system("sudo ip link set can0 down")
os.system("sudo ip link set can0 up type can bitrate 500000")

db = cantools.database.load_file('dbc/j1939.dbc')

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
            case "backwardsL":
                backwards = bool(value) 
            case "backwardsR":
                backwards = bool(value)
            case _:
                print(f"Unknown key: {key}")
                continue
    except ValueError as e:
        print(f"Error processing line: {line} ({e})")
        continue

    # Print the received data
    #print(f"throttleL: {throttleL},\nthrottleR: {throttleR},\nrudderAngle: {rudderAngle},\nbackwards: {backwards}")
    
    # Convert the values to a fixed-width 2-character hexadecimal string
    #throttleL_hex = f"{int(throttleL*100):02X}"
    #throttleR_hex = f"{int(throttleR*100):02X}"
    #rudderAngle_hex = f"{int((rudderAngle+1)*100):02X}"
    #backwards_hex = "01" if backwards else "00"


    # Send the data to the CAN bus
    #if line:
    #    os.system(f"sudo cansend can0 001#{throttleL_hex}{throttleR_hex}{rudderAngle_hex}{backwards_hex}")
    can_bus = can.interface.Bus(channel='can0', bustype='socketcan')
    throttleLInput = example_message.encode({'EngRequestedTorque_TorqueLimit': throttleL, 'EngOverrideCtrlMode': '01b'})
    leftMessage = can.Message(arbitration_id=example_message.frame_id, data=throttleLInput)

