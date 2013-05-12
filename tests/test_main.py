import unittest
import time
from Arduino import Arduino

"""
A collection of some basic tests for the Arduino library.

Extensive coverage is a bit difficult, since a positive test involves actually
connecting and issuing commands to a live Arduino, hosting any hardware
required to test a particular function. But a core of basic communication tests
should at least be maintained here.
"""


class TestBasics(unittest.TestCase):
    _ = raw_input('Plug in Arduino board w/LED at pin 13, then press enter')
    board = Arduino('9600')

    def test_find(self):
        """
        Tests auto-connection/board detection
        """
        self.assertIsNotNone(self.board.port)

    def test_blink(self):
        """
        Tests digital pin functionality
        """
        led_pin = 13
        self.board.digitalWrite(led_pin, "LOW")
        state = self.board.digitalRead(led_pin)
        self.assertEqual(state, 0)

        time.sleep(1)

        self.board.digitalWrite(led_pin, "HIGH")
        state = self.board.digitalRead(led_pin)
        self.assertEqual(state, 1)

        self.board.digitalWrite(led_pin, "LOW")

if __name__ == '__main__':
    unittest.main()
