#!/usr/bin/env python3
"""
Program: split_abag_chains_rosetta
File:    split_abag_chains_rosetta.py

Version:  V1.0
Date:     01.12.21
Function: Extract and process antigen and antibody chains from a PDB file
          for input to docking algorithms.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody (that may or may not be bound by an antigen(s)), separates the antibody and antigen chains, and returns them in the same PDB file. The antigen chain is processed (randomly rotated and transformed) before being written to the new PDB file.

--------------------------------------------------------------------------

Usage:
======
split_abag_chains_rosetta.py PDBFILE OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   01.12.21   Original   By: OECH
"""
#*************************************************************************

# Import Libraries
import sys
import os
import random
from .split_abag_chains_lib import (get_antigen_chain_label, extract_antibody_chains, extract_antigen_chain)

#*************************************************************************

# Get PDB file from command line
PDBfile = sys.argv[1]

# Get output path from command line (if present)
OUTPath = ''
try:
   OUTPath = sys.argv[2] + '/'
except IndexError:
   OUTPath = ''
# Get the antigen's chain id
agchainid = get_antigen_chain_label(PDBfile)

# Filter out files with multiple or no antigen chains
if agchainid != 'Multiple chains' and agchainid != 'No chains':
   # Extract antibody chains from PDB
   antibody_chains = extract_antibody_chains(PDBfile)
   # Extract and process antigen chain from PDB
   processed_antigen_chain = extract_antigen_chain(PDBfile)
   # Initialise the list of file lines
   file_lines = []
   # Split antibody chain into lines
   antibody_lines = antibody_chains.splitlines()
   # Split antigen chain into lines
   antigen_lines = processed_antigen_chain.splitlines()
   # Write (most) antibody lines to file_lines
   for line in antibody_lines:
      if 'END' not in line:
         file_lines += [line + '\n']
   # Write atom antigen lines to file_lines
   for line in antigen_lines:
      if 'ATOM' in line:
         file_lines += [line + '\n']
   # Get the base filename from input file
   filename = os.path.basename(PDBfile).split('.')[0]
   # Specifying new filename
   processed_filename = "%s_processed.pdb" % filename
   # Write new PDB file
   with open(processed_filename, "w") as file:
      for line in file_lines:
         file.write(line)