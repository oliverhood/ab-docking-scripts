#!/usr/bin/env python3
"""
Program: getfasta
File:    getfasta.py

Version:  V1.0
Date:     15.02.2022
Function: Extract fasta sequence from input pdb file and output into separate.fasta format

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file as input and extracts the sequences within it in fasta format using pdb2pir.

--------------------------------------------------------------------------

Usage:
======
getfasta.py PDBFile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   12.11.21   Original   By: OECH

"""

#*************************************************************************

# Import Libraries
import sys, os, subprocess

#*************************************************************************

# Define input file
PDBfile = sys.argv[1]

# Get output path from command line (if present)
OUTPath = './'
try:
   OUTPath = sys.argv[2] + '/'
except IndexError:
   print('No output directory specified, writing files to current directory')
   OUTPath = './'

#*************************************************************************

# Get input filename
inputfilename = os.path.basename(PDBfile).split('.')[0]

# Define output file name
outputfilename = OUTPath + inputfilename + ".fasta"

#*************************************************************************

# Run pdb2pir on input file using -f flag for fasta format
subprocess.run([f"pdb2pir -f {PDBfile} {outputfilename}"], shell=True)

#*************************************************************************