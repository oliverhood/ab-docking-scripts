#!/usr/bin/env python3
"""
Program: runmegadock
File:    runmegadock.py

Version: V1.0
Date:    
Function: Run input antibody and antigen files through the Megadock docking algorithm and extract the top-ranked docked ligand into a new PDB file.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============

--------------------------------------------------------------------------

Usage:
======
runmegadock.py receptorfile ligandfile OUTPath

--------------------------------------------------------------------------

Revision History:
=================

"""

#*************************************************************************

#Import Libraries

import sys
import os
import subprocess

#*************************************************************************

# Define receptor (antibody) file
receptor = sys.argv[1]
# Define ligand (antigen) file
ligand = sys.argv[2]
# Get output path from command line (if present)
OUTPath = ''
try:
   OUTPath = sys.argv[4] + '/'
except IndexError:
   print('No output directory specified, writing files to current directory')
   OUTPath = './'
# Run Megadock
subprocess.run(["~/DockingSoftware/megadock-4.1.1/megadock -R " + receptor + " -L " + ligand + " -o megadock.out"], shell=True)
# Get input file basename
filenamecontents = os.path.basename(receptor).split('.')[0].split('_')
inputfilename = filenamecontents[0] + "_" + filenamecontents[1]
# Define output filename
outfile = inputfilename + "_Dag.pdb"
# Extract top docking result from megadock using decoygen
subprocess.run(["~/DockingSoftware/megadock-4.1.1/decoygen " + outfile + " " + ligand + " megadock.out 1"], shell=True)
# Remove megadock.out file
subprocess.run(["rm megadock.out"], shell=True)