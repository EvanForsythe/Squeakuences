#!/usr/bin/env python3
import argparse

#Set up an argumanet parser
parser = argparse.ArgumentParser(description='Quick and Dirty Squeakuences Model')

parser.add_argument('-f', '--file', type=str, metavar='', required=True, help='Full path to fasta file to clean') 

#Define the parser
args = parser.parse_args()

#Store arguments
fasta=args.file

fasta_handle = open(fasta, 'r')

count = 0

for line in fasta_handle:
  if line.startswith('>'):
    count += 1
    print(line)

print(count)