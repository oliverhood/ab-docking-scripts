#!/usr/bin/env python3
"""
Program: split-antibody-antigen-files
File:    split-antibody-antigen-files.py

Version: V1.0
Date: 04.11.21
Function: Extract and process antigen and antibody chains from a PDB file 
          for input to docking algorithms.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody (that
may or may not be bound by an antigen(s)) and returns the antibody and 
antigen(s) chains as separate PDB files. The antigen chain is processed 
(randomly rotated and transformed) before being written to the new PDB 
file.

--------------------------------------------------------------------------

Usage:
======
split-antibody-antigen-files.py PDBFILE

--------------------------------------------------------------------------

Revision History:
=================
V1.0   08.11.21   Original   By: OECH
"""

#*************************************************************************

# Import Libraries
import sys
import os
import random
from split-antibody-antigen-files_lib import (getantigenchainid, extractantibodychains, extractantigenchain)

#*************************************************************************

# Get PDB files from command line
PDBfile = sys.argv[1]

# Extract antibody chains from PDB
antibody_chains = extractantibodychains(PDBfile)

# Extract and process antigen chain from PDB
processed_antigen_chain = extractantigenchain(PDBfile)

# Get the base filename from input file
filename = os.path.splitext(PDBfile)[0]

# Specifying new filenames
ab_filename = "%s_ab.pdb" filename
ag_filename = "%s_ag.pdb" filename

# Write Antibody file
ab_file = open(ab_filename, "w")
ab_file.write(antibody_chains)
ab_file.close()

# Write Antigen file
ag_file = open(ag_filename, "w")
ag_file.write(processed_antigen_chain)
ag_file.close()