import serial
import time
import struct

BAUD = 115200

arduino = serial.Serial('/dev/ttyACM0', BAUD, timeout=0.1)

time.sleep(1) #give the connection a sec to settle

val = float(5.5555)

ba = bytearray(struct.pack("f", val))
print([ "0x%02x" % b for b in ba])

arduino.write(ba)
arduino.flush()

#while True:
    #data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
    #data = arduino.readline()
    
    #if data:
    #    print data.rstrip('\n') #strip out the new lines for now
    #    #better to do .read() in the long run for this reason


