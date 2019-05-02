# Arduino-Python3 Command API

This API is forked from the original [Python Arduino Command API](https://github.com/thearn/Python-Arduino-Command-API) to add support for Python 3.

The Arduino-Python3 Command API is a lightweight Python library for
communicating with [Arduino microcontroller boards](http://www.arduino.cc/) from a connected computer using
standard serial IO, either over a physical wire
or wirelessly. It is written using a custom protocol, similar to [Firmata](http://firmata.org/wiki/Main_Page).

This allows a user to quickly prototype programs for Arduino using Python code, or to
simply read/control/troubleshoot/experiment
with hardware connected to an Arduino board without ever having to recompile and reload sketches to the board itself.

Method names within the Arduino-Python3 Command API are designed to be as close
as possible to their Arduino programming language counterparts

## Simple usage example (LED blink)
```python
#!/usr/bin/env python
"""
 Blinks an LED on digital pin 13
 in 1 second intervals
"""

from Arduino import Arduino
import time

board = Arduino() # plugged in via USB, serial com at rate 115200
board.pinMode(13, "OUTPUT")

while True:
    board.digitalWrite(13, "LOW")
    time.sleep(1)
    board.digitalWrite(13, "HIGH")
    time.sleep(1)
```

## Requirements:
- [Python](http://python.org/) 3.7 tested on Windows and macOS.
- [pyserial](http://pyserial.sourceforge.net/) 2.6 or higher
- Any [Arduino compatible microcontroller](https://www.sparkfun.com/categories/242) with at least 14KB of flash memory

## Installation:
Either run `pip install arduino-python3` from a command line, or run `python setup.py
build install` from the source directory to install this library.

## Setup:
1. Verify that your Arduino board communicates at the baud rate specified in the
`setup()` function (line 348) in `prototype.ino`. Change it there if necessary.
2. Load the `prototype.ino` sketch onto your Arduino board, using the Arduino IDE.
3. Set up some kind of serial I/O communication between the Arduino board and your computer (via physical USB cable,
Bluetooth, xbee, etc. + associated drivers)
4. Add `from Arduino import Arduino` into your python script to communicate with your Arduino

For a collection of examples, see `examples.py`. This file contains methods which replicate
the functionality of many Arduino demo sketches.

## Testing:
The `tests` directory contains some basic tests for the library. Extensive code coverage is a bit difficult to expect for every release, since a positive test involves actually
connecting and issuing commands to a live Arduino, hosting any hardware
required to test a particular function. But a core of basic communication tests
should at least be maintained here and used before merging into the `master` branch.

After installation, the interactive tests can be run from the source directory:
```bash
$ python tests/test_main.py
```

Automated tests can be run from the source directory with:
```bash
$ python tests/test_arduino.py
```

## Classes
- `Arduino(baud)` - Set up communication with currently connected and powered
Arduino.

```python
board = Arduino("115200") #Example
```

The device name / COM port of the connected Arduino will be auto-detected.
If there are more than one Arduino boards connected,
the desired COM port can be also be passed as an optional argument:

```python
board = Arduino("115200", port="COM3") #Windows example
```
```python
board = Arduino("115200", port="/dev/tty.usbmodemfa141") #OSX example
```

A time-out for reading from the Arduino can also be specified as an optional
argument:

```python
board = Arduino("115200", timeout=2) #Serial reading functions will
#wait for no more than 2 seconds
```

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

**Shift Register**

- `Arduino.shiftIn(dataPin, clockPin, bitOrder)` shift a byte in and returns it
- `Arduino.shiftOut(dataPin, clockPin, bitOrder, value)` shift the given byte out

`bitOrder` should be either `"MSBFIRST"` or `"LSBFIRST"`

**Servo Library Functionality**
Support is included for up to 8 servos.

- `Arduino.Servos.attach(pin, min=544, max=2400)` Create servo instance. Only 8 servos can be used at one time.
- `Arduino.Servos.read(pin)` Returns the angle of the servo attached to the specified pin
- `Arduino.Servos.write(pin, angle)` Move an attached servo on a pin to a specified angle
- `Arduino.Servos.writeMicroseconds(pin, uS)` Write a value in microseconds to the servo on a specified pin
- `Arduino.Servos.detach(pin)` Detaches the servo on the specified pin

```python
#Servo example
board.Servos.attach(9) #declare servo on pin 9
board.Servos.write(9, 0) #move servo on pin 9 to 0 degrees
print board.Servos.read(9) # should be 0
board.Servos.detach(9) #free pin 9
```

**Software Serial Functionality**

- `Arduino.SoftwareSerial.begin(ss_rxPin, ss_txPin, ss_device_baud)` initialize software serial device on
specified pins.
Only one software serial device can be used at a time. Existing software serial instance will
be overwritten by calling this method, both in Python and on the Arduino board.
- `Arduino.SoftwareSerial.write(data)` send data using the Arduino 'write' function to the existing software
serial connection.
- `Arduino.SoftwareSerial.read()` returns one byte from the existing software serial connection

```python
#Software serial example
board.SoftwareSerial.begin(0, 7, "19200") # Start software serial for transmit only (tx on pin 7)
board.SoftwareSerial.write(" test ") #Send some data
response_char = board.SoftwareSerial.read() #read response character
```

**EEPROM**

- `Arduino.EEPROM.read(address)` reads a byte from the EEPROM
- `Arduino.EEPROM.write(address, value)` writes a byte to the EEPROM
- `Arduino.EEPROM.size()` returns size of the EEPROM

```python
#EEPROM read and write examples
location = 42
value = 10 # 0-255(byte)

board.EEPROM.write(location, 10)
print(board.EEPROM.read(location))
print('EEPROM size {size}'.format(size=board.EEPROM.size()))
```

**Screen**
Display text on an LCD screen.
Use the function displayText(text, fontSize = 1) to display a string on the screen.

**DHT**

- `Arduino.dht(pin, module)` reads sensor values from the DHT sensor connected at the specified pin.

Read data from DHT temperature and humidity sensors based on the
Adafruit [DHT sensor library](https://github.com/adafruit/DHT-sensor-library).

Pass as arguments the pin the sensor is connected to (as an integer) and the sensor type you are using as an integer (see list below).

There are five sensors that work with this library:
- 0 = DHT 11 (blue cage, less accurate)
- 1 = DHT 12
- 2 = DHT 21
- 3 = DHT 22 (white cage)
- 4 = AM2301

The function returns an array of three elements:
1. humidity (in %)
2. temperature (in Celsius)
3. heat index (in Celsius)

If there is an error with the reading (e.g., the selected sensor is wrong) all values will return as zero.

```python
#DHT sensor example
pin = 7
sensorType = 0

data = board.dht(pin, sensorType)
[humidity, temperature, heatIndex] = data

reply =  "Humidity = " + str(humidity) + " % \t"
reply += "Temperature = " + str(temperature) + " ˙C \t"
reply += "Heat Index = " + str(heatIndex) + " ˙C"

print(reply)
```

**Misc**

- `Arduino.close()` closes serial connection to the Arduino.

## To-do list:
- Expand software serial functionality (`print()` and `println()`)
- Add simple reset functionality that zeros out all pin values
- Add I2C / TWI function support (Arduino `Wire.h` commands)
- Include a wizard which generates 'prototype.ino' with selected serial baud rate and Arduino function support
(to help reduce memory requirements).
- Multi-serial support for Arduino mega (`Serial1.read()`, etc)
