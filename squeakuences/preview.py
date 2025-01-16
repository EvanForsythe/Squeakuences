import cli
import file_system
import squeakify

def generatePreview(file, argsDict):
  fileNameWithExt = file_system.fileNameWithExt(file)
  print('Now generating preview of cleaned sequence ids from: ' + fileNameWithExt)
  print()

  messyFastaHandle = file_system.loadMessyFile(file)

  for linecount in range(30):
    line = next(messyFastaHandle).strip()
    if line.startswith('>'):
      sequenceID = squeakify.stripSequenceID(line)

      cleanSequenceId = squeakify.squeakify(sequenceID, argsDict, fileNameWithExt)

      print(cleanSequenceId)
    linecount += 1
