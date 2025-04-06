import re

def squeakify(sequenceID, argsFlags, fastaFileName):
  if argsFlags['retain'] is not None:
    retainTag = re.search(r'(locus=\S+)', sequenceID).group()
    sequenceID = sequenceID.replace(retainTag, '')

  checkWhiteSpace(sequenceID)

  endID = camelCase(sequenceID)
  
  endID = removeNonAlphanumeric(endID, argsFlags['ignore'], argsFlags['underscore'])
  
  if argsFlags['addFileName'] is True:
    endID = attachFileName(endID, fastaFileName, argsFlags)

  if argsFlags['chopMethod'] != 'skip':
    endID = checkLength(endID, argsFlags['chopMax'], argsFlags['chopMethod'])

  endID = removeSpaces(endID, argsFlags['underscore'])

  if argsFlags['retain'] is not None:
    info = retainTag.split('=')[1]
    info = '_'+ info
    endID = endID + info

  return endID

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

def removeSpaces(sequenceID, underscores):
  if underscores is False:
    modifiedID = re.sub(r'\s', '', sequenceID)
  if underscores is True:
    modifiedID = re.sub(r'\s', '_', sequenceID)
  return modifiedID

def removeNonAlphanumeric(sequenceID, ignore, underscore):
  if ignore is None:
    customRegex = r'[^A-Za-z0-9\s]'
  else:
    customRegex = r'[^A-Za-z0-9\s](?<![' + ignore + '])'

  if underscore is False:
    modifiedID = re.sub(customRegex, '', sequenceID)
  if underscore is True:
    modifiedID = re.sub(customRegex, '_', sequenceID)
  return modifiedID

def attachFileName(sequenceID, attachFileName, argsFlags):
  attachFileName = camelCase(attachFileName)
  attachFileName = removeSpaces(attachFileName, argsFlags['underscore'])
  attachFileName = removeNonAlphanumeric(attachFileName,argsFlags['ignore'], argsFlags['underscore'])
  sequenceIDLower = sequenceID.lower()
  attachFileNameLower = attachFileName.lower()

  if sequenceIDLower.startswith(attachFileNameLower):
    underscoreindex = len(attachFileName)
    modifiedID = sequenceID[:underscoreindex] + '_' + sequenceID[underscoreindex:]
  else:
    modifiedID = attachFileName + '_' + sequenceID
  return modifiedID

def checkLength(sequenceID, max, method):
  choppedSeqID = ''
  if method == 'words':
    choppedSeqID = chopWords(sequenceID, max)
  if method == 'chars':
    choppedSeqID = chopChars(sequenceID, max)
  return choppedSeqID

def chopWords(sequenceID, max):
  length = len(sequenceID)

  if length < max:
    return sequenceID
  else:
    nameComponents = []
    nameComponents = re.findall(r'[A-Za-z0-9_]+|[\s]', sequenceID)
    middle = len(nameComponents) // 2
    del nameComponents[middle:middle+2]
    nameComponents.insert(middle, '___')
    newName = ''.join(nameComponents)
    return chopWords(newName, max)
  
def chopChars(sequenceID, max):
  length = len(sequenceID)
  difference = length - max
  #sequenceID  = removeSpaces(sequenceID)
  middle = length // 2
  buffer = difference // 2
  spliceIndexLeft = middle - buffer
  spliceIndexRight = middle + buffer
  choppedSeqID = sequenceID[:spliceIndexLeft] + '___' + sequenceID[spliceIndexRight:]
  return choppedSeqID
