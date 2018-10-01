#!/usr/bin/python
# -*-coding: utf-8 -*-

import unittest
from snake import Base


class TestBaseFunctions(unittest.TestCase):
    def test_node_add(self):
        self.assertEqual(Base().node_add((0, 1), (2, 3)), (2, 4))

    def test_node_sub(self):
        self.assertEqual(Base().node_sub((0, 1), (2, 3)), (-2, -2))
