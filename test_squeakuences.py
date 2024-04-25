#!/usr/bin/env python3
from io import TextIOWrapper
import unittest
import squeakuences
import os
from pyfakefs import fake_filesystem_unittest

# TODO: add test(s) for parser?
# TODO: add test for duplicates

class TestFileMethods(fake_filesystem_unittest.TestCase):
  # Set up the fake file system
  def setUp(self):
    self.setUpPyfakefs()
    if not os.path.exists('test.fa'):
      self.fs.create_file('test.fa')

  # Does loadFile load file properly
  def test_loadFile(self):
    self.setUp()
    faFileNameExt, fastaHandle, faFileName = squeakuences.loadFile('test.fa')
    self.assertEqual(faFileNameExt, 'test.fa')
    #self.assertIsInstance(fastaHandle, TextIOWrapper)
    self.assertEqual(faFileName, 'test')
    fastaHandle.close()

  # Does checkExisting remove file(s) from previous squeakuences runs
  def test_checkExisting(self):
    self.setUp()
    filePathTrue = 'test.fa'
    filePathFalse = 'notThere.faa'
    
    #Test first parameter
    self.assertTrue(os.path.exists(filePathTrue))
    self.assertFalse(os.path.exists(filePathFalse))

    squeakuences.checkExisting(filePathTrue, filePathFalse)

    self.assertFalse(os.path.exists(filePathTrue))
    self.assertFalse(os.path.exists(filePathFalse))

    #Test second parameter
    self.setUp()
    self.assertTrue(os.path.exists(filePathTrue))
    self.assertFalse(os.path.exists(filePathFalse))

    squeakuences.checkExisting(filePathFalse, filePathTrue)

    self.assertFalse(os.path.exists(filePathTrue))
    self.assertFalse(os.path.exists(filePathFalse))

  # Does writeLine append a line to the file with > \n if needed
  def test_writeLine(self):  
    self.setUp()
    squeakyFileName = 'test_squeaky.fa'
    seqId = 'MySequenceID'
    aaData = 'ABCD'
    squeakuences.writeLine(squeakyFileName, seqId, True)
    squeakuences.writeLine(squeakyFileName, aaData, False)

    self.assertTrue(os.path.exists(squeakyFileName))

    with open("test_squeaky.fa") as f:
      contents = f.readlines()

    self.assertIn('>MySequenceID\n', contents)
    self.assertIn('ABCD', contents)

  # Does writeModIdFile write a new file with the dirty and clean sequence ids
  def test_writeModIdFile(self):
    modIdFileName = 'my_sequences'
    modIdDict = {
      'Agepho_acid-sensing ion channel 5': 'Agepho_acidsensingionchannel5',
      'Acachl_14-3-3 protein gamma': 'Acachl_1433ProteinGamma',
      'Galgal_catenin alpha-1': 'Galgal_CateninAlpha1'
    }

    squeakuences.writeModIdFile(modIdFileName, modIdDict)

    with open("my_sequences_squeakMods.tsv") as f:
        contents = f.readlines()

    self.assertIn('Agepho_acid-sensing ion channel 5\tAgepho_acidsensingionchannel5\n', contents)
    self.assertIn('Acachl_14-3-3 protein gamma\tAcachl_1433ProteinGamma\n', contents)
    self.assertIn('Galgal_catenin alpha-1\tGalgal_CateninAlpha1\n', contents)


class TestSequenceMethods(unittest.TestCase):
  # Does isSequenceId identify a line begining with > as being true
  def test_isSequenceIdTrue(self):
    self.assertEqual(squeakuences.isSequenceId('> This line is true'), True)

  # Does isSequenceId identify a line not begining with > as being false
  def test_isSequenceIdFalse(self):
    self.assertEqual(squeakuences.isSequenceId('This line is false'), False)

  # Does stripSequenceId remove > and \n from a given line
  def test_stripSequenceId(self):
    funcInput = '>Galgal_14-3-3 protein gamma\n'
    funcOutput = 'Galgal_14-3-3 protein gamma'
    self.assertEqual(squeakuences.stripSequenceId(funcInput), funcOutput)

  # Does camelCase captitalize all the words in a sequence id
  def test_camelCase(self):
    input_sequence = 'Galgal_BTB/POZ domain-containing protein KCTD12'
    self.assertEqual(squeakuences.camelCase(input_sequence), 'Galgal BTB/POZ Domain Containing Protein KCTD12')

  # Does removeSpaces remove whitespace
  def test_removeSpaces(self):
    self.assertEqual(squeakuences.removeSpaces('Remove Spaces '), 'RemoveSpaces')
    self.assertEqual(squeakuences.removeSpaces('Remove  Spaces'), 'RemoveSpaces')
    self.assertEqual(squeakuences.removeSpaces('Acachl_aminoacyl tRNA synthase complex-interacting multifunctional protein 1-like, partial'), 'Acachl_aminoacyltRNAsynthasecomplex-interactingmultifunctionalprotein1-like,partial')

  # Does removeNonAlphanumeric remove brackets from a given line
  def test_removeNonAlphanumeric(self):
    self.assertEqual(squeakuences.removeNonAlphanumeric('Re(mov{e br[ack}]ets)'), 'Remove brackets')
    self.assertEqual(squeakuences.removeNonAlphanumeric('.R`e=m+o:v_e. /p"u?n¿c!¡t:;u&a$t*i@*o%#n'), 'Remove punctuation')
    self.assertEqual(squeakuences.removeNonAlphanumeric('Acachl_[Pyruvate dehydrogenase [acetyl-transferring]]-phosphatase 2, mitochondrial'), 'AcachlPyruvate dehydrogenase acetyltransferringphosphatase 2 mitochondrial')

  # Does removeNonAlphanumeric remove any non english characters
  def test_remove_non_english_characters(self):
    self.assertEqual(squeakuences.removeNonAlphanumeric('R¥emÙove ÅnoĦn-engŧlish chaŸracters'), 'Remove nonenglish characters')

  # Does speciesName ensure that the sequence id always begins with the species name and an underscore
  def test_speciesName(self):
    self.assertEqual(squeakuences.speciesName('AcachlArg8VasotocinReceptorLike', 'Acachl'), 'Acachl_Arg8VasotocinReceptorLike')
    self.assertEqual(squeakuences.speciesName('Arg8VasotocinReceptorLike', 'Acachl'), 'Acachl_Arg8VasotocinReceptorLike')

  # Does chop shorten a sequence id to either the default or given maximum length
  def test_chop(self):
    self.assertEqual(squeakuences.chop('Acachl_PyruvateDehydrogenaseAcetylTransferringKinaseIsozyme1Mitochondrial'), 'Acachl_PyruvateDehydrogenaseAcetyl___KinaseIsozyme1Mitochondrial')
    self.assertEqual(squeakuences.chop('Acachl_ADisintegrinAndMetalloproteinaseWithThrombospondinMotifs18Partial'), 'Acachl_ADisintegrinAnd___WithThrombospondinMotifs18Partial')
    self.assertEqual(squeakuences.chop('Acachl_MembraneAssociatedGuanylateKinaseWwAndPdzDomainContainingProtein1', 40), 'Acachl_Membrane___ContainingProtein1')

if __name__ == '__main__':
  unittest.main()
