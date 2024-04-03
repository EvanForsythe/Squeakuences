#!/usr/bin/env python3
import argparse
import re
import csv
import os

def removeSpaces(seqName):
  modifiedName = seqName.strip()
  modifiedName = modifiedName.replace(' ', '')
  modifiedName = modifiedName.replace('\t', '')
  return modifiedName

def removeNonAlphanumeric(seqName):
  modifiedName = re.sub(r'[\W_]+', '', seqName)
  return modifiedName

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

#Set up an argumanet parser
parser = argparse.ArgumentParser(description='Quick and Dirty Squeakuences Model')

parser.add_argument('-f', '--file', type=str, metavar='', required=True, help='Full path to fasta file to clean') 

#Define the parser
args = parser.parse_args()

#Store arguments
fasta=args.file

fasta_handle = open(fasta, 'r')

count = 0
idDict = {}

faFile = os.path.basename(fasta)
faFileName = os.path.splitext(faFile)
squeakyFileName = faFileName[0] + '_squeak.fa'

if os.path.exists(squeakyFileName):
  os.remove(squeakyFileName)
  print('Previous squeaky fa file deleted.')

for line in fasta_handle:
  if line.startswith('>'):
    count += 1
    #print(line)
    line = line.strip('>')
    line = line.strip('\n')
    camelCaseName = line.title()
    id = removeSpaces(camelCaseName)
    id = removeNonAlphanumeric(id)
    
    idDict.update({line: id})

    writeSqueakyID(squeakyFileName, id)
  
  else:
    with open(squeakyFileName, 'a') as file:
      file.write(line)
    file.close()

writeModIDFile(faFile, idDict)
print('Ta-da! Squeaky clean sequence ids!')
print('File(s) processed: ' + faFile)