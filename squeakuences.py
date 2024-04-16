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

def removeSpaces(seqName):
  modifiedName = seqName.strip()
  modifiedName = modifiedName.replace(' ', '')
  modifiedName = modifiedName.replace('\t', '')
  return modifiedName

def removeNonAlphanumeric(seqName):
  modifiedName = re.sub(r'[^a-zA-Z0-9]', '', seqName)
  return modifiedName

# Optional?
def remove_non_english_characters(sequence_id):
  # TODO: Remove any non-english characters
  # Regex: /<-[a..zA..Z\s]>+/  <<< Do we need this to include numbers? This is saying anything that isn't an english alphabetic letter
  return

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
