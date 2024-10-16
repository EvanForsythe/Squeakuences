import glob
import os

def compileSqueakifyList(type, argsDict):
  toSqueakify = []
  if type == 'file':
    toSqueakify.append(argsDict['input'])
    if argsDict['fileExt'] != ['.fa*']:
      print('-e flag is not supported with file input. Squeakuences will proceed and ignore user input in -e flag.')
  if type == 'directory':
    for inputExt in argsDict['fileExt']:
      toSqueakify += glob.glob(argsDict['input'] + '/*' + inputExt)
  for file in toSqueakify:
    index = toSqueakify.index(file)
    toSqueakify[index] = os.path.abspath(file)
  toSqueakify.sort()
  return toSqueakify

def getFileNames(inputList):
  faNameExtList = []
  for filePath in inputList:
    faNameExtList.append(filePath.split('/')[-1])
  return faNameExtList