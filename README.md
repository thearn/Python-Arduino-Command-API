# Python Arduino Command API

> &copy; 2012-2013 Tristan A. Hearn <tristanhearn@gmail.com>
> under the MIT License

Based on the Python Arduino Prototyping API by Akash Manohar (https://github.com/HashNuke/Python-Arduino-Prototyping-API/).

The Python Arduino Command API is a light-weight Python package for communicating with Arduino microcontroller boards. It is written
using a custom protocol, similar to Firmata (http://firmata.org/wiki/Main_Page). This allows a user to quickly protoype programs
for Arduino or to simply read and control harware connected to an Arduino from a host computer, without having to reload sketches onto an Arduino board.

Method names within the Python Arduino Command API are designed to be as close as possible to their Arduino programming language counterparts.

## Usage example
```python
#!/usr/bin/env python
"""
 Blinks an LED on digital pin 13
 in 1 second intervals
"""

from arduino import Arduino
import time

board = Arduino('9600')

while True:
    board.digitalWrite(13, "LOW")
    time.sleep(1)
    board.digitalWrite(13, "HIGH")
    time.sleep(1)
```
Python-Arduino-Command-API
For more examples, see arduino/examples.py. This file contains methods which replicate
the functionality of many Arduino demo sketches. 

#### Requirements:
* Python 2.3 or higher (Python 3.x not yet tested)
* PySerial
* Arduino compatible microcontroller with at least 14KB of memory 

#### Setup:

1. Load the sketch prototype.ino onto your Arduino board.
2. Import the arduino library into your python script.

## Methods

*Arduino(baud)* - Set up communication with currently connected and powered Arduino. 

The device name / COM port will be auto-detected. If there are more than one Arduino boards connected,
the desired COM port can be also be passed:
*Arduino(baud, port = "COM3")* 
A time-out for reading from the Arduino can also be specified:
*Arduino(baud, timeout = 2)* 

**Digital I/O**

* *Arduino.digitalWrite(pin_number, state)* - turn digital pin on/off
* *Arduino.digitalRead(pin_number)* - read state of a digital pin
* *Arduino.pinMode(pin_number, io_mode)* - set pin I/O mode
* *Arduino.pulseIn(pin_number, state)* - measures a pulse  
* *Arduino.pulseIn_set(pin_number, state)* - measures a pulse, with preconditioning

**Analog I/O**

* *Arduino.analogRead(pin_number)* - returns the analog value
* *Arduino.analogWrite(pin_number, value)* - sets the analog value

**Software Serial Functionality**

* *Arduino.SoftwareSerial.begin(ss_rxPin,ss_txPin,ss_device_baud)* - initialize software serial device on 
specified pins. 
Only one sofware serial device can be used at a time. Existing software serial instance will 
be be overwritten by calling this method, both in Python and on the arduino board.
* *Arduino.SoftwareSerial.write(data)* - send data using the arduino 'write' function to the existing software serial connection.
* *Arduino.SoftwareSerial.read()* - returns one byte from the existing software serial connection

**Misc**

* *Arduino.close()* - closes serial connection to the Arduino.

## To-do list:
* Add simple reset functionality that zeros out all pin values
* Add I2C / TWI function support (Arduino Wire.h commands)
* Add Servo support (Arduino Servo.h commands)
* Add tone() / noTone() squarewave generator support for piezo type speakers
* Make a program which generates 'prototype.ino' with selected Arduino function support, to help reduce memory requirements.
* Multi-serial support for Arduino mega (Serial1.read(), etc)