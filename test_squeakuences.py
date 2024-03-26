#!/usr/bin/env python3
import unittest
import squeakuences

class TestStringMethods(unittest.TestCase):

  def test_hello_world(self):
    self.assertEqual(squeakuences.hello_world(), 'Hello world!')

if __name__ == '__main__':
  unittest.main()