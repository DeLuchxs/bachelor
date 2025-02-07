import os
import cantools
import can
from time import sleep

import cantools.database

throttleL = 0
speedL = 0
throttleR = 0
speedR = 0 
rudderAngle = 0
backwardsL = False
backwardsR = False
key = ""
value = 0
messageCounter = -1
canFrameID = 0x2348875518

import sys

#os.system("sudo ip link set can0 down")
#os.system("sudo ip link set can0 up type can bitrate 500000")
os.system("sudo ip link delete vcan0")
os.system("sudo modprobe vcan")
os.system("sudo ip link add dev vcan0 type vcan")
os.system("sudo ip link set up vcan0")

db = cantools.database.load_file('dbc/j1939.dbc')
db.messages
example_message = db.get_message_by_name('TSC1')
can_bus = can.interface.Bus(channel='vcan0', interface='socketcan')


# Continuously read data from stdin
try:
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
                    speedL = float(value) * 8031.75 # 8031.75 maximum value for rpm speed in DBC (scale 0.125)
                case "throttleR":
                    throttleR = float(value)
                    speedR = float(value) * 8031.75
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

        if messageCounter < 15:
            messageCounter += 1
        else:
            messageCounter = 0

    # encode the message for the CAN bus
        try:
            throttleRInput = example_message.encode({ 
                'EngOverrideCtrlMode': 3, #3: Torque Control Mode
                'EngRqedSpeedCtrlConditions': 3, # 3: Transient Optimized for driveline disengaged and non-lockup conditions
                'OverrideCtrlModePriority': 0, # 0: Highest Priority
                'EngRqedSpeed_SpeedLimit': speedR,
                'EngRqedTorque_TorqueLimit': throttleR,
                'TransmissionRate': 2, # Transmission Rate of 100ms
                'ControlPurpose': 5, # Transient Optimized Torque Limit
                'EngineRequestedTorqueHiRes': throttleR,
                'MessageCounter': messageCounter,
                'MessageChecksum': 0
            })
        except Exception as e:
            print(f"Error encoding message: {e}")
            continue
        #calculate the checksum
        checksum = 0x00
        data_bytes = throttleRInput[:7]
        checksum = sum(data_bytes)
        checksum += (messageCounter & 0x0F)
                 
        idLowByte = canFrameID & 0xFF
        idMidLowByte = (canFrameID >> 8) & 0xFF
        idMidHighByte = (canFrameID >> 16) & 0xFF
        idHighByte = (canFrameID >> 24) & 0xFF

        checksum += idLowByte + idMidLowByte + idMidHighByte + idHighByte
        checksum = (((checksum >> 4) + checksum) & 0x0F)

    # encode the message with checksum
        try:
            throttleRChecksum = example_message.encode({ 
                'EngOverrideCtrlMode': 3, #3: Torque Control Mode
                'EngRqedSpeedCtrlConditions': 3, # 3: Transient Optimized for driveline disengaged and non-lockup conditions
                'OverrideCtrlModePriority': 0, # 0: Highest Priority
                'EngRqedSpeed_SpeedLimit': speedR,
                'EngRqedTorque_TorqueLimit': throttleR,
                'TransmissionRate': 2, # Transmission Rate of 100ms
                'ControlPurpose': 5, # Transient Optimized Torque Limit
                'EngineRequestedTorqueHiRes': throttleR,
                'MessageCounter': messageCounter,
                'MessageChecksum': checksum
            })
        except Exception as e:
            print(f"Error encoding message: {e}")
            continue
        rightMessage = can.Message(arbitration_id=example_message.frame_id, data=throttleRChecksum, is_extended_id=True)
        print(rightMessage)

except KeyboardInterrupt:
    print("Exiting")

finally:
    can_bus.shutdown()