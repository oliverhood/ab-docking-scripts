#!/usr/bin/env python3
"""
Program: runprofit
File:    runprofit.py

Version: V1.0
Date:    
Function: Process the output files of docking algorithms run on split antibody/antigen structures to compare them to the original antibody/antigen structures using ProFit.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program automates the process of comparing the results of a docking algorithm (using split antibody/antigen complexes as input) to the original antibody/antigen complex using ProFit to calculate the RMSD between the two structures. The program can be split into a number of steps:
   1. Combine the split antibody (_ab.pdb) and docked antigen (_dag.pdb) files into a single PDB file (_abDag.pdb).
   2. Write a control script for ProFit, specifying the chainid for the antigen chain.
   3. Run ProFit to compare the structures of the combined antibody/docked antigen structure with the original antibody/antigen structure.
   4. Output the RMSD values across all atoms and across the C-alpha atoms.

--------------------------------------------------------------------------

Usage:
======
runprofit OG_file Ab_file DAg_file OUTPath

Where:
OG_file is the original, unsplit antibody/antigen complex
Ab_file is the split antibody file
DAg_file is the docked antigen file (output from docking algorithm)
OUTPath (optional) is the directory that new files will be written to

--------------------------------------------------------------------------

Revision History:
=================
V1.0   11.11.21   Original   By: OECH

"""

#*************************************************************************

# Import Libraries

import sys
import os
import subprocess
from runprofit_lib import (combineabdagfiles, getantigenchainid, writecontrolscript)

#*************************************************************************

# Get input files from command line
# Original PDB file
OG_file = sys.argv[1]
# Antibody file
Ab_file = sys.argv[2]
# Docked antigen file
DAg_file = sys.argv[3]
# Get output path from command line (if present)
OUTPath = ''
try:
   OUTPath = sys.argv[4] + '/'
except IndexError:
   print('No output directory specified, writing files to current directory')
   OUTPath = './'

# Combine the antibody and docked antigen files
testfile = str(combineabdagfiles(Ab_file, DAg_file, OUTPath))

# Write the profit control script
script = str(writecontrolscript(OG_file))

# Run profit, returning the RMS values across all atoms and across CA atoms
result = subprocess.check_output("profit -f" + " " + script + " " + OG_file + " " + testfile + " | grep 'RMS' | tail -2", shell=True)
# Decode results
result = str(result, 'utf-8')
# Split result text into list
result = result.split()
# Set all_atoms RMSD
all_atoms = result[1]
# Set CA atoms RMSD
CA_atoms = result[3]
# Print RMSD values
print('All atoms RMSD:  '+all_atoms)
print('CA atoms RMSD:   '+CA_atoms)
# Remove .prf file
subprocess.run(['rm ' + script], shell=True)
# Print finished to commandline
print("runprofit: Done")