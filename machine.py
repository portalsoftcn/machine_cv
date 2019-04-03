import sys
import smbus
import time
bus = smbus.SMBus(1)
while True:
    cmd = input("enter a command:")
    print("command is %s"%cmd)
    cmdcode = int(cmd)
    if cmdcode == 0:
        time.sleep(2)
        exit()
    bus.write_byte(0x04,cmdcode)
