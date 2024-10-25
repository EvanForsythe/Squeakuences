import file_system
import squeakify

def printMessage(argsDict):
  print('Preview mode activated!')
  print('--------------------------------')
  print('Squeakuences will clean sequence ids will the following settings:\n')
  print('Chop method (-c): ' + argsDict['chopMethod'])
  print('Maximum sequence id character length (-m): ' + str(argsDict['chopMax']))
  print('Prepend file name (-f): ' + str(argsDict['addFileName']))
  print('Underscores (-u): ' + str(argsDict['underscore']))
  print('Ignore characters (-x): ' + str(argsDict['ignore']))
  print('--------------------------------')

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
