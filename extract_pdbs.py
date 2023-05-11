#!/usr/bin/env python3
"""
Program: extract_pdbs
File:    extract_pdbs.py

Version:  V1.0
Date:     11.05.23
Function: Filter through the output directories of tesdockingprogs_master to extract docking result PDBs.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes the log file for a docking run as input and filters through it to find the ids of files that were
entered into the docking protocol. Output PDB files are identified and copied to a new directory.

--------------------------------------------------------------------------

Usage:
======
extract_pdbs.py logfile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   11.05.23   Original   By: OECH

"""

#*************************************************************************

# Import libraries

import sys, os, subprocess

#*************************************************************************

# Specify input file

LOGfile = sys.argv[1]

# Get current working directory
directory = os.getcwd()
# Get output path from command line (if present)
OUTPath = directory + "/"
try:
   OUTPath = sys.argv[2] + '/'
except IndexError:
   print('No output directory specified, writing files to current directory')
   OUTPath = directory + "/"

#*************************************************************************

# Get pdb ids from input file

# Initialise list
list_ids = []

# Open log file
with open(LOGfile) as file:
   # Read lines
   rows = file.readlines()
   # Filter for files that were run
   for line in rows:
      if 'Starting docking program on' in line:
         # Get filename
         file_id = line.split(' on ')[1].split('...')[0]
         # Add to list
         list_ids += [file_id]

#*************************************************************************

# Get PDB files

# Get current directory
pwd = os.getcwd()

# Move to results directory if there
for item in list_ids:
    # Get path to location of logfile
    path = os.path.dirname(os.path.realpath(LOGfile))
    # Search through contents of path for docking results directory
    for file in os.listdir(path):
        if file.startswith('docking_results'):
            # Define docking results directory
            docking_results = file
    # Run0
    # Check if output directory 1 (run0) exists
    output_dir_0 = f"{path}/{docking_results}/{item}/run0/"
    if os.path.isdir(output_dir_0):
        # Print statement that file produced full results
        print(f"{item} has results, copying output PDBs")
        # Define result file locations and names
        og = f"{path}/{docking_results}/{item}/{item}.pdb"
        megadock_0 = f"{output_dir_0}{item}_MegadockRanked_result.pdb"
        piper_0 = f"{output_dir_0}{item}_nohydrogens_Piper_result.pdb"
        rosetta_0 = f"{output_dir_0}{item}_Rosetta_result.pdb"
        haddock_waters_0 = f"{output_dir_0}/haddock_out/{item}_nohydrogens_Haddock_waters_result.pdb"
        haddock_nowaters_0 = f"{output_dir_0}/haddock_out/{item}_nohydrogens_Haddock_nowaters_result.pdb"
        # Define output directory
        out_dir_combined_0 = "/home/oliverh/data/pdb_files/output_PDBs/run0"
        # Make output directory
        subprocess.run([f"mkdir {out_dir_combined_0}"], shell=True)
        # Copy the files to new directory
        subprocess.run([f"cp {megadock_0} {piper_0} {rosetta_0} {haddock_waters_0} {haddock_nowaters_0} {og} {out_dir_combined_0}"], shell=True)
    # Fail line
    else:
        print(f"No results directory found for {item}.")

    # Run1
    # Check if output directory 2 (run1) exists
    output_dir_1 = f"{path}/{docking_results}/{item}/run1/"
    if os.path.isdir(output_dir_1):
        # Print statement that file produced full results
        print(f"{item} has results, copying output PDBs")
        # Define result file locations and names
        og = f"{path}/{docking_results}/{item}/{item}.pdb"
        megadock_1 = f"{output_dir_1}{item}_MegadockRanked_result.pdb"
        piper_1 = f"{output_dir_1}{item}_nohydrogens_Piper_result.pdb"
        rosetta_1 = f"{output_dir_1}{item}_Rosetta_result.pdb"
        haddock_waters_1 = f"{output_dir_1}/haddock_out/{item}_nohydrogens_Haddock_waters_result.pdb"
        haddock_nowaters_1 = f"{output_dir_1}/haddock_out/{item}_nohydrogens_Haddock_nowaters_result.pdb"
        # Define output directory
        out_dir_combined_1 = "/home/oliverh/data/pdb_files/output_PDBs/run1"
        # Make output directory
        subprocess.run([f"mkdir {out_dir_combined_1}"], shell=True)
        # Copy the files to new directory
        subprocess.run([f"cp {megadock_1} {piper_1} {rosetta_1} {haddock_waters_1} {haddock_nowaters_1} {og} {out_dir_combined_1}"], shell=True)
    # Fail line
    else:
        print(f"No results directory found for {item}.")

    # Run2
    # Check if output directory 3 (run2) exists
    output_dir_2 = f"{path}/{docking_results}/{item}/run2/"
    if os.path.isdir(output_dir_2):
        # Print statement that file produced full results
        print(f"{item} has results, copying output PDBs")
        # Define result file locations and names
        og = f"{path}/{docking_results}/{item}/{item}.pdb"
        megadock_2 = f"{output_dir_2}{item}_MegadockRanked_result.pdb"
        piper_2 = f"{output_dir_2}{item}_nohydrogens_Piper_result.pdb"
        rosetta_2 = f"{output_dir_2}{item}_Rosetta_result.pdb"
        haddock_waters_2 = f"{output_dir_2}/haddock_out/{item}_nohydrogens_Haddock_waters_result.pdb"
        haddock_nowaters_2 = f"{output_dir_2}/haddock_out/{item}_nohydrogens_Haddock_nowaters_result.pdb"
        # Define output directory
        out_dir_combined_2 = "/home/oliverh/data/pdb_files/output_PDBs/run2"
        # Make output directory
        subprocess.run([f"mkdir {out_dir_combined_2}"], shell=True)
        # Copy the files to new directory
        subprocess.run(
            [f"cp {megadock_2} {piper_2} {rosetta_2} {haddock_waters_2} {haddock_nowaters_2} {og} {out_dir_combined_2}"],
            shell=True)
    # Fail line
    else:
        print(f"No results directory found for {item}.")

# Print that file extraction is complete for item in list
    print(f"File extraction complete for {item}.")

# Print run complete
print("File extraction for chunkx is complete.")