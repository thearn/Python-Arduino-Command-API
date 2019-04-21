
from arduino import Arduino

board = Arduino()

#from Arduino import Arduino
#import time
#
#PORT_NAME = '/dev/tty.usbserial-1410'              # MUST BE UPDATED TO USE THE CORRECT PORT
#PIN_SENSE = 12                  # pin where ultrasic sensor is connected
#
## connect to Arduino
#board = Arduino(port=PORT_NAME)
#print('Connected')
#
#try:
#    while True:
#        # make distance measurement
#        pulseTime = board.pulseIn_set(PIN_SENSE, 'HIGH')
#        print(pulseTime)
#
#        time.sleep(1) # delay to keep UART bus for getting overloaded
#
#except KeyboardInterrupt:
#    board.close() # close serial connection