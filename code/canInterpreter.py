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
canLeftFrameID = 0x50d # CAN3 (0x5b3)
canRightFrameID = 0x20d # CAN4


import sys

"""os.system("sudo ip link set can0 down")
os.system("sudo modprobe -r gs_usb")
os.system("sudo modprobe gs_usb")
os.system("sudo ip link set can0 up type can bitrate 500000") """


os.system("sudo ip link delete vcan0")
os.system("sudo modprobe vcan")
os.system("sudo ip link add dev vcan0 type vcan")
os.system("sudo ip link set up vcan0")

db = cantools.database.load_file('dbc/j1939_1.dbc', strict=False)
db.messages
gasLeverMessage = db.get_message_by_name('TSC1')
gearboxMessage = db.get_message_by_name('MAN1')
can_bus = can.interface.Bus(channel='vcan0', interface='socketcan')

# Functions
def encodeThrottleMessage(speed, throttle, canFrameID):
    torqueHiRes = throttle * 0.125
    if torqueHiRes > 0.875:
        torqueHiRes = 0.875
    throttle = (throttle * 250) - 125
    try:
        throttleInput = gasLeverMessage.encode({ 
            'EngOverrideCtrlMode': 3, #3: Speed / Torque Limit Control Mode
            'EngRequestedSpeedCtrlConditions': 0, # 0: Transient Optimized for driveline disengaged and non-lockup conditions
            'OverrideCtrlModePriority': 0, # 0: Highest Priority
            'EngRequestedSpeed_SpeedLimit': speed,
            'EngRequestedTorque_TorqueLimit': throttle,
            'TSC1TransRate': 4, # Transmission Rate of 100ms
            'TSC1CtrlPurpose': 31, # Temporary PowerTrain Control
            'EngRequestedTorqueHighResolution': torqueHiRes,
            'MessageCounter': messageCounter,
            'MessageChecksum': 0
        })
    except Exception as e:
        print(f"Error encoding message: {e}")
        return None
    #calculate the checksum        
    if messageCounter != 4 and messageCounter != 15: 
        print ("EngRqedTorque_TorqueLimit: ", throttle)
        return can.Message(arbitration_id=canFrameID, data=throttleInput, is_extended_id=False)
    elif messageCounter == 4:
        currentChecksum = 3
    else:
        currentChecksum = 15
    
    # encode the message with checksum
    try:
        throttleInput = gasLeverMessage.encode({ 
            'EngOverrideCtrlMode': 3, #3: Speed / Torque Limit Control Mode
            'EngRequestedSpeedCtrlConditions': 0, # 0: Transient Optimized for driveline disengaged and non-lockup conditions
            'OverrideCtrlModePriority': 0, # 0: Highest Priority
            'EngRequestedSpeed_SpeedLimit': speed,
            'EngRequestedTorque_TorqueLimit': throttle,
            'TSC1TransRate': 4, # Transmission Rate of 100ms
            'TSC1CtrlPurpose': 31, # Temporary PowerTrain Control
            'EngRequestedTorqueHighResolution': torqueHiRes,
            'MessageCounter': messageCounter,
            'MessageChecksum': currentChecksum
        })
    except Exception as e:
        print(f"Error encoding message: {e}")
        return None
    print ("EngRqedTorque_TorqueLimit: ", throttle)
    return can.Message(arbitration_id=canFrameID, data=throttleInput, is_extended_id=False)

def encodeGearboxMessage(throttle, backwards):
    throttle = (throttle * 250) - 125
    gearboxForward = False
    gearboxReverse = False
    gearboxNeutral = True
    if backwards:
        gearboxReverse = True
        gearboxForward = False
        gearboxNeutral = False
    else:
        gearboxForward = True
        gearboxReverse = False
        gearboxNeutral = False
    try: 
        gearboxInput = gearboxMessage.encode({
            'StatusGearboxNeutral' : gearboxNeutral,
            'StatusGearboxForward' : gearboxForward,
            'StatusGearboxReverse' : gearboxReverse,
            'EngStartReq' : 0x01,
            'EngStopReq' : 0x00,
            'CurrentMaxPermissibleLoad' : throttle,
            'ExhaustBackPressure' : 0,
            'SCRSystem1CatalystTemperature' : 0,
            'SCRSystem2CatalystTemperature' : 0
        })
    except Exception as e:
        print(f"Error encoding message: {e}")
        return None
    return can.Message(arbitration_id=gearboxMessage.frame_id, data=gearboxInput, is_extended_id=True)


def calculateChecksum(dataInput, canFrameID):
    checksum = 0x00
    data_bytes = dataInput[:7]
    checksum = sum(data_bytes)
    checksum += (messageCounter & 0x0F)
                 
    idLowByte = canFrameID & 0xFF
    idMidLowByte = (canFrameID >> 8) & 0xFF
    idMidHighByte = (canFrameID >> 16) & 0xFF
    idHighByte = (canFrameID >> 24) & 0xFF

    checksum += idLowByte + idMidLowByte + idMidHighByte + idHighByte
    checksum = (((checksum >> 4) + checksum) & 0x0F)
    return checksum


throttleLMessage = ""
throttleRMessage = ""
previousThrottleL = ""
previousThrottleR = ""
gearboxL = ""
gearboxR = ""

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
        
        messageCounter = (messageCounter + 1) % 8

        try:
            key, value = line.split(": ", 1)  # Split into key and value, allow extra colons in value
            match key:
                case "Action":
                    if value == "Throttle":
                        throttleLMessage = encodeThrottleMessage(speedL, throttleL, canLeftFrameID)
                        throttleRMessage = encodeThrottleMessage(speedR, throttleR, canRightFrameID)
                case "throttleL":
                    throttleL = float(value)
                    speedL = float(value) * 8031.75 # 8031.75 maximum value for rpm speed in DBC (scale 0.125)
                    throttleLMessage = encodeThrottleMessage(speedL, throttleL, canLeftFrameID)
                case "throttleR":
                    throttleR = float(value)
                    speedR = float(value) * 8031.75
                    throttleRMessage = encodeThrottleMessage(speedR, throttleR, canRightFrameID)
                case "rudderAngle":
                    rudderAngle = float(value)
                case "backwardsL":
                    backwards = bool(value) 
                    gearboxL = encodeGearboxMessage(throttleL, backwards)
                    can_bus.send(gearboxL)
                case "backwardsR":
                    backwards = bool(value)
                    gearboxR = encodeGearboxMessage(throttleR, backwards)
                    #can_bus.send(gearboxR) # can bus unterscheidung muss noch vorgenommen werden
                case _:
                    print(f"Unknown key: {key}")
                    continue
        except ValueError as e:
            print(f"Error processing line: {line} ({e})")
            continue


        '''if throttleLMessage != "" or previousThrottleL != throttleLMessage:
            can_bus.send(throttleLMessage)
            previousThrottleL = throttleLMessage
            print(f"Sent message: {throttleLMessage}")'''

except KeyboardInterrupt:
    print("Exiting")

finally:
    can_bus.shutdown()

