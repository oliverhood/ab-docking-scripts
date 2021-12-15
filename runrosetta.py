#!/usr/bin/env python3
"""
Program: runrosetta
File:    runrosetta.py

Version:  V1.0
Date:     03.12.21
Function: Takes a PDB file containing an antibody and an antigen as input and runs the Rosetta docking algorithm on them, extracting the top scoring structure as the output.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing an antibody and an antigen as input, pre-processes the file using the Rosetta 'prepack' protocol, generates __ docked structures using the Rosetta 'protein-protein docking' protocol, then extracts the top scoring structure as the docking result.

--------------------------------------------------------------------------

Usage:
======
runrosetta.py PDBfile antibody antigen num_outputs OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   03.12.2021   Original   By: OECH

"""

#*************************************************************************

# Import Libraries

import subprocess
import sys
import os
from runrosetta_lib import (writeprepack_flags, writedocking_flags, getbestresult, combine_input_files)

#*************************************************************************

# Define Input Files
# PDB file
PDBfile = sys.argv[1]
# Antibody file
antibody = sys.argv[2]

# Antigen file
antigen = sys.argv[3]

# Get number of docking runs to carry out (num_outputs)
runs = 10
try:
   runs = sys.argv[4]
except IndexError:
   runs = 10

# Define OUTPath
OUTPath = './'
try:
   OUTPath = sys.argv[5] + '/'
except IndexError:
   OUTPath = './'

#*************************************************************************

# Create directory to output docked PDBs
outdir = OUTPath + "docking_out"
subprocess.run([f"mkdir {outdir}"], shell=True)

#*************************************************************************

# Combine input files into signle PDB
combine_input_files(antibody, antigen)

# Define combined filename
# Get input filename
filename = os.path.basename(PDBfile).split('.')[0]
# Combined filename
combined_filename = OUTPath + filename + "_Rosetta_input.pdb"

#*************************************************************************

# Prepack the input structure

# Write prepack_flags
writeprepack_flags(PDBfile)

# Run the prepack protocol
subprocess.run(["/home/oliverh/DockingSoftware/rosetta/rosetta/main/source/bin/docking_prepack_protocol.default.linuxgccrelease @prepack_flags"], shell=True)

#*************************************************************************

# Perform docking run

# Write docking_flags
writedocking_flags(PDBfile, runs)

# Run the docking protocol
subprocess.run(["/home/oliverh/DockingSoftware/rosetta/rosetta/main/source/bin/docking_protocol.default.linuxgccrelease @docking_flags"], shell=True)

#*************************************************************************

# Get the best docked structure from the scores file
scores_file = "score_local_dock.sc"
best_structure = getbestresult(scores_file)
best_structure_file = OUTPath + best_structure
best_structure_file_compressed = best_structure_file + ".gz"

# Define new filename for best structure
rosetta_out = OUTPath + filename + "_Rosetta_result.pdb"

# Decompress best result
subprocess.run([f"gunzip {outdir}/{best_structure_file_compressed}"])
# Copy the file contents to new file
subprocess.run([f"cp {outdir}/{best_structure_file} {rosetta_out}"], shell=True)

#*************************************************************************