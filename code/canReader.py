import os
import cantools
import can
import sys
from canId import CanId

os.system("sudo ip link set can0 down")
os.system("sudo modprobe -r gs_usb")
os.system("sudo modprobe gs_usb")
os.system("sudo ip link set can0 up type can bitrate 125000")


"""os.system("sudo ip link delete vcan0")
os.system("sudo modprobe vcan")
os.system("sudo ip link add dev vcan0 type vcan")
os.system("sudo ip link set up vcan0")"""


db = cantools.database.load_file('dbc/j1939_1.dbc', strict=False)
can_bus = can.interface.Bus(channel='can0', interface='socketcan')
throttleMessage = db.get_message_by_name('TSC1')
gearboxMessage = db.get_message_by_name('MAN1')
eec1Message = db.get_message_by_name('EEC1')

def isThrottleMessage(decodedMessage):
    if "EngRqedTorque_TorqueLimit" in decodedMessage and "MessageCounter" in decodedMessage:
        print ("Action: Throttle")
        return

while True:
    message = can_bus.recv()
    try:
        print ("messageArbitrationID: ", message.arbitration_id)
        pgn = CanId.parse_int(message.arbitration_id).pgn
        if pgn == 0:
            messageData = db.decode_message(throttleMessage.frame_id, message.data)
            print ("throttleMessage: ", messageData)
            if message.arbitration_id not in {0x50d, 0x20d}:
                isThrottleMessage(messageData)
        elif message.arbitration_id == 0x18FF1C27:
            messageData = db.decode_message(gearboxMessage.frame_id, message.data)
            print ("gearboxMessage: ", messageData)
            print ()
        elif message.arbitration_id == eec1Message.frame_id:
            messageData = db.decode_message(eec1Message.frame_id, message.data)
            print ("eec1Message: ", messageData)
    except Exception as e:
        print(f"Error decoding message: {e}")
        continue
    print ("message: ", message)

