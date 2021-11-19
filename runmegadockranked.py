#!/usr/bin/env python3
"""
Program: runmegadockranked
File:    runmegadockranked.py

Version: V1.0
Date:    18.11.21 
Function: Run input antibody and antigen files through the Megadock docking algorithm and extract the top-ranked docked ligand into a new PDB file.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a receptor (antibody), ligand (antigen), and their bound complex as input. The residues at the binding interface between the proteins is determined and non-interface residues are 'blocked' using the blockNIres program

--------------------------------------------------------------------------

Usage:
======
runmegadockranked.py receptorfile ligandfile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   19.11.2021   Original   By: OECH


"""

#*************************************************************************

#Import Libraries

import sys
import os
import subprocess

#*************************************************************************
# Run Megadock

# Define receptor (antibody) file
receptor = sys.argv[1]
# Define ligand (antigen) file
ligand = sys.argv[2]
# Get output path from command line (if present)
OUTPath = ''
try:
   OUTPath = sys.argv[3] + '/'
except IndexError:
   OUTPath = './'
# Run Megadock
subprocess.run(["~/DockingSoftware/megadock-4.1.1/megadock -R " + receptor + " -L " + ligand + " -o megadock.out"], shell=True)
# Get input file basename
filenamecontents = os.path.basename(receptor).split('.')[0].split('_')
inputfilename = filenamecontents[0] + "_" + filenamecontents[1]
# Define output filename
outfile = OUTPath+inputfilename + "_Dag.pdb"

#*************************************************************************
# Run ZRank