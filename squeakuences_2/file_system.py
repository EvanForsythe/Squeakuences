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

def checkExistingOutputPath(ouputDirectoryPath):
  if not os.path.isdir(ouputDirectoryPath):
    os.mkdir(ouputDirectoryPath)
    print('The provided output path does not lead to an existing directory.')
    print('A directory was created at: ' + os.path.abspath(ouputDirectoryPath))
    print('Squeakuences files will be written in this new directory.')
    print('--------------------------------')
  else:
    print('Output directory found!')
    print('Squeakuences files will be written in the provided directory.')
    print('--------------------------------')
  return ouputDirectoryPath
