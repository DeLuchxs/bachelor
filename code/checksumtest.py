canFrameID = 0x5b3
throttleRInput = 0xDEADBEEF
messageCounter = 0x00

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