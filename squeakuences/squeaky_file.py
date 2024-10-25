import log
import file_system
import squeakify
import os

def generate(file, argsDict):
  if argsDict['log'] is True:
    logData = {}
    log.startLog(logData, file)  

  sequenceIdCount = 0
  idDict = {}
  idDuplicatesList = []
  cleanedFaLines = []

  messyFastaHandle = file_system.loadMessyFile(file)
  fileNameExt = file_system.fileNameWithExt(file)
  print('Now processing ' + fileNameExt)

  currentFaFileName = file_system.fileNameOnly(file)
  squeakyPath = argsDict['output'] + '/' + currentFaFileName + '_squeak.fa'
  squeakyDictPath = argsDict['output'] + '/' + currentFaFileName + '_modSeqs.tsv'

  file_system.removeExistingSqueakyFiles(squeakyDictPath, squeakyPath)

  print('...')

  for line in messyFastaHandle:
    if line.startswith('>'):
      sequenceIdCount += 1
      sequenceID = squeakify.stripSequenceID(line)

      cleanSequenceId = squeakify.squeakify(sequenceID, argsDict)

      if checkForDuplicates(cleanSequenceId, idDict):
        sequenceID, cleanSequenceId = resolveDuplicate(sequenceID, cleanSequenceId, idDuplicatesList)
        cleanSequenceId = squeakify.checkLength(cleanSequenceId, argsDict['chopMax'], argsDict['chopMethod'])

      idDict.update({sequenceID: cleanSequenceId})

      storeLine(cleanedFaLines, cleanSequenceId, True)
    else:
      storeLine(cleanedFaLines, line, False)
  
  file_system.writeNewFaFile(squeakyPath, cleanedFaLines)

  file_system.writeModIdFile(argsDict['output'] + '/' + currentFaFileName, idDict)

  if argsDict['log'] is True:
    log.endLog(logData, fileNameExt, os.path.abspath(squeakyPath))
    file_system.writeLogFile(logData, argsDict['logPath'], sequenceIdCount)

  print(fileNameExt + ' complete!')

def isSequenceId(line):
  return line.startswith('>')

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

def storeLine(outFaFileLines, line, sequence):
    if sequence is True:
      outFaFileLines.append('>' + line + '\n')
    else:
      outFaFileLines.append(line)
      