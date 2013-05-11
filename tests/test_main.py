import unittest
from Arduino import Arduino


class TestConnect(unittest.TestCase):

    def test_find(self):
        board = Arduino('9600')
        self.assertIsNotNone(board.port)


if __name__ == '__main__':
    unittest.main()
