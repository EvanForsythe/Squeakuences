import re

def squeakify(sequenceID, argsFlags, fastaFileName):
  if argsFlags['retain'] is not None:
    regex = re.compile('(' + argsFlags['retain'] + r'\S+)')
    retainTag = re.search(regex, sequenceID).group()
    sequenceID = sequenceID.replace(retainTag, '')

  checkWhiteSpace(sequenceID)

  stepPrint(sequenceID, 'Starting string:', argsFlags['stepbystep'])

  endID = camelCase(sequenceID)

  stepPrint(endID, 'Camel case:', argsFlags['stepbystep'])

  endID = removeNonAlphanumeric(endID, argsFlags['ignore'], argsFlags['underscore'])

  stepPrint(endID, 'Remove non-alphanumeric:', argsFlags['stepbystep'])

  if argsFlags['addFileName'] is True:
    endID = attachFileName(endID, fastaFileName, argsFlags)
    stepPrint(endID, 'Prepend file name:', argsFlags['stepbystep'])

  if argsFlags['chopMethod'] != 'skip':
    endID = checkLength(endID, argsFlags)
    stepPrint(endID, 'Chop:', argsFlags['stepbystep'])

  endID = removeSpaces(endID, argsFlags['underscore'])
  stepPrint(endID, 'Remove spaces:', argsFlags['stepbystep'])

  if argsFlags['retain'] is not None:
    info = retainTag.split('=')[1]
    info = '_'+ info
    endID = endID + info
    stepPrint(endID, 'Retain characters:', argsFlags['stepbystep'])

  stepPrint(endID, 'Final cleaned sequence:', argsFlags['stepbystep'])

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

def checkLength(sequenceID, argsDict):
  choppedSeqID = ''
  if argsDict['chopMethod'] == 'words':
    choppedSeqID = chopWords(sequenceID, argsDict)
  if argsDict['chopMethod'] == 'chars':
    choppedSeqID = chopChars(sequenceID, argsDict)
  return choppedSeqID

def chopWords(sequenceID, argsDict):
  length = len(sequenceID)
  maxLength = argsDict['chopMax']

  if length < maxLength:
    return sequenceID
  else:
    nameComponents = []
    nameComponents = re.findall(r'[A-Za-z0-9_]+|[^\w\s]+|\s', sequenceID)
    middle = len(nameComponents) // 2
    del nameComponents[middle:middle+2]
    nameComponents.insert(middle, '___')
    newName = ''.join(nameComponents)
    #stepPrint(newName, 'Inside chop', argsDict['stepbystep'])
    return chopWords(newName, argsDict)
  
def chopChars(sequenceID, argsDict):
  length = len(sequenceID)
  difference = length - argsDict['chopMax']
  #sequenceID  = removeSpaces(sequenceID)
  middle = length // 2
  buffer = difference // 2
  spliceIndexLeft = middle - buffer
  spliceIndexRight = middle + buffer
  choppedSeqID = sequenceID[:spliceIndexLeft] + '___' + sequenceID[spliceIndexRight:]
  return choppedSeqID

def stepPrint(sequence, stepName, stepFlag):
  if stepFlag != False:
    print(stepName)
    print(sequence)
    if stepName != 'Final cleaned sequence:':
      print('\n')
