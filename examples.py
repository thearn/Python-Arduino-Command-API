#!/usr/bin/env python
from Arduino import Arduino
import time

class ArduinoExample(object):
    
    def __init__(self, baud,port="",timeout=2):
        self.board = Arduino(baud = baud, port = port, timeout = timeout)
    
    def execute(self):
        pass

class Blink(ArduinoExample):
    """
    Blinks an LED off and on, using 
    Arduino's digitalWrite function
    """    
    def __init__(self, led_pin, baud,port="",timeout=2):
        super(Blink, self).__init__(baud, port = port, timeout = timeout)
        self.led_pin = led_pin
    
    def execute(self):
        self.board.digitalWrite(self.led_pin,"LOW")
        print self.board.digitalRead(self.led_pin) #confirm LOW (0)
        time.sleep(1)
        self.board.digitalWrite(self.led_pin,"HIGH")
        print self.board.digitalRead(self.led_pin) #confirm HIGH (1)
        time.sleep(1)

class SoftBlink(ArduinoExample):
    """
    Fades an LED off and on, using 
    Arduino's analogWrite (PWM) function
    """    
    def __init__(self, led_pin, baud,port="",timeout=2):
        super(SoftBlink, self).__init__(baud, port = port, timeout = timeout)
        self.led_pin = led_pin
        self.i = 0
        
    def execute(self):
        self.i+=1
        k=self.i%510
        if k%5==0:
            if k>255:
                k=510-k
            self.board.analogWrite(self.led_pin,k)

class AdjustBrightness(ArduinoExample):
    """
    Adjusts brightness of an LED using a
    potentiometer
    """    
    def __init__(self, led_pin, pot_pin,baud,port="",timeout=2):
        super(AdjustBrightness, self).__init__(baud, port = port, 
                                               timeout = timeout)
        self.led_pin = led_pin
        self.pot_pin = pot_pin
        
    def execute(self):
        time.sleep(0.01)
        val=self.board.analogRead(self.pot_pin)/4
        print val
        self.board.analogWrite(self.led_pin,self.val)

class PingSonar(ArduinoExample):
    """
    Gets distance measurement from Ping))) 
    ultrasonic rangefinder connected to pw_pin
    """  
    def __init__(self, pw_pin ,baud,port="",timeout=2):
        super(PingSonar, self).__init__(baud, port = port, timeout = timeout)
        self.pw_pin = pw_pin

    def execute(self):
        duration = self.board.pulseIn(self.pw_pin, "HIGH")
        inches = duration/72./2.
        cent = duration/29./2.
        print inches,"inches"
        time.sleep(0.1)
   
class LCD(ArduinoExample):
    """
    Prints to two-line LCD connected to 
    pin tx
    """
    def __init__(self, tx,ssbaud ,baud,port="",timeout=2):
        super(LCD, self).__init__(baud, port = port, timeout = timeout)
        self.tx = tx
        self.ssbaud = ssbaud

    def execute(self, message):
        self.board.SoftwareSerial.write(message) 


if __name__=="__main__":
    app = Blink(9600)
    while True:
        app.execute()