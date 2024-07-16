#!/usr/bin/env python3
import argparse
import glob
import pandas
import matplotlib.pyplot as plt
#import mpl

def setupParser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', metavar='dir_path', help='', required=True)
  parser.add_argument('-o', '--output', metavar='dir_path', help='', required=True)
  return parser

def main():
  parser = setupParser()
  args = parser.parse_args()
  outputPath = args.output
  
  log_file_path = args.input

  df = pandas.read_csv(log_file_path, sep='\t')
  #print(df)

  timeVsSeq(df, outputPath)
  seqVsTime(df, outputPath)
  startingMbVsTime(df, outputPath)
  timeVsStartingMb(df, outputPath)
  seqVsStartingMb(df, outputPath)
  startingMbVsSeq(df, outputPath)
  

def timeVsSeq(df, outputPath):
  #mpl.rcParams['pdf.fonttype'] = 42
  df = df.sort_values(by=['Processing Time (Seconds)'])
  plt.Figure(figsize=(3,2))
  plt.plot(df['Processing Time (Seconds)'], df['Number of sequences cleaned'])
  plt.title('Runtime in Seconds VS Number of Sequences Cleaned')
  plt.xlabel('Seconds')
  plt.ylabel('Sequences Cleaned')
  plt.savefig(outputPath + '/timeVsSeq.pdf', format = 'pdf', transparent = True) 
  plt.close()

def seqVsTime(df, outputPath):
  #mpl.rcParams['pdf.fonttype'] = 42
  df = df.sort_values(by=['Number of sequences cleaned'])
  plt.Figure(figsize=(3,2))
  plt.plot(df['Number of sequences cleaned'], df['Processing Time (Seconds)'])
  plt.title('Number of Sequences Cleaned VS Runtime in Seconds')
  plt.xlabel('Sequences Cleaned')
  plt.ylabel('Seconds')
  plt.savefig(outputPath + '/SeqVsTime.pdf', format = 'pdf', transparent = True) 
  plt.close()

def startingMbVsTime(df, outputPath):
  #mpl.rcParams['pdf.fonttype'] = 42
  df = df.sort_values(by=['Starting File Size (MB)'])
  plt.Figure(figsize=(3,2))
  plt.plot(df['Starting File Size (MB)'], df['Processing Time (Seconds)'])
  plt.title('Starting File Size VS Runtime in Seconds')
  plt.xlabel('File Size (MB)')
  plt.ylabel('Seconds')
  plt.savefig(outputPath + '/StartingMbVsTime.pdf', format = 'pdf', transparent = True) 
  plt.close()

def timeVsStartingMb(df, outputPath):
  #mpl.rcParams['pdf.fonttype'] = 42
  df = df.sort_values(by=['Processing Time (Seconds)'])
  plt.Figure(figsize=(3,2))
  plt.plot(df['Processing Time (Seconds)'], df['Starting File Size (MB)'])
  plt.title('Runtime in Seconds VS Starting File Size')
  plt.ylabel('File Size (MB)')
  plt.xlabel('Seconds')
  plt.savefig(outputPath + '/TimeVsStartingMb.pdf', format = 'pdf', transparent = True) 
  plt.close()

def seqVsStartingMb(df, outputPath):
  #mpl.rcParams['pdf.fonttype'] = 42
  df = df.sort_values(by=['Number of sequences cleaned'])
  plt.Figure(figsize=(3,2))
  plt.plot(df['Number of sequences cleaned'], df['Starting File Size (MB)'])
  plt.title('Number of Sequences Cleaned VS Starting File Size')
  plt.xlabel('Sequences Cleaned')
  plt.ylabel('File Size (MB)')
  plt.savefig(outputPath + '/SeqVsStaringMb.pdf', format = 'pdf', transparent = True) 
  plt.close()

def startingMbVsSeq(df, outputPath):
  #mpl.rcParams['pdf.fonttype'] = 42
  df = df.sort_values(by=['Starting File Size (MB)'])
  plt.Figure(figsize=(3,2))
  plt.plot(df['Starting File Size (MB)'], df['Number of sequences cleaned'])
  plt.title('Starting File Size VS Number of Sequences Cleaned')
  plt.ylabel('Sequences Cleaned')
  plt.xlabel('File Size (MB)')
  plt.savefig(outputPath + '/StartingMbVsSeq.pdf', format = 'pdf', transparent = True) 
  plt.close()

if __name__ == '__main__':
  main()
  