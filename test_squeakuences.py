#!/usr/bin/env python3
import unittest
import squeakuences

class TestStringMethods(unittest.TestCase):

  # Does load_file load file properly
  def testLoadFile(self):
    faFile, fastaHandle = squeakuences.loadFile(test.txt)
    self.assertEqual(faFile, 'test')
    self.assertInstance(fastHandle, _io.TextIOWrappe)

  # Does is_squence_id identify a line begining with > as being true
  def testIsSequenceIdTrue(self):
    self.assertEqual(squeakuences.isSequenceId('> This line is true'), true)

  # Does is_squence_id identify a line not begining with > as being false
  def testIsSequenceIdFalse(self):
    self.assertEqual(squeakuences.isSequenceId('This line is false'), false)

  # Does remove_brackets remove brackets from a given line
  def test_remove_brackets(self):
    self.assertEqual(squeakuences.removeNonAlphanumeric('Re(move{ br[ack}]ets)'), 'Remove brackets')

  # Does remove_punctuation remove all puntuation from a given line
  def test_remove_punctuation(self):
    self.assertEqual(squeakuences.removeNonAlphanumeric('.R`e=m+o:v_e. \p"u?n¿c!¡t:;u&a$t*i@*o%#n'), 'Remove punctuation')

  # Does remove_non_english_characters remove any non english characters
  def test_remove_non_english_characters(self):
    self.assertEqual(squeakuences.removeNonAlphanumeric('R¥emÙove ÅnoĦn-engŧlish chaŸracters'), 'Remove non-english characters')

if __name__ == '__main__':
  unittest.main()
