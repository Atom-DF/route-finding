import unittest

import Robot
import Search
import Board
import Enemy


class TestSum(unittest.TestCase):
    def test_list_int(self):
        result = Robot.heuristic((1, 2), (2, 3))
        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()