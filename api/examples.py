#!/usr/bin/env python
from arduino import Arduino
import time

def Blink(led_pin,baud):
    """
    Blinks an LED in 1 sec intervals
    """
    board = Arduino(baud)
    while True:
        board.digitalWrite(led_pin,"LOW")
        print board.digitalRead(led_pin) #confirm LOW (0)
        time.sleep(1)
        board.digitalWrite(led_pin,"HIGH")
        print board.digitalRead(led_pin) #confirm HIGH (1)
        time.sleep(1)

def softBlink(led_pin,baud):
    """
    Fades an LED off and on, using 
    Arduino's analogWrite (PWM) function
    """    
    board=Arduino(baud)
    i=0
    while True:
        i+=1
        k=i%510
        if k%5==0:
            if k>255:
                k=510-k
            board.analogWrite(led_pin,k)

def adjustBrightness(pot_pin,led_pin,baud):
    """
    Adjusts brightness of an LED using a
    potentiometer
    """    
    board=Arduino(baud)
    while True:
        time.sleep(0.01)
        val=board.analogRead(pot_pin)/4
        print val
        board.analogWrite(led_pin,val)


def PingSonar(pw_pin,baud):
    """
    Gets distance measurement from Ping))) 
    ultrasonic rangefinder connected to pw_pin
    """
    board = Arduino(baud)
    pingPin=pw_pin
    while True:
        duration = board.pulseIn(pingPin, "HIGH")
        inches = duration/72./2.
        cent = duration/29./2.
        print inches,"inches"
        time.sleep(0.1)
        
def LCD(tx,baud,ssbaud,message):
    """
    Prints to two-line LCD connected to 
    pin tx
    """
    board = Arduino(baud)
    board.SoftwareSerial.begin(0,tx,ssbaud)
    while True:
        board.SoftwareSerial.write(" test ") 




if __name__=="__main__":
    #LCD(5,9600,9600," test ")
    adjustBrightness(5,11,9600)
    #softBlink(11,9600)