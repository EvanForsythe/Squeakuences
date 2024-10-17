import log
import file_system

def generate(file, argsDict):
  if argsDict['log'] is True:
    logData = {}
    log.startLog(logData, file)  

  sequenceIdCount = 0
  idDict = {}
  idDuplicatesList = []

  cleanedFaLines = []

  messyFastaHandle = file_system.loadMessyFile(file)
  print('Now processing ' + file_system.fileNameWithExt(file))


  currentFaFileName = file_system.fileNameOnly(file)
  squeakyPath = argsDict['output'] + '/' + currentFaFileName + '_squeak.fa'
  squeakyDictPath = argsDict['output'] + '/' + currentFaFileName + '_modSeqs.tsv'

  file_system.removeExistingSqueakyFiles(squeakyDictPath, squeakyPath)
