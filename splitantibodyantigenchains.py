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
split-antibody-antigen-files.py PDBFILE OUTPath

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
from splitantibodyantigenchains_lib import (getantigenchainid, extractantibodychains, extractantigenchain)

#*************************************************************************

# Get PDB file from command line
PDBfile = sys.argv[1]

# Get output path from command line (if present)
if len(sys.argv) >= 2:
   OUTPath = sys.argv[2] + '/'
# If no output path is specified write to current directory
else:
   OUTPath = '/'

# Get the antigen's chain id
agchainid = getantigenchainid(PDBfile)

# Filter out files with multiple or no antigen chains
if agchainid != 'Multiple chains' and agchainid != 'No chains':
   # Extract antibody chains from PDB
   antibody_chains = extractantibodychains(PDBfile)

   # Extract and process antigen chain from PDB
   processed_antigen_chain = extractantigenchain(PDBfile)

   # Get the base filename from input file
   filename = os.path.basename(PDBfile).split('.')[0]

   # Specifying new filenames
   ab_filename = "%s_ab.pdb" % filename
   ag_filename = "%s_ag.pdb" % filename

   # Write Antibody file
   ab_file = open(str(OUTPath+ab_filename), "w")
   ab_file.write(antibody_chains)
   ab_file.close()

   # Write Antigen file
   ag_file = open(str(OUTPath+ag_filename), "w")
   ag_file.write(processed_antigen_chain)
   ag_file.close()