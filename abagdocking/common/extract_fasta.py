#!/usr/bin/env python3
"""
Program: extract_fasta
File:    extract_fasta.py

Version:  V1.0
Date:     14.01.2022
Function: Filter input PDB file for number of antigen chains then extract the sequences in files with a single antigen chain in FASTA format.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing an antibody-antigen complex as input, filters for the number of antigen chains present, then extracts the chain sequences in FASTA format.

--------------------------------------------------------------------------

Usage:
======
extract_fasta.py PDBfile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   14.01.2022   Original   By: OECH

"""

#*************************************************************************

# Import Libraries

import sys, os, subprocess
from dockingtools_lib import getantigenchainid

#*************************************************************************

# Get input file
PDBfile = sys.argv[1]

# Get output path from command line (if present)
OUTPath = './'
try:
   OUTPath = sys.argv[3] + '/'
except IndexError:
   OUTPath = './'

#*************************************************************************

# Get input file basename
filename = os.path.basename(PDBfile).split('.')[0]

# Get antigen chain ID (/number of antigen chains)
agchainid = getantigenchainid(PDBfile)

# Define output filename
output_name = f"{OUTPath}{filename}.fasta"

# Filter for number of antigen chains
if agchainid != 'Multiple chains' and agchainid != 'No chains':
   # Extract sequence, write to fasta file
   subprocess.run([f"pdb2pir -f {PDBfile} > {output_name}"], shell=True)