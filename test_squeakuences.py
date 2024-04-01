#!/usr/bin/env python3
import unittest
import squeakuences

class TestStringMethods(unittest.TestCase):

  def test_hello_world(self):
    self.assertEqual(squeakuences.hello_world(), 'Hello world!')

  # Does load_file load file properly
  def test_load_file(self):
    self.assertEqual(squeakuences.load_file(test.txt),
                      'Hello, World\nWelcome to Squeakuences.')

  # Does is_squence_id identify a line begining with > as being true
  def test_is_squence_id_true(self):
    self.assertEqual(squeakuences.is_squence_id('> This line is true'), true)

  # Does is_squence_id identify a line not begining with > as being false
  def test_is_squence_id_false(self):
    self.assertEqual(squeakuences.is_squence_id('This line is false'), false)

  # Does remove_brackets remove brackets from a given line
  def test_remove_brackets(self):
    self.assertEqual(squeakuences.remove_brackets('Re(move{ br[ack}]ets)'), 'Remove brackets')

  # Does remove_punctuation remove all puntuation from a given line
  def test_remove_punctuation(self):
    self.assertEqual(squeakuences.remove_punctuation('.R`e=m+o:v_e. \p"u?n¿c!¡t:;u&a$t*i@*o%#n'), 'Remove punctuation')

  # Does remove_non_english_characters remove any non english characters
  def test_remove_non_english_characters(self):
    self.assertEqual(squeakuences.remove_non_english_characters('R¥emÙove ÅnoĦn-engŧlish chaŸracters'), 'Remove non-english characters')

if __name__ == '__main__':
  unittest.main()