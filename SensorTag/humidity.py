import struct

def unpack(b, signed = False):
  (lo, hi) = struct.unpack('Bb' if signed else 'BB', b)
  return (hi << 8) + lo

def celsiusToF(t):
  return t * 9.0/5.0 + 32

def getHumTemp(rawT):
  return -46.85 + 175.72 / 65536 * rawT

def getHum(rawH):
  rawH &= ~0x0003;  #clear bits [1..0]
  return -6.0 + 125.0/65536 * rawH;

def process_hum(data):
  if len(data) != 4:
    print "Error: Hum unexpected frame length:", len(data)
    return

  rawT = unpack(data[0:2])
  rawH = unpack(data[2:4])

  temp = getHumTemp(rawT)
  hum = getHum(rawH)
  print "Hum:\t Temp = %.2f, Relative Humidty = %.2f%%" % (celsiusToF(temp), hum) 
