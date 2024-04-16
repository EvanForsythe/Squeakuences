#!/usr/bin/env python3
import argparse
import re
import csv
import os
import glob

def removeSpaces(seqName):
  modifiedName = seqName.strip()
  modifiedName = modifiedName.replace(' ', '')
  modifiedName = modifiedName.replace('\t', '')
  return modifiedName

def removeNonAlphanumeric(seqName):
  modifiedName = re.sub(r'[\W_]+', '', seqName)
  return modifiedName

def chop(seqName, max = 70):
  length = len(seqName)

  if length < max:
    return seqName

  else:
    nameComponents = []
    nameComponents = re.findall(r'[A-Z][^A-Z]*', seqName)
    middle = len(nameComponents) // 2
    del nameComponents[middle:middle+1]
    nameComponents.insert(middle, '___')
    newName = ''.join(nameComponents)
    return chop(newName)

def writeModIDFile(faFileName, idDictInput):
  fileExtension = os.path.splitext(faFileName)
  newFileName = fileExtension[0] + '_squeakMods.tsv'
  
  with open(newFileName, 'w') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    for k, v in idDictInput.items():
      writer.writerow([k, v])
  tsvfile.close()

def writeSqueakyID(faFile, id):
  with open(faFile, 'a') as file:
    file.write('>' + id + '\n')
  file.close()

def resolveDuplicate(id, dupsList):
  existing = dupsList.count(id)
  #print("existing count " + str(existing))
  nextCount = existing + 1 
  incID = id + '_' + str(nextCount)
  dupsList.append(id)
  #print(incID)
  return incID

def squeakify(file, write):
  totalCount = 0
  dupsCount = 0

  faFile = os.path.basename(file)
  fasta_handle = open(file, 'r')
 
  idDuplicates = []
  idDict = {}
  
  
  faFileName = os.path.splitext(faFile)[0]
  squeakyFileName = write + '/' + faFileName + '_squeak.fa'
  squeakyDictFile = write + '/' + faFileName + '_squeakMods.tsv'

  if os.path.exists(squeakyDictFile):
    os.remove(squeakyDictFile)
    print('Existing squeaky dictionary file deleted.')

  if os.path.exists(squeakyFileName):
    os.remove(squeakyFileName)
    print('Existing squeaky fa file deleted.')

  print('...')

  for line in fasta_handle:
    if line.startswith('>'):
      totalCount += 1
      line = line.strip('>')
      line = line.strip('\n')
      camelCaseName = line.title()
      id = removeSpaces(camelCaseName)
      id = removeNonAlphanumeric(id)

      if id.startswith(faFileName):
        underscoreindex = len(faFileName)
        id = id[:underscoreindex] + '_' + id[underscoreindex:]
      else:
        id = faFileName + '_' + id

      if len(id) > 65:
        id = chop(id)

      if id in idDict.values():
        #print("Duplicate found: " + id)
        id = resolveDuplicate(id, idDuplicates)
        dupsCount += 1
        if len(id) > 65:
          id = chop(id)

      idDict.update({line: id})

      writeSqueakyID(squeakyFileName, id)
    
    else:
      with open(squeakyFileName, 'a') as file:
        file.write(line)
      file.close()

  writeModIDFile(write + '/' + faFile, idDict)

  #print(str(dupsCount) + ' duplicates found')
  #print(idDuplicates)
  print(str(totalCount) + ' ids processed') 

#Set up an argumanet parser
parser = argparse.ArgumentParser(description='Quick and Dirty Squeakuences Model')

parser.add_argument('-i', '--input', type=str, required=True, help='Full path to fasta file(s) to clean') 
parser.add_argument('-o', '--output', type=str, required=True, help='Full path to write location of squeaky clean files') 

#Define the parser
args = parser.parse_args()

#Store arguments
userPath = args.input
writePath = args.output

if os.path.isfile(userPath):
  fileName = os.path.basename(userPath)
  print("You've input a file")
  print('----------')
  print("Now processing " + fileName)
  squeakify(userPath, writePath)
  print(fileName + ' Complete')
  print('----------')
  print('Ta-da! Squeaky clean sequence ids!')
  print('File processed: ' + fileName)
  print('New squeaky clean files can be found in: ' + writePath)

elif os.path.isdir(userPath):
  print("You've input a directory")
  filesList = glob.glob(userPath + '/*.fa*')
  print("File retrieval successful!")
  print('----------')

  for file in filesList:
    fileName = os.path.basename(file)
    print('Now processing ' + fileName)
    squeakify(file, writePath)
    print(fileName + ' Complete')
    print('----------')
  
  print('Ta-da! Squeaky clean sequence ids!')
  print('Files processed: ' + str(filesList))
  print('New squeaky clean files can be found in: ' + writePath)
