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
runrosetta.py PDBfile num_outputs OUTPath

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
from runrosetta_lib import (writeprepack_flags, writedocking_flags, getbestresult)

#*************************************************************************

# Define Input Files
# Processed (splitantibodyantigenchains_rosetta.py) file
PDBfile = sys.argv[1]

# Get number of docking runs to carry out (num_outputs)
runs = int(sys.argv[2])

# Define OUTPath
OUTPath = './'
try:
   OUTPath = sys.argv[3] + '/'
except IndexError:
   OUTPath = './'

#*************************************************************************

# Prepack the input structure

# Write prepack_flags
writeprepack_flags(PDBfile, runs)

# Run the prepack protocol
subprocess.run(["/home/oliverh/DockingSoftware/rosetta/rosetta/main/source/bin/docking_prepack_protocol.default.linuxgccrelease @prepack_flags"], shell=True)

#*************************************************************************

# Perform docking run

# Write docking_flags
writedocking_flags(PDBfile)

# Run the docking protocol
subprocess.run(["/home/oliverh/DockingSoftware/rosetta/rosetta/main/source/bin/docking_protocol.default.linuxgccrelease @docking_flags"], shell=True)

#*************************************************************************

# Get the best docked structure from the scores file
scores_file = "score_local_dock.sc"
best_structure = getbestresult(scores_file)
best_structure_file = OUTPath + best_structure

# Get input filename
filename = os.path.basename(PDBfile).split('.')[0]
# Define new filename for best structure
rosetta_out = OUTPath + filename + "_docked.pdb"

# Copy the file contents to new file
subprocess.run([f"cp {best_structure_file} {rosetta_out}"], shell=True)

#*************************************************************************