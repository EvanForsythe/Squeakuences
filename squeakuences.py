#!/usr/bin/env python3
import argparse
import re
import os
import csv

def main():
  parser = setupParser()
  args = parseArguments(parser)
  write = args.write

  sequenceIdCount = 0
  idDict = {}

  faFileNameExt, fastaHandle, faFileName = loadFile(args.input)
  
  squeakyFileName = write + '/' + faFileName + '_squeak.fa'
  squeakyDictFile = write + '/' + faFileName + '_squeakMods.tsv'

  checkExisting(squeakyDictFile, squeakyFileName)

  for line in fastaHandle:
    if isSequenceId(line):
      sequenceIdCount += 1
      startId = stripSequenceId(line)
      #Linnea: revist camelCase situtation
      endId = removeSpaces(startId)
      endId = removeNonAlphanumeric(endId)
      endId = speciesName(endId, faFileName)
      endId = chop(endId)

      idDict.update({startId: endId})

  writeModIDFile(write + '/' + faFileName, idDict)


def loadFile(file):
  faFileNameExt = os.path.basename(file)
  fastaHandle = open(file, 'r')
  faFileName = os.path.splitext(faFileNameExt)[0]
  return faFileNameExt, fastaHandle, faFileName

def checkExisting(squeakyDictFile, squeakyFileName):
  if os.path.exists(squeakyDictFile):
    os.remove(squeakyDictFile)
    print('Existing squeaky dictionary file deleted.')

  if os.path.exists(squeakyFileName):
    os.remove(squeakyFileName)
    print('Existing squeaky fa file deleted.')

def isSequenceId(line):
  return line.startswith('>')

def stripSequenceId(line):
  line = line.strip('>')
  line = line.strip('\n')
  return line

#######################################
# Non Alpha-Numeric Removal Functions #
#######################################

def removeSpaces(sequenceID):
  modifiedID = re.sub(r'\s', '', sequenceID)
  return modifiedID

def removeNonAlphanumeric(sequenceID):
  modifiedID = re.sub(r'[^a-zA-Z0-9\s]', '', sequenceID)
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
  
def writeModIDFile(faFileName, idDictInput):
  fileExtension = os.path.splitext(faFileName)
  newFileName = fileExtension[0] + '_squeakMods.tsv'
  
  with open(newFileName, 'w') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    for k, v in idDictInput.items():
      writer.writerow([k, v])
  tsvfile.close()

# TODO: add/write function for dealing with duplciates

# TODO: add/write function/code for writing before-after file

# TODO: add/write function/code for writing new squeaky clean file  

# Create tests for these???
def setupParser():
    parser = argparse.ArgumentParser()
    # Add parser arguments. ex: parser.add_argument('-l', '--long_name', help='What is it for?', required=True/False)
    parser.add_argument('-i', '--input', help='Input file', required=True)
    parser.add_argument('-w', '--write', help='Output Location', required=True)
    # add arg for chop function length
    # add arg for write location
    return parser
  
def parseArguments(parser):
    args = parser.parse_args()
    # Place any messages you may want
    return args

if __name__ == '__main__':
  main()