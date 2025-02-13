import os
import cantools
import can
import sys

#os.system("sudo ip link set can0 down")
#os.system("sudo ip link set can0 up type can bitrate 500000")
os.system("sudo ip link delete vcan0")
os.system("sudo modprobe vcan")
os.system("sudo ip link add dev vcan0 type vcan")
os.system("sudo ip link set up vcan0")


db = cantools.database.load_file('dbc/j1939.dbc')
can_bus = can.interface.Bus(channel='vcan0', interface='socketcan')

def isThrottleMessage(decodedMessage):
    if decodedMessage.get_message_name() == 'TSC1':
        print ("Action: Throttle")


while True:
    message = can_bus.recv()
    messageData = db.decode_message(message.arbitration_id, message.data)
    isThrottleMessage(messageData)

