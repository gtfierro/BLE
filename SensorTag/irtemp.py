import struct

def unpack(b, signed = False):
  (lo, hi) = struct.unpack('Bb' if signed else 'BB', b)
  return (hi << 8) + lo

def celsiusToF(t):
  return t * 9.0/5.0 + 32

def getAmbientTemp(t):
  return t / 128.0

def getTragetTemp(v, ambientT):
  Vobj2 = v * 0.00000015625
  Tdie = ambientT + 273.15

  S0 = 5.593E-14  # Calibration factor
  a1 = 1.75E-3
  a2 = -1.678E-5
  b0 = -2.94E-5
  b1 = -5.7E-7
  b2 = 4.63E-9
  c2 = 13.4
  Tref = 298.15
  S = S0*(1+a1*(Tdie - Tref)+a2*pow((Tdie - Tref),2))
  Vos = b0 + b1*(Tdie - Tref) + b2*pow((Tdie - Tref),2)
  fObj = (Vobj2 - Vos) + c2*pow((Vobj2 - Vos),2)
  tObj = pow(pow(Tdie,4) + (fObj/S),.25)

  return tObj - 273.15;

def process_temp(data):
  if len(data) != 4:
    print "Error: Temp unexpected frame length:", len(data)
    return
  
  v = unpack(data[0:2], signed=True)
  t = unpack(data[2:4])
  ambiantT = getAmbientTemp(t)
  targetT = getTragetTemp(v, ambiantT)
  print "Temp:\t Ambiant Temp = %.2f, Target Temp = %.2f" % \
      (celsiusToF(ambiantT), celsiusToF(targetT))
