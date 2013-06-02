import logging
import unittest


logging.basicConfig(level=logging.DEBUG)


class MockSerial(object):

    def __init__(self, baud, port, timeout=None):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.output = []
        self.input = []

    def flush(self):
        pass

    def write(self, line):
        self.output.append(line)

    def readline(self):
        """
        @TODO: This does not take timeout into account at all.
        """
        return self.input.pop(0)

    def reset_mock(self):
        self.output = []
        self.input = []

    def push_line(self, line, term='\r\n'):
        self.input.append(str(line) + term)


INPUT = "INPUT"
OUTPUT = "OUTPUT"
LOW = "LOW"
HIGH = "HIGH"
READ_LOW = 0
READ_HIGH = 1
MSBFIRST = "MSBFIRST"
LSBFIRST = "LSBFIRST"


class TestArduino(unittest.TestCase):

    def parse_cmd_sr(self, cmd_str):
        assert cmd_str[0] == '@'
        first_index = cmd_str.find('%')
        assert first_index != -1
        assert cmd_str[-2:] == '$!'
        # Skip over the @ and read up to but not including the %.
        cmd = cmd_str[1:first_index]
        # Skip over the first % and ignore the trailing $!.
        args_str = cmd_str[first_index+1:-2]
        args = args_str.split('%')
        return cmd, args

    def setUp(self):
        from Arduino.arduino import Arduino
        self.mock_serial = MockSerial(9600, '/dev/ttyACM0')
        self.board = Arduino(sr=self.mock_serial)

    def test_version(self):
        from Arduino.arduino import build_cmd_str
        expected_version = "version"
        self.mock_serial.push_line(expected_version)
        self.assertEquals(self.board.version(), expected_version)
        self.assertEquals(self.mock_serial.output[0], build_cmd_str('version'))

    def test_pinMode_input(self):
        from Arduino.arduino import build_cmd_str
        pin = 9
        self.board.pinMode(pin, INPUT)
        self.assertEquals(self.mock_serial.output[0],
            build_cmd_str('pm', (-pin,)))

    def test_pinMode_output(self):
        from Arduino.arduino import build_cmd_str
        pin = 9
        self.board.pinMode(pin, OUTPUT)
        self.assertEquals(self.mock_serial.output[0],
            build_cmd_str('pm', (pin,)))

    def test_pulseIn_low(self):
        from Arduino.arduino import build_cmd_str
        expected_duration = 230
        self.mock_serial.push_line(expected_duration)
        pin = 9
        self.assertEquals(self.board.pulseIn(pin, LOW), expected_duration)
        self.assertEquals(self.mock_serial.output[0],
            build_cmd_str('pi', (-pin,)))

    def test_pulseIn_high(self):
        from Arduino.arduino import build_cmd_str
        expected_duration = 230
        pin = 9
        self.mock_serial.push_line(expected_duration)
        self.assertEquals(self.board.pulseIn(pin, HIGH), expected_duration)
        self.assertEquals(self.mock_serial.output[0], build_cmd_str('pi', (pin,)))

    def test_digitalRead(self):
        from Arduino.arduino import build_cmd_str
        pin = 9
        self.mock_serial.push_line(READ_LOW)
        self.assertEquals(self.board.digitalRead(pin), READ_LOW)
        self.assertEquals(self.mock_serial.output[0], build_cmd_str('dr', (pin,)))

    def test_digitalWrite_low(self):
        from Arduino.arduino import build_cmd_str
        pin = 9
        self.board.digitalWrite(pin, LOW)
        self.assertEquals(self.mock_serial.output[0], build_cmd_str('dw', (-pin,)))

    def test_digitalWrite_high(self):
        from Arduino.arduino import build_cmd_str
        pin = 9
        self.board.digitalWrite(pin, HIGH)
        self.assertEquals(self.mock_serial.output[0], build_cmd_str('dw', (pin,)))

    def test_melody(self):
        from Arduino.arduino import build_cmd_str
        pin = 9
        notes = ["C4"]
        duration = 4
        C4_NOTE = 262
        self.board.Melody(pin, notes, [duration])
        self.assertEquals(self.mock_serial.output[0],
            build_cmd_str('to', (len(notes), pin, C4_NOTE, duration)))
        self.assertEquals(self.mock_serial.output[1],
            build_cmd_str('nto', (pin,)))

    def test_shiftIn(self):
        from Arduino.arduino import build_cmd_str
        dataPin = 2
        clockPin = 3
        pinOrder = MSBFIRST
        expected = 0xff
        self.mock_serial.push_line(expected)
        self.assertEquals(self.board.shiftIn(dataPin, clockPin, pinOrder),
            expected)
        self.assertEquals(self.mock_serial.output[0],
            build_cmd_str('si', (dataPin, clockPin, pinOrder,)))

    def test_shiftOut(self):
        from Arduino.arduino import build_cmd_str
        dataPin = 2
        clockPin = 3
        pinOrder = MSBFIRST
        value = 0xff
        self.board.shiftOut(dataPin, clockPin, pinOrder, value)
        self.assertEquals(self.mock_serial.output[0],
            build_cmd_str('so', (dataPin, clockPin, pinOrder, value)))

    def test_analogRead(self):
        from Arduino.arduino import build_cmd_str
        pin = 9
        expected = 1023
        self.mock_serial.push_line(expected)
        self.assertEquals(self.board.analogRead(pin), expected)
        self.assertEquals(self.mock_serial.output[0],
            build_cmd_str('ar', (pin,)))

    def test_analogWrite(self):
        from Arduino.arduino import build_cmd_str
        pin = 9
        value = 255
        self.board.analogWrite(pin, value)
        self.assertEquals(self.mock_serial.output[0],
            build_cmd_str('aw', (pin, value)))


if __name__ == '__main__':
    unittest.main()
