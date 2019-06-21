#!/usr/bin/env python
from Arduino import Arduino
import time


def Blink(led_pin, baud, port=""):
    """
    Blinks an LED in 1 sec intervals
    """
    board = Arduino(baud, port=port)
    board.pinMode(led_pin, "OUTPUT")
    while True:
        board.digitalWrite(led_pin, "LOW")
        print board.digitalRead(led_pin)  # confirm LOW (0)
        time.sleep(1)
        board.digitalWrite(led_pin, "HIGH")
        print board.digitalRead(led_pin)  # confirm HIGH (1)
        time.sleep(1)


def softBlink(led_pin, baud, port=""):
    """
    Fades an LED off and on, using
    Arduino's analogWrite (PWM) function
    """
    board = Arduino(baud, port=port)
    i = 0
    while True:
        i += 1
        k = i % 510
        if k % 5 == 0:
            if k > 255:
                k = 510 - k
            board.analogWrite(led_pin, k)


def adjustBrightness(pot_pin, led_pin, baud, port=""):
    """
    Adjusts brightness of an LED using a
    potentiometer.
    """
    board = Arduino(baud, port=port)
    while True:
        time.sleep(0.01)
        val = board.analogRead(pot_pin) / 4
        print val
        board.analogWrite(led_pin, val)


def PingSonar(pw_pin, baud, port=""):
    """
    Gets distance measurement from Ping)))
    ultrasonic rangefinder connected to pw_pin
    """
    board = Arduino(baud, port=port)
    pingPin = pw_pin
    while True:
        duration = board.pulseIn(pingPin, "HIGH")
        inches = duration / 72. / 2.
        # cent = duration / 29. / 2.
        print inches, "inches"
        time.sleep(0.1)


def LCD(tx, baud, ssbaud, message, port=""):
    """
    Prints to two-line LCD connected to
    pin tx
    """
    board = Arduino(baud, port=port)
    board.SoftwareSerial.begin(0, tx, ssbaud)
    while True:
        board.SoftwareSerial.write(" test ")

if __name__ == "__main__":
    Blink(13, '115200')
