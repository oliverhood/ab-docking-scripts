#!/usr/bin/env python3
"""
Program: evaluate_2000_decoys
File:    evaluate_2000_decoys.py

Version:  V1.0
Date:     26.06.23
Function:   Run evaluate_interface on full list of 2000 Megadock outputs
Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
Take a directory name as input, find the OG structure in one of 4 directories and run evaluate_interface using the OG and each output file

--------------------------------------------------------------------------

Usage:
======


--------------------------------------------------------------------------

Revision History:
=================
V1.0   29.07.23   Original   By: OECH

"""

#*************************************************************************

# Import libraries
import sys, os, subprocess, json

#*************************************************************************

filename = sys.argv[1]

#*************************************************************************

# Get input name (not sure if sys arg takes full path or just dir name)
filename_stripped = filename.split('/')[1].split('-')[1] # 2nd split to get rid of decoy_complexes text

# get filename semi-stripped
filename_semi_stripped = filename.split('/')[1]

# Get PWD
pwd = os.getcwd()

# Define target directory
target_dir = f"{pwd}/{filename_semi_stripped}"

# Find OG file
OG_file = f"/home/oliverh/data/test_files/pdb{filename_stripped}.pdb"

#*************************************************************************

# Define dict of metrics
evaluation_outputs = {}

# List to add dict to
evaluation_output = []

# Add filename
evaluation_outputs['PDB ID'] = filename_stripped

#*************************************************************************

# Evaluation function
def evaluate_decoy(decoyfile, OG_file):
    output = subprocess.run([f"~/ab-docking-scripts/evaluate_interface.py {OG_file} {decoyfile}"], capture_output=True,shell=True)
    return(output)

#*************************************************************************

# iterate through each decoy

#for decoy in range(2001):
#    decoy_number = f"decoy.{decoy}" # Get decoy.x identifier
#    decoyfilename = f"decoy.{decoy}.pdb" # get actual decoy filename
#    evaluation = evaluate_decoy(decoyfilename, OG_file) # run evaluation
#    evaluation_outputs[decoy_number] = evaluation # add evaluation output to dictionary

# Temp decoy list for test
decoys = [1110,1555,1690,28,573]

for item in decoys:
    decoy_number = f"decoy.{item}" # Get decoy.x identifier
    decoyfilename = f"{target_dir}/decoy.{item}.pdb" # get actual decoy filename
    evaluation = evaluate_decoy(decoyfilename, OG_file) # run evaluation
    evaluation_outputs[decoy_number] = evaluation # add evaluation output to dictionary

#*************************************************************************

# Add data to list
evaluation_output.append(evaluation_outputs)

# Define json filename
out_json_filename = f"{filename_stripped}_evaluation.json"

# Dump to json
with open(out_json_filename, 'w') as file:
    json.dump(evaluation_output, file)


