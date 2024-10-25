import glob
import os
import log
import sys
import csv

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
  print('The following file(s) will be cleaned: ' + str(faNameExtList))
  print('--------------------------------')
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

def checkExistingLogFile(logPath):
  if os.path.exists(logPath):
    print('Existing log file detected.')
    print('Processing information from fasta files cleaned in this run will be appended to this file.')
    print('--------------------------------')

  if not os.path.exists(logPath):
    createLogFile(logPath)
    print('An existing log file was not detected.')
    print('A new log file was created at: ' + os.path.abspath(logPath))
    print('--------------------------------')
  return logPath

def loadMessyFile(file):
  try: 
    messyFastaHandle = open(file, 'r')
  except:
    print('Squeakuences was unable to open ' + str(file) +'.')
    print('')
  else:
    return messyFastaHandle
  
def fileNameWithExt(file):
  return os.path.basename(file)

def fileNameOnly(file):
  faFileNameExt = fileNameWithExt(file)
  return os.path.splitext(faFileNameExt)[0]

def removeExistingSqueakyFiles(squeakyDictPath, squeakyPath):
  if os.path.exists(squeakyDictPath):
    os.remove(squeakyDictPath)
    print('Existing squeaky dictionary file deleted.')

  if os.path.exists(squeakyPath):
    os.remove(squeakyPath)
    print('Existing squeaky fa file deleted.')

def checkEmptySqueakifyList(squeakifyList, ext):
  if squeakifyList == []:
    print('--------------------------------')
    print('Squeakuences did not find any files with the ' + str(ext) + ' extension at the input directory location.')
    print('Please check your command and try again.')
    print('Exiting Squeakuences run now.')
    sys.exit()

def writeNewFaFile(newFilePath, cleanedLinesList):
  f = open(newFilePath, 'w')
  f.writelines(cleanedLinesList)
  f.close()
  
def writeModIdFile(faFileName, idDictInput):
  fileExtension = os.path.splitext(faFileName)
  newFileName = fileExtension[0] + '_modSeqs.tsv'
  
  with open(newFileName, 'w') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    for k, v in idDictInput.items():
      writer.writerow([k, v])
  tsvfile.close()

def createLogFile(logPath):
  with open(logPath, 'a') as file:
    file.write('File Name\tProcessing Time (Hours: Minutes: Seconds)\tMemory (peak size of memory blocks traced in MB)\tStarting File Size (MB)\tEnding File Size (MB)\tNumber of sequences cleaned\n')
  file.close()

def writeLogFile(logDataDict, logPath, processedIdCount):
  with open(logPath, 'a') as file:
    file.write(logDataDict['file_name'] + '\t' + logDataDict['duration'] + '\t' + 
               str(logDataDict['memory']) + '\t' + str(logDataDict['start_file_size']) + '\t' + str(logDataDict['end_file_size']) + '\t' + str(processedIdCount) + '\n')
  file.close()
  