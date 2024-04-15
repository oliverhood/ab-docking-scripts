#!/usr/bin/env python3
"""
Program: runprofit_single
File:    runprofit_single.py

Version: V1.0
Date:
Function: Process the output files of docking algorithms run on split antibody/antigen structures to compare them to the original antibody/antigen structures using ProFit. Input is in the form of a single PDB file containing both the antibody and docked antigen chains.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program automates the process of comparing the results of a docking algorithm (using split antibody/antigen complexes as input) to the original antibody/antigen complex using ProFit to calculate the RMSD between the two structures.

--------------------------------------------------------------------------

Usage:
======
runprofit_single OG_file Docked_file OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   06.12.2021   Original   By: OECH

"""

#*************************************************************************

# Import Libraries

import sys, os
import subprocess
from .runprofit_lib import (writecontrolscript)

#*************************************************************************

# Get input files from command line
# Original PDB file
OG_file = sys.argv[1]
# Docked structure file
Docked_file = sys.argv[2]
# Get output path from command line (if present)
OUTPath = ''
try:
   OUTPath = sys.argv[3] + '/'
except IndexError:
   OUTPath = './'

# Get input filenames
inputfilename = os.path.basename(OG_file).split('.')[0]
docked_filename = os.path.basename(Docked_file).split('.')[0]

# Define new filenames
OG_nohydrogens = OUTPath + inputfilename + "_nohydrogens.pdb"
docked_nohydrogens = OUTPath + docked_filename + "_nohydrogens.pdb"

# Strip hydrogens from input files
subprocess.run([f"pdbhstrip {OG_file} {OG_nohydrogens}"], shell=True)
subprocess.run([f"pdbhstrip {Docked_file} {docked_nohydrogens}"], shell=True)

# Write the profit control script
script = str(writecontrolscript(OG_file))

# Run profit, returning the RMS values across all atoms and across CA atoms
result = subprocess.check_output("profit -f" + " " + script + " " + OG_nohydrogens + " " + docked_nohydrogens + " | grep 'RMS' | tail -2", shell=True)
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