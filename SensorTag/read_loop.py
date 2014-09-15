import serial

BUF_SIZE = 1024
ser = serial.Serial('/dev/tty.usbserial-A900abe4', 115200, timeout=0)
while True:
  ba = bytearray(ser.read(size=BUF_SIZE))
  if len(ba) > 0:
    print ba, ['%02X' % b for b in ba], len(ba)
