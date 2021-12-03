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
runrosetta.py PDBfile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   03.12.2021   Original   By: OECH

"""

#*************************************************************************

# Import Libraries

import subprocess

#*************************************************************************

# Define Input Files
# Processed (splitantibodyantigenchains_rosetta.py) file
PDBfile = sys.argv[1]

# Define OUTPath
OUTPath = './'
try:
   OUTPath = sys.argv[2] + '/'
except IndexError:
   OUTPath = './'

#*************************************************************************

