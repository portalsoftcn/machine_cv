import sys
import smbus
import time
bus = smbus.SMBus(1)
while True:
    time.sleep(0.2)
    bus.write_byte(0x04,1)
