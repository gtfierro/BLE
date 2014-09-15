import struct

def to_hex(ba):
  return ":".join("%02X" % b for b in ba)

def process_ble(data):
  type = data[0:1]
  payload = data[1:]
  if type == 'S' and len(payload) == 0:
    # Start of a scan
    pass
  elif type == 'D' and len(payload) == 7:
    mac = payload[0:6]
    rssi = struct.unpack('b', payload[6:7])[0]

    print "BLE:\t Addr = %s, RSSI = %d" % (to_hex(mac), rssi)
  else:
    print "Unknown", to_hex(data)
