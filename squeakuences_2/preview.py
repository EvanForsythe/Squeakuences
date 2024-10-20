import file_system
import squeakify

def generatePreview(argsDict):
  print('Preview mode activated!')
  print('--------------------------------')
  print('Squeakuences will clean sequence ids will the following settings:\n')
  print('Chop method (-c): ' + argsDict['chopMethod'])
  print('Maximum sequence id character length (-m): ' + str(argsDict['chopMax']))
  print('Prepend file name (-f): ' + str(argsDict['addFileName']))
  print('--------------------------------')

  messyFastaHandle = file_system.loadMessyFile(argsDict['input'])

  for linecount in range(30):
    line = next(messyFastaHandle).strip()
    if line.startswith('>'):
      sequenceID = squeakify.stripSequenceID(line)

      cleanSequenceId = squeakify.squeakify(sequenceID, argsDict)

      print(cleanSequenceId)
    linecount += 1