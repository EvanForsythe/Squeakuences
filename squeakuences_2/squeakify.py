def squeakify(sequence):
  sequence = stripSequenceId(sequence)
  endId = camelCase(startId)
  endId = removeSpaces(endId)
  endId = removeNonAlphanumeric(endId)
  if fileNameFlag is True:
    endId = attachFileName(endId, faFileName)
  endId = chop(endId)

def stripSequenceId(line):
  line = line.strip('>')
  line = line.strip('\n')
  return line