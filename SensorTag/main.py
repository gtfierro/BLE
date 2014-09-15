import serial
import time
from irtemp import process_temp
from humidity import process_hum
from ble import process_ble

FRAME_START_MAGIC = bytearray([0xBE, 0xEF])
FRAME_MAX_LEN = 128

class FrameType:
  TEMP = 0x01
  HUM = 0x02
  BAR = 0x03
  MAG = 0x04
  ACC = 0x05
  GYRO = 0x06
  BLE_AD = 0x10
  
def read_loop(tty, process_frame, baud = 115200):
  # Non-blocking mode
  ser = serial.Serial(tty, baud, timeout=0)

  buf = bytearray()
  # Does a new frame begin at buf[0]
  frame_start = False

  while True:
    buf += bytearray(ser.read(size=FRAME_MAX_LEN))
    # Truncate buffer from the left to 2 * max frame size
    if len(buf) > 2 * FRAME_MAX_LEN:
      buf = buf[-2 * FRAME_MAX_LEN:]
      found_frame = False
      print 'Warning: data dropped'

    # Search for frames
    idx = buf.find(FRAME_START_MAGIC)
    while idx != -1:
      if frame_start:
        process_frame(buf[:idx])

      buf = buf[idx+len(FRAME_START_MAGIC):]
      frame_start = True

      idx = buf.find(FRAME_START_MAGIC)

    time.sleep(0.05)

def process_frame(frame):
  if len(frame) < 2:
    return

  type = frame[0]
  data = frame[1:]
  if type == FrameType.TEMP:
    process_temp(data)
  elif type == FrameType.HUM:
    process_hum(data)
    pass
  elif type == FrameType.BLE_AD:
    process_ble(data)
    pass
  else:
    print "Error: unknown frame type: %d" % type

def main():
  read_loop('/dev/tty.usbserial-A900abe4', process_frame, baud = 115200)

if __name__ == '__main__':
  main()
