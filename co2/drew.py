import serial
import time

ser = serial.Serial("/dev/ttyS0",baudrate=9600,timeout=.5)
ser.flushInput()
time.sleep(1)

while True:
    ser.flushInput()
    ser.write("\xFE\x44\x00\x08\x02\x9F\x25")
    time.sleep(1)

    resp = ser.read(7)
    high = ord(resp[3])
    low = ord(resp[4])
    C = (high*256) + low

    print(C)
    time.sleep(.1)
#    print(resp[0])

