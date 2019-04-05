import sys
import smbus
import time

class Arduino:

    def __init__(self):

    def sendCmd(self,cmd):
        bus = smbus.SMBus(1)
        cmdcode = int(cmd)
        bus.write_byte(0x04,cmdcode)
