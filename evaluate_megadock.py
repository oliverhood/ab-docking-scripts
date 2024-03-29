#!/usr/bin/env python3
"""
Program: evaluate_megadock
File:    evaluate_megadock.py

Version:  V1.0
Date:     26.06.23
Function:   Run evaluate_interface on outputs of CL's megadock Docking
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
V1.0   26.06.23   Original   By: OECH
V2.0   17.03.24   Modified for new results directory structure   By: OECH

"""

#*************************************************************************

# Import libraries
import sys, os, subprocess

#*************************************************************************

filename = sys.argv[1]

#*************************************************************************

# Get input name (not sure if sys arg takes full path or just dir name)
filename_stripped = filename.split('/')[1]

# Get PWD
pwd = os.getcwd()

# Define target directory
target_dir = f"{pwd}/{filename_stripped}"

# Find OG file
OG_file = f"/home/oliverh/data/CL_OH_megadock_redo/complex_files/pdb{filename_stripped}.pdb"

#*************************************************************************

# Define list of metrics
evaluation_outputs = []

# Add filename
evaluation_outputs += [filename_stripped]

#*************************************************************************

# Evaluate each output
print(filename_stripped, flush=True)

# rank1
print("Rank1:", flush=True)
rank_1 = f"{target_dir}/{filename_stripped}_1.pdb"

# Run evaluation
output_1 = str(subprocess.run([f"~/ab-docking-scripts/evaluate_interface.py {OG_file} {rank_1}"], shell=True))

print("", flush=True)
# save evaluation
#evaluation_outputs += ["Rank 1:"]
#evaluation_outputs += [output_1]

# rank2
print("Rank2:", flush=True)
rank_2 = f"{target_dir}/{filename_stripped}_2.pdb"

# Run evaluation
output_2 = str(subprocess.run([f"~/ab-docking-scripts/evaluate_interface.py {OG_file} {rank_2}"], shell=True))

print("", flush=True)
# save evaluation
#evaluation_outputs += ["Rank 2:"]
#evaluation_outputs += [output_2]

# rank3
print("Rank3:", flush=True)
rank_3 = f"{target_dir}/{filename_stripped}_3.pdb"

# Run evaluation
output_3 = str(subprocess.run([f"~/ab-docking-scripts/evaluate_interface.py {OG_file} {rank_3}"], shell=True))

print("", flush=True)
# save evaluation
#evaluation_outputs += ["Rank 3:"]
#evaluation_outputs += [output_3]

# rank4
print("Rank4:", flush=True)
rank_4 = f"{target_dir}/{filename_stripped}_4.pdb"

# Run evaluation
output_4 = str(subprocess.run([f"~/ab-docking-scripts/evaluate_interface.py {OG_file} {rank_4}"], shell=True))

print("", flush=True)
# save evaluation
#evaluation_outputs += ["Rank 4:"]
#evaluation_outputs += [output_4]

# rank5
print("Rank5:", flush=True)
rank_5 = f"{target_dir}/{filename_stripped}_5.pdb"

# Run evaluation
output_5 = str(subprocess.run([f"~/ab-docking-scripts/evaluate_interface.py {OG_file} {rank_5}"], shell=True))

print("", flush=True)
# save evaluation
#evaluation_outputs += ["Rank 5:"]
#evaluation_outputs += [output_5]

# Add end line
print("*************************************************************************", flush=True)
#*************************************************************************

# Print outputs

#for item in evaluation_outputs:
#    print(item)

#*************************************************************************

# Remove interim files
subprocess.run(["rm ./*_contacts"], shell=True)

