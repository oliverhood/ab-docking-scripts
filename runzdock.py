#!/usr/bin/env python3
"""
Program: runzdock
File:    runzdock.py

Version: V1.0
Date:    13.12.21 
Function: Run input antibody and antigen files through the Zdock docking algorithm and extract the top-ranked docked ligand into a new PDB file.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a receptor (antibody), ligand (antigen), and their bound complex as input. The residues at the binding interface between the proteins is determined and non-interface residues are 'blocked' using the blockNIres program

--------------------------------------------------------------------------

Usage:
======
runzdock.py receptorfile ligandfile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   13.12.21   Original   By: OECH


"""

#*************************************************************************

# Import libraries

import sys, os, subprocess

#*************************************************************************

# Define input files

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

#*************************************************************************

# Add hydrogens to input files

# Get input file basename
filenamecontents = os.path.basename(receptor).split('.')[0].split('_')
inputfilename = filenamecontents[0] + "_" + filenamecontents[1]
# Define output antibody file name
antibody_hydrogens = OUTPath + inputfilename + "_ab_hydrogens.pdb"
# Define output antigen file name
antigen_hydrogens = OUTPath + inputfilename + "_ag_hydrogens.pdb"
# Antibody file
subprocess.run([f"pdbhadd -a {receptor} {antibody_hydrogens}"], shell=True)
# Antigen file
subprocess.run([f"pdbhadd -a {ligand} {antigen_hydrogens}"], shell=True)

#*************************************************************************

# Run zdock
subprocess.run([f"~/DockingSoftware/zdock3.0.2/zdock -R {antibody_hydrogens} -L {antigen_hydrogens} -o {OUTPath}zdock.out"], shell=True)

#*************************************************************************

# Run zrank
subprocess.run([f"~/DockingSoftware/zdock3.0.2/zrank {OUTPath}zdock.out 1 2000"], shell=True)

# Extracting top ranked output
# Initiate min out variable
min_out = 0

# Read Zrank out file
with open('zdock.out.zr.out') as file:
   # Read lines
   rows = file.readlines()
   # Identify highest scoring output
   for line in rows:
      contents = line.split()
      if float(contents[1]) < min_out:
         min_out = float(contents[1])
         # Get number of the top hit
         top_hit = contents[0]

#*************************************************************************

# Define output filename
outfile = OUTPath+inputfilename + "_zdock_Dag.pdb"

# Extract top docking result from zdock using megadock's decoygen script
subprocess.run([f"~/DockingSoftware/megadock-4.1.1/decoygen {outfile} {antigen_hydrogens} {OUTPath}zdock.out {top_hit}"], shell=True)

#*************************************************************************

# Tidy up unecessary files
#subprocess.run(["rm zdock.out zdock.out.zr.out"], shell=True)