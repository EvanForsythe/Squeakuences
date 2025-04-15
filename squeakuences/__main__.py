import cli
import file_system
import squeaky_file
import preview
import squeakify

print('================================')
print('Commencing Squeakuences Cleanup')
print('================================')

#Parse user input from the command line
args = cli.runParser()
#Generate dictionary of flags parsed in cli.py
argsDict = vars(args)

#Check if -s flag is activated
if argsDict['stepbystep'] != False:
  print('Step by step print mode activated.')
  print('A step by step cleaning of the provided sequence will be output.')
  print()
  print('-i, -o, and -p flags will be ignored. If the -f flag is activated, an stand in file name will be prepended.')
  print('--------------------------------')
  #Set default values
  cli.setDefaults(argsDict)
  print('Squeakuences will clean sequence id will the following settings:\n')
  cli.printArgumentState(argsDict)
  cleaned_seq = squeakify.squeakify(argsDict['stepbystep'], argsDict, 'myFile')
  print('--------------------------------')
  print('Ta-da! Squeaky clean sequence id!')

else:
  #Print message confirming user arguments to command line
  cli.messagesForArgs(argsDict)
  print('--------------------------------')
  #Set default values
  cli.setDefaults(argsDict)
  print('Squeakuences will clean sequence ids will the following settings:\n')
  cli.printArgumentState(argsDict)

  #Determine if input is a valid path like string that leads to a file or directory
  #Exits if input is not a valid path
  inputType = cli.resolveInputType(argsDict['input'])
    
  #Collect file(s) to be cleaned  
  squeakifyList = file_system.compileSqueakifyList(inputType, argsDict)
  #Check if list is empty and exit if empty
  file_system.checkEmptySqueakifyList(squeakifyList, argsDict['fileExt'])
  #Get names of fasta files to be cleaned and print to command line
  fileNameList = file_system.getFileNames(squeakifyList)

  if argsDict['preview'] is True:
    for file in squeakifyList:
      preview.generatePreview(file, argsDict)
      print('--------------------------------')

    print('Preview(s) sucessfully generated!')

  else:
    #Verify path to user defined ouput directory exists and create directory if not found
    verifiedOuputPath = file_system.checkExistingOutputPath(argsDict['output'])

    #Create log file if flag is true and no existing log file exists at path location. 
    #Otherwise, create log file at logPath location
    if argsDict['log'] is True:
      logPath = file_system.checkExistingLogFile(verifiedOuputPath + '/log.tsv')
      argsDict.update({'logPath': logPath}) 

    #Clean each fasta file collected and generate a squeaky clean version
    for file in squeakifyList:
      squeaky_file.generate(file, argsDict)
      print('--------------------------------')

    print('Ta-da! Squeaky clean sequence ids!')
    #print('New squeaky clean files and other output files can be found in: ' + outputPath)
