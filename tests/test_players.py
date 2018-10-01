#!/usr/bin/python
# -*-coding: utf-8 -*-

import unittest
from snake import LongestPath, Snake, Apple


class TestPlayers(unittest.TestCase):
    def test_longest_path(self):
        snake = Snake(body=[(0, 0), (0, 1), (0, 2)], cell_width=5, cell_height=5)
        apple = Apple(cell_width=5, cell_height=5)
        apple.location = (3, 3)

        LongestPath(snake=snake, apple=apple, cell_width=5, cell_height=5).run_longest()

        self.assertEqual(
            LongestPath(snake=snake, apple=apple, cell_width=8, cell_height=8).run_longest(), [
                (0, 3), (1, 3), (1, 2), (1, 1), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (3, 2), (3, 1), (2, 1),
                (2, 2), (2, 3), (3, 3)
            ]
        )
