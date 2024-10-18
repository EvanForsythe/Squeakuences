import file_system
import squeakify

def generatePreview(argsDict):
  print('Preview mode activated!')
  sequenceIdCount = 0

  messyFastaHandle = file_system.loadMessyFile(argsDict['input'])

  for line in messyFastaHandle:
    if line.startswith('>'):
      sequenceIdCount += 1
      sequenceID = squeakify.stripSequenceID(line)

      cleanSequenceId = squeakify.squeakify(sequenceID, argsDict)

      print(cleanSequenceId)