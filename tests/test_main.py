import logging
import unittest
import time

"""
A collection of some basic tests for the Arduino library.

Extensive coverage is a bit difficult, since a positive test involves actually
connecting and issuing commands to a live Arduino, hosting any hardware
required to test a particular function. But a core of basic communication tests
should at least be maintained here.
"""


logging.basicConfig(level=logging.DEBUG)

# Bind raw_input to input in python 2.7
try:
    input = raw_input
except NameError:
    pass


class TestBasics(unittest.TestCase):

    def test_find(self):
        """ Tests auto-connection/board detection. """
        input(
            'Plug in Arduino board w/LED at pin 13, reset, then press enter')
        from Arduino import Arduino
        board = None
        try:
            # This will trigger automatic port resolution.
            board = Arduino(115200)
        finally:
            if board:
                board.close()

    def test_open(self):
        """ Tests connecting to an explicit port. """
        port = None
        while not port:
            port = input(
                'Plug in Arduino board w/LED at pin 13, reset.\n'\
                'Enter the port where the Arduino is connected, then press enter:')
            if not port:
                print('You must enter a port.')
        from Arduino import Arduino
        board = None
        try:
            board = Arduino(115200, port=port)
        finally:
            if board:
                board.close()

if __name__ == '__main__':
    unittest.main()
