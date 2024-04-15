#!/usr/bin/env python3
"""
Program: maskNIres
File     maskNIres.py

Version:  V1.0
Date:     28.11.21
Function: Write PDB file to mask non-interface residues in antibody-antigen complex when running docking algorithms.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program uses AM's findif.pl script to identify interface residues in an input antibody-antigen complex structure then uses these to write residues to a 'mask' PDB file to be used as input to docking algorithms.

--------------------------------------------------------------------------

Usage:
======

maskNIres.py OG_file Ab_file Ag_file OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   28.11.21   Original   By: OECH

"""

#*************************************************************************

# Import Libraries

import os
import sys
import subprocess
import re

#*************************************************************************

# Define input files
# Original PDB file
OG_file = sys.argv[1]
# Antibody file
Ab_file = sys.argv[2]
# Antigen file
Ag_file = sys.argv[3]
# Get output path from command line (if present)
OUTPath = './'
try:
   OUTPath = sys.argv[4] + '/'
except IndexError:
   OUTPath = './'

#*************************************************************************
# Find interface residues

# Define location for interface residues file
int_res = OUTPath + "int_res"

# Run findif.pl to identify interface residues, writing result to int_res
subprocess.run(["~/ab-docking-scripts/findif.pl -x " + OG_file + " " + Ab_file + " " + Ag_file + " > " + int_res], shell=True)

#*************************************************************************
Hres = []
Lres = []

# Read int_res and extract residue numbers
with open(int_res) as file:
   # Read rows in file
   rows = file.readlines()
   # Identify heavy and light chain residues
   for line in rows:
      # Heavy chain
      if 'H' in line:
         contents = re.compile("([a-zA-Z]+)([0-9]+)").match(line)
         Hres += [contents.group(2)]
      # Light chain
      if 'L' in line:
         contents = re.compile("([a-zA-Z]+)([0-9]+)").match(line)
         Lres += [contents.group(2)]

#*************************************************************************
# Get length of heavy and light chains

# Set Hlength and Llength as variables
Hlength = ''
Llength = ''

# Get length of Heavy and Light chains from antibody file
with open(Ab_file) as file:
   # Read rows in file
   rows = file.readlines()
   # Identify terminal heavy chain residue
   for line in rows:
      if 'TER ' and 'H' in line and 'ATOM' not in line:
         Hcontents = line.split()
         Hlength = Hcontents[4]
      if 'TER ' and 'L' in line and 'ATOM' not in line:
            Lcontents = line.split()
            Llength = Lcontents[4]

#*************************************************************************
 # Create lists of residues to be blocked

# Heavy chain
Hblock = []
for i in range(int(Hlength)+1):
   if str(i) not in Hres:
      Hblock += [str(i)]
# Light chain
Lblock = []
for i in range(int(Llength)+1):
   if str(i) not in Lres:
      Lblock += [str(i)]

#*************************************************************************
# Get PDB lines for residues not in interface

#Define PDB lines list
PDBline = []
# Opem Ab file
with open(Ab_file) as file:
   rows = file.readlines()
   # Loop through lines
   for line in rows:
      # Filter 'ATOM' lines
      if 'ATOM' in line:
         # Split line
         contents = line.split()
         # Filter through heavy chain residues
         if contents[4] == 'H':
            # Extract residue ID (number)
            resid = contents[5]
            if resid in Hblock:
               PDBline += [line]
         if contents[4] == 'L':
            # Extract residue ID (number)
            resid = contents[5]
            if resid in Lblock:
               PDBline += [line]

#*************************************************************************
# Write 'Mask' file

# Get the base filename from the input file
filename = os.path.basename(OG_file).split('.')[0]

# Define output filename
outfile = OUTPath + filename + '_maskfile.pdb'

# Write maskfile.pdb
with open(outfile, "w") as file:
   for line in PDBline:
      file.write(line)

#*************************************************************************

# Clean up

# Remove 'int_res' file
subprocess.run([f"rm {int_res}"], shell=True)