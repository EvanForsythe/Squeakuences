import sys
import cli
import file_system

#Parse user input from the command line
args = cli.runParser()
#Generate dictionary of flags parsed in cli.py
argsDict = vars(args)

print('Commencing Squeakuences Cleanup')
print('================================')
cli.messagesForArgs(argsDict)
print('--------------------------------')

inputType = cli.resolveInputType(argsDict['input'])

if inputType == 'non-path':
  print('You\'ve passed a non-path string into the input flag. Please review your input and try again.')
  print('Exiting Squeakuences run now.')
  sys.exit()
  
print('You\'ve input a ' + inputType + '.')

squeakifyList = file_system.compileSqueakifyList(inputType, argsDict)

if squeakifyList == []:
  print('--------------------------------')
  print('Squeakuences did not find any files with the ' + str(argsDict['fileExt']) + ' extension at the input directory location.')
  print('Please check your command and try again.')
  print('Exiting Squeakuences run now.')
  sys.exit()

fileNameList = file_system.getFileNames(squeakifyList)
print('The following file(s) will be cleaned: ' + str(fileNameList))
print('--------------------------------')
