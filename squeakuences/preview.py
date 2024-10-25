import cli
import file_system
import squeakify

def generatePreview(file, argsDict):
  print('Now generating preview of cleaned sequence ids from: ' + file_system.fileNameWithExt(file))
  print()

  messyFastaHandle = file_system.loadMessyFile(file)

  for linecount in range(30):
    line = next(messyFastaHandle).strip()
    if line.startswith('>'):
      sequenceID = squeakify.stripSequenceID(line)

      cleanSequenceId = squeakify.squeakify(sequenceID, argsDict)

      print(cleanSequenceId)
    linecount += 1
