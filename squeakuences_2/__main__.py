import sys
import cli

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
  sys.exit()
  
print('You\'ve input a ' + inputType + '.')


