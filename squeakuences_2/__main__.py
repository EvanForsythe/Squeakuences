import cli

#Parse user input from the command line
args = cli.runParser()
#Generate dictionary of flags parsed in cli.py
argsDict = vars(args)

print('Commencing Squeakuences Cleanup')
print('================================')
cli.messagesForArgs(argsDict)
print('--------------------------------')

