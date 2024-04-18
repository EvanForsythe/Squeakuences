#!/usr/bin/env python3
import argparse
import re
import os

def main():
  parser = setup_parser()
  args = parse_arguments(parser)

  loadFile(args.input)
  
  print("implement")

def loadFile(file):
  faFile = os.path.basename(file)
  fasta_handle = open(file, 'r')
  return faFile, fasta_handle

def isSequenceId(line):
  return line.startswith('>')

#######################################
# Non Alpha-Numeric Removal Functions #
#######################################

def removeSpaces(sequenceID):
  modifiedID = re.sub(r'\s', '', sequenceID)
  return modifiedID

def removeNonAlphanumeric(sequenceID):
  modifiedID = re.sub(r'[^a-zA-Z0-9]', '', sequenceID)
  return modifiedID

# Optional?
def remove_non_english_characters(sequenceID):
  # TODO: Remove any non-english characters
  # Regex: /<-[a..zA..Z\s]>+/  <<< Do we need this to include numbers? This is saying anything that isn't an english alphabetic letter
  return

def speciesName(sequenceID, speciesName):
  if sequenceID.startswith(speciesName):
    underscoreindex = len(speciesName)
    modifiedID = sequenceID[:underscoreindex] + '_' + sequenceID[underscoreindex:]
  else:
    modifiedID = speciesName + '_' + sequenceID
  return modifiedID
    
# TODO: add/write function for chopping seq IDs to a given length
def chop(sequenceID, max = 70):
  length = len(sequenceID)

  if length < max:
    return sequenceID
  else:
    sequenceID = re.sub(r'___', '', sequenceID)
    nameComponents = []
    nameComponents = re.findall(r'[A-Z][^A-Z]*', sequenceID)
    middle = len(nameComponents) // 2
    del nameComponents[middle:middle+1]
    nameComponents.insert(middle, '___')
    newName = ''.join(nameComponents)
    return chop(newName, max)

# TODO: add/write function for dealing with duplciates

# TODO: add/write function/code for writing before-after file

# TODO: add/write function/code for writing new squeaky clean file  

# Create tests for these???
def setup_parser():
    parser = argparse.ArgumentParser()
    # Add parser arguments. ex: parser.add_argument('-l', '--long_name', help='What is it for?', required=True/False)
    parser.add_argument('-i', '--input', help='Input file', required=True/False)
    return parser
  
def parse_arguments(parser):
    args = parser.parse_args()
    # Place any messages you may want
    return args
