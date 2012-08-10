#!/usr/bin/env python
from serial.tools import list_ports
import serial, time

class SoftwareSerial(object):
    """
    Class for Arduino software serial functionality
    """
    def __init__(self,board):
        self.board=board
        self.connected = False

    def begin(self,p1,p2,baud):
        """
        Create software serial instance on 
        specified tx,rx pins, at specified baud
        """
        cmd_str=''.join(["@ss%",str(p1),"%",str(p2),"%",str(baud),"$!"])
        self.board.sr.write(cmd_str)
        self.board.sr.flush()
        response= self.board.sr.readline().replace("\r\n","")
        if response == "ss OK":
            self.connected = True
            return True
        else:
            self.connected = False
            return False
        
    def write(self,data):
        """
        sends data to existing software serial instance 
        using Arduino's 'write' function
        """
        if self.connected:
            cmd_str=''.join(["@sw%",str(data),"$!"])
            self.board.sr.write(cmd_str)
            self.board.sr.flush()
            response= self.board.sr.readline().replace("\r\n","")
            if response == "ss OK":
                return True
        else:
            return False

    def read(self):
        """
        returns first bit read from
        existing software serial instance
        """
        if self.connected:
            cmd_str=''.join(["@sr%$!"])
            self.board.sr.write(cmd_str)
            self.board.sr.flush()
            response= self.board.sr.readline().replace("\r\n","")
            if response:
                return response
        else:
            return False

class Arduino(object):
    def __init__(self,baud,port="",timeout=2):
        """
        Initializes serial communication with Arduino.
        Attempts to self-select COM port, if not specified.
        """
        self.baud = baud
        self.timeout = timeout
        self.ss_connected=False
        self.SoftwareSerial = SoftwareSerial(self)
        if port == "":
            self.findPort()
        self.sr = serial.Serial(self.port, self.baud,timeout =self.timeout)
        time.sleep(2)
        
    def findPort(self):
        """
        Returns first Arduino found
        in system's device list
        """
        for pt in list_ports.comports():
            if ("FTDIBUS" in pt[-1]) or ("usbserial" in pt[-1]):
                self.port = pt[0]
                return
       
    def digitalWrite(self,pin,val):
        """
        Sends digitalWrite command
        to digital pin on Arduino
        -------------
        inputs:
           pin : digital pin number
           val : either "HIGH" or "LOW"
        """
        if val=="LOW":
            pin_ = -pin
        else:
            pin_ = pin
        cmd_str=''.join(["@dw%",str(pin_),"$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()    
        except:
            pass

    def analogWrite(self,pin,val):
        """
        Sends analogWrite pwm command
        to pin on Arduino
        -------------
        inputs:
           pin : pin number
           val : integer 0 (off) to 255 (always on)
        """
        if val>255:
            val=255
        elif val<0:
            val=0
        cmd_str=''.join(["@aw%",str(pin),"%",str(val),"$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass

    def analogRead(self,pin):
        """
        Returns the value of a specified
        analog pin.
        inputs:
           pin : analog pin number for measurement
        returns:
           value: integer from 1 to 1023
        """
        cmd_str=''.join(["@ar%",str(pin),"$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass
        rd = self.sr.readline().replace("\r\n","")
        try:
            return int(rd)
        except:
            return 0

      
    def pinMode(self,pin,val):
        """
        Sets I/O mode of pin
        inputs:
           pin: pin number to toggle
           val: "INPUT" or "OUTPUT"
        """
        if val=="INPUT":
            pin_ = -pin
        else:
            pin_ = pin
        cmd_str=''.join(["@pm%",str(pin_),"$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()    
        except:
            pass
    
    def pulseIn(self,pin,val):
        """
        Reads a pulse from a pin
        
        inputs:
           pin: pin number for pulse measurement
        returns:
           duration : pulse length measurement
           
        """
        if val=="LOW":
            pin_ = -pin
        else:
            pin_ = pin
        cmd_str=''.join(["@pi%",str(pin_),"$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()   
        except:
            pass
        rd = self.sr.readline().replace("\r\n","")
        try:
            return float(rd)
        except:
            return -1    
    
    def pulseIn_set(self,pin,val):
        """
        Sets a digital pin value, then reads the response
        as a pulse width.
        Useful for some ultrasonic rangefinders, etc.
        
        inputs:
           pin: pin number for pulse measurement
           val: "HIGH" or "LOW". Pulse is measured
                when this state is detected
        returns:
           duration : pulse length measurement
           
        This method will automatically toggle
        I/O modes on the pin and precondition the 
        measurment with a clean LOW/HIGH pulse.
        Arduino.pulseIn_set(pin,"HIGH") is 
        equivalent to the Arduino sketch code:
        
        pinMode(pin, OUTPUT);
        digitalWrite(pin, LOW);
        delayMicroseconds(2);
        digitalWrite(pin, HIGH);
        delayMicroseconds(5);
        digitalWrite(pin, LOW);
        pinMode(pin, INPUT);
        long duration = pulseIn(pin, HIGH); 
        """
        if val=="LOW":
            pin_ = -pin
        else:
            pin_ = pin
        cmd_str=''.join(["@ps%",str(pin_),"$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()   
        except:
            pass
        rd = self.sr.readline().replace("\r\n","")
        try:
            return float(rd)
        except:
            return -1
        
    def close(self):
        self.sr.close() 
    
    def digitalRead(self,pin):
        """
        Returns the value of a specified
        digital pin.
        inputs:
           pin : digital pin number for measurement
        returns:
           value: 0 for "LOW", 1 for "HIGH"
        """
        cmd_str=''.join(["@dr%",str(pin),"$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass
        rd = self.sr.readline().replace("\r\n","")
        try:
            return 1 - int(rd)
        except:
            return 0
          

if __name__=="__main__":
    board=Arduino(9600)
    while True:
        time.sleep(0.01)
        val=board.analogRead(5)/4
        board.analogWrite(11,val)
    