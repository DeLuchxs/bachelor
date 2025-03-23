import cantools


canFrameID = 0x5b3
messageCounter = 0x00

db = cantools.database.load_file('dbc/j1939_1.dbc', strict=False)
gasLeverMessage = db.get_message_by_name('TSC1')

throttleRInput = gasLeverMessage.encode({ 
        'EngOverrideCtrlMode': 3, #3: Speed / Torque Limit Control Mode
        'EngRequestedSpeedCtrlConditions': 0, # 0: Transient Optimized for driveline disengaged and non-lockup conditions
        'OverrideCtrlModePriority': 0, # 0: Highest Priority
        'EngRequestedSpeed_SpeedLimit': 1027.25,
        'EngRequestedTorque_TorqueLimit': -123,
        'TSC1TransRate': 7, # Transmission Rate of 100ms
        'TSC1CtrlPurpose': 31, # Temporary PowerTrain Control
        'EngRequestedTorqueHighResolution': 1.875,
        'MessageCounter': 15,
        'MessageChecksum': 0
    })


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

print(checksum)