#!/usr/bin/env python3
from io import TextIOWrapper
import unittest
import squeakuences
import os

class TestStringMethods(unittest.TestCase):

  # Does load_file load file properly
  def testLoadFile(self):
    faFile, fastaHandle = squeakuences.loadFile('test.txt')
    self.assertEqual(faFile, 'test.txt')
    self.assertIsInstance(fastaHandle, TextIOWrapper)
    fastaHandle.close()

  # Does is_squence_id identify a line begining with > as being true
  def testIsSequenceIdTrue(self):
    self.assertEqual(squeakuences.isSequenceId('> This line is true'), True)

  # Does is_squence_id identify a line not begining with > as being false
  def testIsSequenceIdFalse(self):
    self.assertEqual(squeakuences.isSequenceId('This line is false'), False)

  # Does remove_brackets remove brackets from a given line
  def test_removeNonAlphanumeric(self):
    self.assertEqual(squeakuences.removeNonAlphanumeric('Re(mov{e br[ack}]ets)'), 'Remove brackets')
    self.assertEqual(squeakuences.removeNonAlphanumeric('.R`e=m+o:v_e. /p"u?n¿c!¡t:;u&a$t*i@*o%#n'), 'Remove punctuation')
    self.assertEqual(squeakuences.removeNonAlphanumeric('Acachl_[Pyruvate dehydrogenase [acetyl-transferring]]-phosphatase 2, mitochondrial'), 'AcachlPyruvate dehydrogenase acetyltransferringphosphatase 2 mitochondrial')

  # Does remove_non_english_characters remove any non english characters
  def test_remove_non_english_characters(self):
    self.assertEqual(squeakuences.removeNonAlphanumeric('R¥emÙove ÅnoĦn-engŧlish chaŸracters'), 'Remove nonenglish characters')

  # Does remove_non_english_characters remove any non english characters
  def test_removeSpaces(self):
    self.assertEqual(squeakuences.removeSpaces('Remove Spaces '), 'RemoveSpaces')
    self.assertEqual(squeakuences.removeSpaces('Remove  Spaces'), 'RemoveSpaces')
    self.assertEqual(squeakuences.removeSpaces('Acachl_aminoacyl tRNA synthase complex-interacting multifunctional protein 1-like, partial'), 'Acachl_aminoacyltRNAsynthasecomplex-interactingmultifunctionalprotein1-like,partial')

  def test_speciesName(self):
    self.assertEqual(squeakuences.speciesName('AcachlArg8VasotocinReceptorLike', 'Acachl'), 'Acachl_Arg8VasotocinReceptorLike')
    self.assertEqual(squeakuences.speciesName('Arg8VasotocinReceptorLike', 'Acachl'), 'Acachl_Arg8VasotocinReceptorLike')

  def test_chop(self):
    self.assertEqual(squeakuences.chop('Acachl_PyruvateDehydrogenaseAcetylTransferringKinaseIsozyme1Mitochondrial'), 'Acachl_PyruvateDehydrogenaseAcetyl___KinaseIsozyme1Mitochondrial')
    self.assertEqual(squeakuences.chop('Acachl_ADisintegrinAndMetalloproteinaseWithThrombospondinMotifs18Partial'), 'Acachl_ADisintegrinAnd___WithThrombospondinMotifs18Partial')
    self.assertEqual(squeakuences.chop('Acachl_MembraneAssociatedGuanylateKinaseWwAndPdzDomainContainingProtein1', 40), 'Acachl_Membrane___ContainingProtein1')

  # TODO: add test for checkExisting

  # TODO: add test for adding to dictionary?
  
  # TODO: add test for duplicates
  
  # TODO: add test for adding species name with underscore
  
  # TODO: add test for writing to file?

if __name__ == '__main__':
  unittest.main()
