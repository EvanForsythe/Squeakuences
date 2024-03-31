#!/usr/bin/env python3
import argparse
import re
import csv

def removeSpaces(seqName):
  modifiedName = seqName.strip()
  modifiedName = modifiedName.replace(' ', '')
  modifiedName = modifiedName.replace('\t', '')
  return modifiedName

def removeNonAlphanumeric(seqName):
  modifiedName = re.sub(r'[\W_]+', '', seqName)
  return modifiedName

def writeModIDFile(idDictInput):
  with open('ids.csv', 'w') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    for k, v in idDictInput.items():
      writer.writerow([k, v])
  tsvfile.close()

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

for line in fasta_handle:
  if line.startswith('>'):
    count += 1
    #print(line)
    line = line.strip('>')
    line = line.strip('\n')
    id = removeSpaces(line)
    id = removeNonAlphanumeric(id)
    
    idDict.update({line: id})

print(idDict)
writeModIDFile(idDict)
print(count)