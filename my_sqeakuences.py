#My own version of squeakuences

import glob
import sys
import re
import math
import os

in_path = "/shared/forsythe/ERC_datasets/Bird_data/Fasta_files/raw_bird_fastas/"
extension = ".faa"

files=glob.glob(in_path + "*" + extension)

if not os.path.exists("MY_SQUEAK_OUT/"):
    os.makedirs("MY_SQUEAK_OUT/")

if not os.path.exists("MY_SQUEAK_NOTES/"):
    os.makedirs("MY_SQUEAK_NOTES/")

out_files = []

for file in files:
    out_temp=file.replace(in_path, "MY_SQUEAK_OUT/")
    out_files.append(out_temp)

file_counter = 0

for seq_file_path in files:
    #Create a file handle
    seq_handle = open(seq_file_path, "r")
    notes_handle = open(out_files[file_counter].replace("_OUT", "_NOTES").replace(extension, ".tsv"), "a")
    notes_handle.write("Raw_ID" + "\t" + "Squeakuences_version" + "\n")

    #Create an empty dictionary
    seq_dict = {}
    #Loop through the line in the file
    for line in seq_handle:
        if line.startswith(">"):
            
            id_temp = line.strip() #Removes "\n"
            id_clean = id_temp.replace(">", "") #Removes ">" by replacing it with nothing.

            #Seperate the species ID  from the rest of the ID.
            split_ID = id_clean.split("_")
            sp_ID = str(split_ID[0])
            remaining_ID = "".join(split_ID[1:])

            #Remove non alphanumeric from remaining ID
            cleaned_reaminer = re.sub(r'[^A-Za-z0-9]+', '', remaining_ID)
            
            #Get the length of the remaining ID
            ID_len=len(cleaned_reaminer)

            #If it's too long, clean it up.
            if ID_len >= 60:
                n_over= ID_len - 60

                shortened = cleaned_reaminer[:math.ceil(ID_len/2)-math.ceil(n_over/2)] + cleaned_reaminer[math.ceil(ID_len/2)+math.ceil(n_over/2):]

                full_shortened = sp_ID + "_" + shortened
            else:
                full_shortened = sp_ID + "_" + cleaned_reaminer

            if full_shortened not in seq_dict.keys():
                #Add the item to the dictionary
                seq_dict[full_shortened] = "" 
            else:
                while full_shortened in seq_dict.keys():
                    full_shortened += "_dup"
                seq_dict[full_shortened] = ""
            
            #Add to notes doc
            notes_handle.write(id_clean + "\t" + full_shortened + "\n")

        else:
            seq_line = line.strip() #Removes "\n"
            #append this line to the dictionary value, using the key (which is still "id_clean" from the previous line)
            seq_dict[full_shortened] += seq_line
    
    notes_handle.close()
    out_seq_handle = open(out_files[file_counter], "a")

    for key in seq_dict.keys():
        out_seq_handle.write(">"+key+"\n")
        out_seq_handle.write(seq_dict[key]+"\n")
    
    out_seq_handle.close()

    print(f"done processing {seq_file_path}")

    file_counter+=1






