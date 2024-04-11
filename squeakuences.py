#!/usr/bin/env python3
import argparse

def main():
  parser = setup_parser()
  args = parse_arguments(parser)
  
  print("implement")

def hello_world():
  return "Hello world!"

def load_file(file):
  # TODO: Load in  the file that requires preprocessing
  return

def is_squence_id(line):
  # TODO: Check if the line is a squence ID
  return

#######################################
# Non Alpha-Numeric Removal Functions #
#######################################

def remove_brackets(sequence_id):
  # TODO: Remove any brackets from the sequence ID
  # Multiple regexes: /\(.*\)/, /\[.*\]/, /\{.*\}/, /\-.*/
  return

def remove_punctuation(sequence_id):
  # TODO: Remove any punctuation from the sequence ID.
  # Be aware of the first >. How are we going to approach this?
  # regex: /<[\`\=\+\:\_\.\\\"\?\¿\!\¡\.\;\:\&\$\*\@\%\#]>/
  return

# Optional?
def remove_non_english_characters(sequence_id):
  # TODO: Remove any non-english characters
  # Regex: /<-[a..zA..Z\s]>+/  <<< Do we need this to include numbers? This is saying anything that isn't an english alphabetic letter
  return

# Create tests for these???
def setup_parser():
    parser = argparse.ArgumentParser()
    # Add parser arguments. ex: parser.add_argument('-l', '--long_name', help='What is it for?', required=True/False)
    return parser
  
def parse_arguments(parser):
    args = parser.parse_args()
    # Place any messages you may want
    return args
