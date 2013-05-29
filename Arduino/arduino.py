#!/usr/bin/env python
import itertools
import platform
import serial
import time
from serial.tools import list_ports
if platform.system() == 'Windows':
    import _winreg as winreg
else:
    import glob


def enumerate_serial_ports():
    """
    Uses the Win32 registry to return a iterator of serial
        (COM) ports existing on this computer.
    """
    path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    except WindowsError:
        raise IterationError

    for i in itertools.count():
        try:
            val = winreg.EnumValue(key, i)
            yield (str(val[1]))  # , str(val[0]))
        except EnvironmentError:
            break


class Arduino(object):
    def __init__(self, baud=9600, port=None, timeout=2):
        """
        Initializes serial communication with Arduino.
        Attempts to self-select COM port, if not specified.
        """
        self.baud = baud
        self.timeout = timeout
        self.ss_connected = False
        self.port = port
        if not self.port:
            self.findPort()
        else:
            self.sr = serial.Serial(self.port, self.baud,
                                    timeout = self.timeout)
        self.SoftwareSerial = SoftwareSerial(self)
        self.Servos = Servos(self)
        self.sr.flush()

    def version(self):
        cmd_str = ''.join(["@version%$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass
        version = self.sr.readline().replace("\r\n", "")
        return version

    def findPort(self):
        """
        Sets port to the first Arduino found
        in system's device list
        """
        if platform.system() == 'Windows':
            ports = enumerate_serial_ports()
        elif platform.system() == 'Darwin':
            ports = [i[0] for i in list_ports.comports()]
        else:
            ports = glob.glob("/dev/ttyUSB*")
        for p in ports:
            print 'Found ', p
            version = None
            try:
                print 'Testing ', p
                self.sr = serial.Serial(p, self.baud, timeout=self.timeout)
                time.sleep(2)
                version = self.version()
                if version != 'version':
                    raise Exception('This is not a Shrimp/Arduino!')
                self.port = p
                print p, 'passed'
                break
            except Exception, e:
                print "Exception: ", e
                pass

    def digitalWrite(self, pin, val):
        """
        Sends digitalWrite command
        to digital pin on Arduino
        -------------
        inputs:
           pin : digital pin number
           val : either "HIGH" or "LOW"
        """
        if val == "LOW":
            pin_ = -pin
        else:
            pin_ = pin
        cmd_str = ''.join(["@dw%", str(pin_), "$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass

    def analogWrite(self, pin, val):
        """
        Sends analogWrite pwm command
        to pin on Arduino
        -------------
        inputs:
           pin : pin number
           val : integer 0 (off) to 255 (always on)
        """
        if val > 255:
            val = 255
        elif val < 0:
            val = 0
        cmd_str = ''.join(["@aw%", str(pin), "%", str(val), "$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass

    def analogRead(self, pin):
        """
        Returns the value of a specified
        analog pin.
        inputs:
           pin : analog pin number for measurement
        returns:
           value: integer from 1 to 1023
        """
        cmd_str = ''.join(["@ar%", str(pin), "$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass
        rd = self.sr.readline().replace("\r\n", "")
        try:
            return int(rd)
        except:
            return 0

    def pinMode(self, pin, val):
        """
        Sets I/O mode of pin
        inputs:
           pin: pin number to toggle
           val: "INPUT" or "OUTPUT"
        """
        if val == "INPUT":
            pin_ = -pin
        else:
            pin_ = pin
        cmd_str = ''.join(["@pm%", str(pin_), "$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass

    def pulseIn(self, pin, val):
        """
        Reads a pulse from a pin

        inputs:
           pin: pin number for pulse measurement
        returns:
           duration : pulse length measurement
        """
        if val == "LOW":
            pin_ = -pin
        else:
            pin_ = pin
        cmd_str = ''.join(["@pi%", str(pin_), "$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass
        rd = self.sr.readline().replace("\r\n", "")
        try:
            return float(rd)
        except:
            return -1

    def pulseIn_set(self, pin, val, numTrials=5):
        """
        Sets a digital pin value, then reads the response
        as a pulse width.
        Useful for some ultrasonic rangefinders, etc.

        inputs:
           pin: pin number for pulse measurement
           val: "HIGH" or "LOW". Pulse is measured
                when this state is detected
           numTrials: number of trials (for an average)
        returns:
           duration : an average of pulse length measurements

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
        if val == "LOW":
            pin_ = -pin
        else:
            pin_ = pin
        cmd_str = ''.join(["@ps%", str(pin_), "$!"])
        durations = []
        for s in range(numTrials):
            try:
                self.sr.write(cmd_str)
                self.sr.flush()
            except:
                pass
            rd = self.sr.readline().replace("\r\n", "")
            if rd.isdigit():
                if (int(rd) > 1):
                    durations.append(int(rd))
        if len(durations) > 0:
            duration = int(sum(durations)) / int(len(durations))
        else:
            duration = None

        try:
            return float(duration)
        except:
            return -1

    def close(self):
        self.sr.flush()
        self.sr.close()

    def digitalRead(self, pin):
        """
        Returns the value of a specified
        digital pin.
        inputs:
           pin : digital pin number for measurement
        returns:
           value: 0 for "LOW", 1 for "HIGH"
        """
        cmd_str = ''.join(["@dr%", str(pin), "$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass
        rd = self.sr.readline().replace("\r\n", "")
        try:
            return int(rd)
        except:
            return 0

    def Melody(self, pin, melody, durations):
        """
        Plays a melody.
        inputs:
            pin: digital pin number for playback
            melody: list of tones
            durations: list of duration (4=quarter note, 8=eighth note, etc.)
        length of melody should be of same
        length as length of duration

        Melodies of the following lenght, can cause trouble
        when playing it multiple times.
            board.Melody(9,["C4","G3","G3","A3","G3",0,"B3","C4"],
                                                [4,8,8,4,4,4,4,4])
        Playing short melodies (1 or 2 tones) didn't cause
        trouble during testing
        """
        NOTES = dict(B0=31,C1=33,CS1=35,D1=37,DS1=39,E1=41,F1=44,FS1=46,G1=49\
                 ,GS1=52,A1=55,AS1=58,B1=62,C2=65,CS2=69,D2=73,DS2=78,E2=82\
                 ,F2=87,FS2=93,G2=98,GS2=104,A2=110,AS2=117,B2=123,C3=131\
                 ,CS3=139,D3=147,DS3=156,E3=165,F3=175,FS3=185,G3=196,GS3=208\
                 ,A3=220,AS3=233,B3=247,C4=262,CS4=277,D4=294,DS4=311,E4=330\
                 ,F4=349,FS4=370,G4=392,GS4=415,A4=440,AS4=466,B4=494,C5=523\
                 ,CS5=554,D5=587,DS5=622,E5=659,F5=698,FS5=740,G5=784,GS5=831\
                 ,A5=880,AS5=932,B5=988,C6=1047,CS6=1109,D6=1175,DS6=1245,E6=1319\
                 ,F6=1397,FS6=1480,G6=1568,GS6=1661,A6=1760,AS6=1865,B6=1976,C7=2093\
                 ,CS7=2217,D7=2349,DS7=2489,E7=2637,F7=2794,FS7=2960,G7=3136\
                 ,GS7=3322,A7=3520,AS7=3729,B7=3951,C8=4186,CS8=4435,D8=4699,DS8=4978)
        if (type(melody) == list) and (type(durations) == list):
            length = len(melody)
            cmd_str = "@to%"+str(length)+"%"+str(pin)+"%"
            d = ""
            if length == len(durations):
                for note in range(length):
                    n = NOTES.get(melody[note])
                    cmd_str = cmd_str+str(n)+"%"
                for duration in range(len(durations)):
                    d = str(durations[duration])
                    cmd_str = cmd_str+d+"%"
                cmd_str = cmd_str[:-1]+"$!"
                try:
                    self.sr.write(cmd_str)
                    self.sr.flush()
                except:
                    pass
                cmd_str=''.join(["@nto%",str(pin),"$!"])
                try:
                    self.sr.write(cmd_str)
                    self.sr.flush()
                except:
                    pass
            else:
                return -1
        else:
            return -1


    def capacitivePin(self, pin):
        '''
        Input:
            pin (int): pin to use as capacitive sensor

        Use it in a loop!
        DO NOT CONNECT ANY ACTIVE DRIVER TO THE USED PIN !

        the pin is toggled to output mode to discharge the port,
        and if connected to a voltage source,
        will short circuit the pin, potentially damaging
        the Arduino/Shrimp and any hardware attached to the pin. 
        '''
        cmd_str="@cap%"+str(pin)+"$!"
        self.sr.write(cmd_str)
        rd = self.sr.readline().replace("\r\n","")
        if rd.isdigit() == True:
            return int(rd)
            

class Shrimp(Arduino):
    def __init__(self):
        Arduino.__init__(self)

        
class Wires(object):            
    """
    Class for Arduino wire (i2c) support
    """
    def __init__(self, board):
        self.board = board
        self.sr = board.sr

        
class Servos(object):
    """
    Class for Arduino servo support
    0.03 second delay noted
    """
    def __init__(self, board):
        self.board = board
        self.sr = board.sr
        self.servo_pos = {}

        
    def attach(self,pin,min = 544, max = 2400):     
        cmd_str=''.join(["@sva%",str(pin),"%",str(min),"%",str(max),"$!"])
        
        while True:
            self.sr.write(cmd_str)
            self.sr.flush()
                
            rd = self.sr.readline().replace("\r\n","")
            if rd:
                break
            else:
                print "trying to attach servo to pin",pin
        position = int(rd)
        self.servo_pos[pin] = position
        return 1

     
    def detach(self,pin):     
        cmd_str=''.join(["@svd%",str(position),"$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass
        del self.servo_pos[pin]


    def write(self,pin,angle):     
        position = self.servo_pos[pin]
        cmd_str=''.join(["@svw%",str(position),"%",str(angle),"$!"])
        
        self.sr.write(cmd_str)
        self.sr.flush()

   
    def writeMicroseconds(self,pin,uS):     
        cmd_str=''.join(["@svw%",str(position),"%",str(uS),"$!"])
        
        self.sr.write(cmd_str)
        self.sr.flush()

   
    def read(self,pin):
        if pin not in self.servo_pos.keys():
            self.attach(pin) 
        position = self.servo_pos[pin]
        cmd_str=''.join(["@svr%",str(position),"$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass
        rd = self.sr.readline().replace("\r\n","")
        try:
            angle = int(rd)
            return angle
        except:
            return None


class SoftwareSerial(object):
    """
    Class for Arduino software serial functionality
    """
    def __init__(self,board):
        self.board=board
        self.sr = board.sr
        self.connected = False


    def begin(self,p1,p2,baud):
        """
        Create software serial instance on 
        specified tx,rx pins, at specified baud
        """
        cmd_str=''.join(["@ss%",str(p1),"%",str(p2),"%",str(baud),"$!"])
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass
        response= self.sr.readline().replace("\r\n","")
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
            try:
                self.sr.write(cmd_str)
                self.sr.flush()
            except:
                pass
            response= self.sr.readline().replace("\r\n","")
            if response == "ss OK":
                return True
        else:
            return False


    def read(self):
        """
        returns first character read from
        existing software serial instance
        """
        if self.connected:
            cmd_str=''.join(["@sr%$!"])
            self.sr.write(cmd_str)
            self.sr.flush()
            response= self.sr.readline().replace("\r\n","")
            if response:
                return response
        else:
            return False         
