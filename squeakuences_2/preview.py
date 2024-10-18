import file_system
import squeakify

def generatePreview(argsDict):
  print('Preview mode activated!')

  messyFastaHandle = file_system.loadMessyFile(argsDict['input'])

  for linecount in range(30):
    line = next(messyFastaHandle).strip()
    if line.startswith('>'):
      sequenceID = squeakify.stripSequenceID(line)

      cleanSequenceId = squeakify.squeakify(sequenceID, argsDict)

      print(cleanSequenceId)
    linecount += 1