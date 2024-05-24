#!/usr/bin/env python3
import argparse
import re
import os
import csv
import glob

# TODO: decide what we want our output to look like
# TODO: do we need a separate remove non-alphanumeric function?
# TODO: add arguments such as max length, allow underscores, species name, custom replace characters, custom regex. 
# TODO: Make sure all arguements have defaults
# TODO: make sure chop can't return ___ only

def main():
  print('Commencing Squeakuences Cleanup')
  print('================================')

  parser = setupParser()
  args = parseArguments(parser)

  inputType = resolveInput(args.input)
  print('You\'ve input a ' + inputType + '.')
  toProcess = inputList(inputType, args.input)
  
  if inputType == 'directory':
    toClean = getFaNameExt(toProcess)
  else:
    toClean = toProcess
  print('The following file(s) will be cleaned: ' + str(toClean))
  print('--------------------------------')

  ouputPath = checkOutputArg(args.output)
  
  for file in toProcess:
    squeakify(file, ouputPath)
    print('--------------------------------')

  print('Ta-da! Squeaky clean sequence ids!')

def squeakify(file, write):
  sequenceIdCount = 0
  idDict = {}
  idDuplicatesList = []

  faFileNameExt, fastaHandle, faFileName = loadFile(file)
  print('Now processing ' + faFileNameExt)

  squeakyFileName = write + '/' + faFileName + '_squeak.fa'
  squeakyDictFile = write + '/' + faFileName + '_squeakMods.tsv'

  checkExisting(squeakyDictFile, squeakyFileName)

  print('...')

  for line in fastaHandle:
    if isSequenceId(line):
      sequenceIdCount += 1
      startId = stripSequenceId(line)
      endId = camelCase(startId)
      endId = removeSpaces(endId)
      endId = removeNonAlphanumeric(endId)
      endId = speciesName(endId, faFileName)
      endId = chop(endId)
      
      if checkForDuplicates(endId, idDict):
        startId, endId = resolveDuplicate(startId, endId, idDuplicatesList)
        endId = chop(endId)
        
      idDict.update({startId: endId})

      writeLine(squeakyFileName, endId, True)

    else:
      writeLine(squeakyFileName, line, False)

  writeModIdFile(write + '/' + faFileName, idDict)

  print(faFileNameExt + ' complete!')

def resolveInput(userInput):
  if os.path.isfile(userInput):
    return 'file'
  
  if os.path.isdir(userInput):
    fullDirPath = checkDirPath(userInput)
    return 'directory'
  
def checkDirPath(userInput):
  if os.path.isabs(userInput):
    return userInput
  else:
    cwd = os.getcwd()
    if cwd == '/':
      fullPath = '/' + userInput
    else:
      fullPath =  os.getcwd() + '/' + userInput
  return fullPath
  
def getFaNameExt(inputList):
  faNameExtList = []
  for file in inputList:
    faNameExtList.append(file.split('/')[1])
  return faNameExtList

def inputList(type, userInput):
  toSqueakify = []
  if type == 'file':
    toSqueakify.append(userInput)
  if type == 'directory':
    toSqueakify = glob.glob(userInput + '/*.fa*')
  return toSqueakify

def checkOutputArg(ouputDirectoryPath):
  if not os.path.isdir(ouputDirectoryPath):
    os.mkdir(ouputDirectoryPath)
    print('The provided output path does not lead to an existing directory.')
    print('A dictionary was created at that location.')
    print('--------------------------------')

  return ouputDirectoryPath

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

def camelCase(sequenceId):
  capList = []
  wordList = re.split(r'([^a-zA-Z0-9])', sequenceId)
  for word in wordList:
    capWord = word[:1].upper() + word[1:]
    capList.append(capWord)
  camelCaseSequence = ''.join(capList)
  return camelCaseSequence

def removeSpaces(sequenceId):
  modifiedId = re.sub(r'\s', '', sequenceId)
  return modifiedId

def removeNonAlphanumeric(sequenceId):
  modifiedId = re.sub(r'[^a-zA-Z0-9\s]', '', sequenceId)
  return modifiedId

# Optional?
def remove_non_english_characters(sequenceId):
  # TODO: Remove any non-english characters
  # Regex: /<-[a..zA..Z\s]>+/  <<< Do we need this to include numbers? This is saying anything that isn't an english alphabetic letter
  return

def speciesName(sequenceId, speciesName):
  speciesName = camelCase(speciesName)
  speciesName = removeSpaces(speciesName)
  speciesName = removeNonAlphanumeric(speciesName)
  sequenceIdLower = sequenceId.lower()
  speciesNameLower = speciesName.lower()

  if sequenceIdLower.startswith(speciesNameLower):
    underscoreindex = len(speciesName)
    modifiedId = sequenceId[:underscoreindex] + '_' + sequenceId[underscoreindex:]
  else:
    modifiedId = speciesName + '_' + sequenceId
  return modifiedId
    
def chop(sequenceId, max = 70):
  length = len(sequenceId)

  if length < max:
    return sequenceId
  else:
    sequenceId = re.sub(r'___', '', sequenceId)
    nameComponents = []
    nameComponents = re.findall(r'[A-Z][^A-Z]*', sequenceId)
    middle = len(nameComponents) // 2
    del nameComponents[middle:middle+1]
    nameComponents.insert(middle, '___')
    newName = ''.join(nameComponents)
    return chop(newName, max)
  
def checkForDuplicates(sequenceId, idDict):
  if sequenceId in idDict.values():
    return True
  else:
    return False

def resolveDuplicate(startSequenceId, modSequenceId, dupsList):
  existing = dupsList.count(modSequenceId)
  nextCount = existing + 1 
  startDupId = startSequenceId + '_' + str(nextCount)
  endDupId = modSequenceId + '_' + str(nextCount)
  dupsList.append(modSequenceId)
  return startDupId, endDupId

def writeLine(faFile, line, sequence):
  with open(faFile, 'a') as file:
    if sequence is True:
      file.write('>' + line + '\n')
    else:
      file.write(line)
  file.close()
  
def writeModIdFile(faFileName, idDictInput):
  fileExtension = os.path.splitext(faFileName)
  newFileName = fileExtension[0] + '_squeakMods.tsv'
  
  with open(newFileName, 'w') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    for k, v in idDictInput.items():
      writer.writerow([k, v])
  tsvfile.close()

def setupParser():
    parser = argparse.ArgumentParser()
    # Add parser arguments. ex: parser.add_argument('-l', '--long_name', help='What is it for?', required=True/False)
    parser.add_argument('-i', '--input', help='''Path to fasta file(s) to clean.
                                                  You can provide the path to a single fasta file or a directory containing multiple fasta files.
                                                  Squeakuences will not search subdirectories.
                                                  This can be the full path or relative to the squeakuences.py file location.''', required=True)
    parser.add_argument('-o', '--output', help='''Path to output folder where files generated by Squeakuences will be written.
                                                  This can be the full path or relative to the squeakuences.py file location.
                                                  If this directory path does not exist at runtime, Squeakuences will create it for you.''', required=True)
    # add arg for chop function length
    return parser
  
def parseArguments(parser):
    args = parser.parse_args()
    # Place any messages you may want
    return args

if __name__ == '__main__':
  main()
