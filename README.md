# Python Arduino Command API

> &copy; 2012-2013 Tristan A. Hearn <tristanhearn@gmail.com>
> under the MIT License

Based in part on the Python Arduino Prototyping API by Akash Manohar 
(https://github.com/HashNuke/Python-Arduino-Prototyping-API/).

The Python Arduino Command API is a light-weight Python package for 
communicating with Arduino microcontroller boards. It is written
using a custom protocol, similar to Firmata (http://firmata.org/wiki/Main_Page). 
This allows a user to quickly protoype programs
for Arduino or to simply read and control harware connected to an Arduino from 
a host computer, without having to reload sketches onto an Arduino board.

Method names within the Python Arduino Command API are designed to be as close 
as possible to their Arduino programming language counterparts.

## Simple usage example (LED blink)
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

## Requirements:
* Python 2.3 or higher (Python 3.x not yet tested)
* PySerial
* Arduino compatible microcontroller with at least 14KB of memory 

## Setup:
1. Verify that your Arduino board communicates at the baud rate specified in the 
`setup()` function in `prototype.ino`. Change it there if necessary.
1. Load the sketch `sketches\prototype\prototype.ino` onto your Arduino board, using the Arduino IDE.
2. Import the included arduino library `Arduino.py` into your python script.

For a collection of examples, see `arduino/examples.py`. This file contains methods which replicate
the functionality of many Arduino demo sketches. 

## Classes
*Arduino(baud)* - Set up communication with currently connected and powered 
Arduino. 
```python
board = Arduino("9600") #Example
```
The device name / COM port of the connected Arduino will be auto-detected. 
If there are more than one Arduino boards connected,
the desired COM port can be also be passed as an optional argument:
```python
board = Arduino("9600", port = "COM3") #Windows example
```
```python
board = Arduino("9600", port = "/dev/tty.usbmodemfa141") #OSX example
```
A time-out for reading from the Arduino can also be specified as an optional 
argument:
```python
board = Arduino("9600", timeout = 2) #Serial reading functions will 
#wait for no more than 2 seconds
```

- `SoftwareSerial()` A class for handling software serial functionality. 
Is used internally by the Arduino class, and should not be called directly.

## Methods

**Digital I/O**

- `Arduino.digitalWrite(pin_number, state)` turn digital pin on/off
- `Arduino.digitalRead(pin_number)` read state of a digital pin

```python
#Digital read / write example
board.digitalWrite(13, "HIGH") #Set digital pin 13 voltage
state_1 = board.digitalRead(13) #Will return integer 1
board.digitalWrite(13, "LOW") #Set digital pin 13 voltage
state_2 = board.digitalRead(13) #Will return integer 0
```

- `Arduino.pinMode(pin_number, io_mode)` set pin I/O mode
- `Arduino.pulseIn(pin_number, state)` measures a pulse  
- `Arduino.pulseIn_set(pin_number, state)` measures a pulse, with preconditioning

```python
#Digital mode / pulse example
board.pinMode(7, "INPUT") #Set digital pin 7 mode to INPUT
duration = board.pulseIn(7, "HIGH") #Return pulse width measurement on pin 7
```

**Analog I/O**

- `Arduino.analogRead(pin_number)` returns the analog value
- `Arduino.analogWrite(pin_number, value)` sets the analog value

```python
#Analog I/O examples
val=board.analogRead(5) #Read value on analog pin 5 (integer 0 to 1023)
val = val / 4 # scale to 0 - 255
board.analogWrite(11) #Set analog value (PWM) based on analog measurement
```

**Servo Library Functionality**
Support is included for up to 8 servos. 

- `Arduino.Servo.attach(pin, min = 544, max = 2400)` Create servo instance. Only 8 servos can be used at one time. 
- `Arduino.Servo.read(pin)` Returns the angle of the servo attached to the specified pin
- `Arduino.Servo.write(pin, angle)` Move an attached servo on a pin to a specified angle
- `Arduino.Servo.writeMicroseconds(pin, uS)` Write a value in microseconds to the servo on a specified pin
- `Arduino.Servo.detach(pin)` Detaches the servo on the specified pin

```python
#Servo example
board.Servo.attach(9) #declare servo on pin 9
board.Servo.attach(10) #declare servo on pin 10
board.Servo.write(9, 0) #move servo on pin 9 to 0 degrees
board.Servo.write(10, 180) #move servo on pin 10 to 180 degrees
angle_1 = board.Servo.read(9) # should be 0
angle_2 = board.Servo.read(10) # should be 180
board.Servo.detach(9) #free pin 9
board.Servo.detach(10) #free pin 10
```

**Software Serial Functionality**

- `Arduino.SoftwareSerial.begin(ss_rxPin,ss_txPin,ss_device_baud)` initialize software serial device on 
specified pins. 
Only one sofware serial device can be used at a time. Existing software serial instance will 
be be overwritten by calling this method, both in Python and on the arduino board.
- `Arduino.SoftwareSerial.write(data)` send data using the arduino 'write' function to the existing software serial connection.
- `Arduino.SoftwareSerial.read()` returns one byte from the existing software serial connection

```python
#Software serial example
board.SoftwareSerial.begin(0,7,"19200") # Start software serial for transmit only (tx on pin 7)
board.SoftwareSerial.write(" test ") #Send some data 
response_char = board.SoftwareSerial.read() #read response character
```

**Misc**

- `Arduino.close()` closes serial connection to the Arduino.

## To-do list:
- Expand software serial functionality (`print()` and `println()`)
- Add simple reset functionality that zeros out all pin values
- Add I2C / TWI function support (Arduino `Wire.h` commands)
- Add `tone()` / `noTone()` squarewave generator support for piezo type speakers
- Include a wizard which generates 'prototype.ino' with selected serial baud rate and Arduino function support (to help reduce memory requirements).
- Multi-serial support for Arduino mega (`Serial1.read()`, etc)
