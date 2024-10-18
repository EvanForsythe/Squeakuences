import re

def squeakify(sequenceID, argsFlags):
  sequenceID = stripSequenceID(sequenceID)

  checkWhiteSpace(sequenceID)

  endID = camelCase(sequenceID)
  
  endID = removeNonAlphanumeric(endID)
  
  if argsFlags['fileNameFlag'] is True:
    endID = attachFileName(endID, argsFlags['faFileName'])
    
  endID = chopWords(endID, argsFlags['chopMax'])

  endID = removeSpaces(endID)

def stripSequenceID(line):
  line = line.strip('>')
  line = line.strip('\n')
  return line

def camelCase(sequenceID):
  capList = []
  wordList = re.split(r'([^a-zA-Z0-9])', sequenceID)
  for word in wordList:
    capWord = word[:1].upper() + word[1:]
    capList.append(capWord)
  camelCaseSequence = ''.join(capList)
  return camelCaseSequence

def checkWhiteSpace(sequenceID):
  number = re.findall(r'\s', sequenceID)
  return len(number)

def removeSpaces(sequenceID):
  modifiedID = re.sub(r'\s', '', sequenceID)
  return modifiedID

def removeNonAlphanumeric(sequenceID):
  modifiedID = re.sub(r'[^a-zA-Z0-9\s]', '', sequenceID)
  return modifiedID

def attachFileName(sequenceID, attachFileName):
  attachFileName = camelCase(attachFileName)
  attachFileName = removeSpaces(attachFileName)
  attachFileName = removeNonAlphanumeric(attachFileName)
  sequenceIDLower = sequenceID.lower()
  attachFileNameLower = attachFileName.lower()

  if sequenceIDLower.startswith(attachFileNameLower):
    underscoreindex = len(attachFileName)
    modifiedID = sequenceID[:underscoreindex] + '_' + sequenceID[underscoreindex:]
  else:
    modifiedID = attachFileName + '_' + sequenceID
  return modifiedID
    
def chopWords(sequenceID, max = 70):
  length = len(sequenceID)
  print("Start Chop: " + sequenceID)

  if length < max:
    return sequenceID
  else:
    #sequenceID = re.sub(r'___', 'temp', sequenceID)
    nameComponents = []
    nameComponents = re.findall(r'[A-Za-z0-9_]+|[\s]', sequenceID)
    print("ID components:")
    print(nameComponents)
    middle = len(nameComponents) // 2
    del nameComponents[middle:middle+2]
    nameComponents.insert(middle, '___')
    newName = ''.join(nameComponents)
    print("End Chop:")
    print(newName)
    print()
    return chopWords(newName, max)
  
def chopChars(sequenceID, max = 70):
  length = len(sequenceID)
  difference = length - max
  print("Start Chop: " + sequenceID)
  sequenceID  = removeSpaces(sequenceID)
  middle = length // 2
  buffer = difference // 2
  spliceIndexLeft = middle - buffer
  spliceIndexRight = middle + buffer
  choppedSeqID = sequenceID[:spliceIndexLeft] + '___' + sequenceID[spliceIndexRight:]
  print("End Chop:")
  print(choppedSeqID)
  print()
  return choppedSeqID