import cli
import file_system
import squeakify

def generatePreview(file, argsDict):
  previewCounter = 0
  fileNameWithExt = file_system.fileNameWithExt(file)
  fileNameOnly = file_system.fileNameOnly(file)
  print('Now generating preview of cleaned sequence ids from: ' + fileNameWithExt)
  print()

  messyFastaHandle = file_system.loadMessyFile(file)

  while previewCounter < 15:
    try: 
      line = next(messyFastaHandle)
    
    except:
      break

    else:
      line.strip()
      if line.startswith('>'):
        previewCounter += 1
        sequenceID = squeakify.stripSequenceID(line)

        cleanSequenceId = squeakify.squeakify(sequenceID, argsDict, fileNameOnly)

        print(cleanSequenceId)
