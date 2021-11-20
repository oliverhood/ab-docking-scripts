#!/usr/bin/env python3
"""
Program: blockNIres
File:    blockNIres.py

Version:  V1.0
Date:     18.11.21
Function: Define list of non-interface residues in antibody-antigen complex to be blocked when running docking algorithms.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program uses AM's findif.pl script to identify interface residues in an input antibody-antigen complex structure then uses these to create a list of non-interface residues to be 'blocked' for input into docking algorithms.

--------------------------------------------------------------------------

Usage:
======

blockNIres.py OG_file Ab_file Ag_file [antibody/antigen] OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   18.11.21   Original   By: OECH

"""

#*************************************************************************

# Import Libraries

import os
import sys
import subprocess
import re
from runprofit_lib import getantigenchainid

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
   OUTPath = sys.argv[5] + '/'
except IndexError:
   OUTPath = './'

#*************************************************************************
# Find interface residues

# Define location for interface residues file
int_res = OUTPath + "int_res"

# Run findif.pl to identify interface residues, writing result to int_res
subprocess.run(["~/ab-docking-scripts/findif.pl -x " + OG_file + " " + Ab_file + " " + Ag_file + " > " + int_res], shell=True)

#*************************************************************************
# Block Antibody chain residues
if sys.argv[4] == 'antibody':
   # Create lists for Heavy and Light chain interface residues
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
   # Turn Hblock into string
   Hblock = ",".join(Hblock)
   # Light chain
   Lblock = []
   for i in range(int(Llength)+1):
      if str(i) not in Lres:
         Lblock += [str(i)]
   # Turn Lblock into string
   Lblock = ",".join(Lblock)

#*************************************************************************
   # Splitting heavy and light chains as megadock/block doesn't like blocking multiple chains in a single file

   # Get input file basename
   filename = os.path.basename(Ab_file).split('.')[0]

   # Split antibody file into H and L chains
   # Define Heavy chain filename
   heavyname = OUTPath + filename + "_heavy.pdb"
   # Get heavy chain
   subprocess.run(["pdbgetchain H " + Ab_file + " > " + heavyname], shell=True)
   # Define Light chain filename
   lightname = OUTPath + filename + "_light.pdb"
   # Get light chain
   subprocess.run(["pdbgetchain L " + Ab_file + " > " + lightname], shell=True)

#*************************************************************************
   # Block residues in the heavy and light chains separately

   # Define filename for heavy chain with blocked residues
   heavyblocked = OUTPath + filename + "_heavy_blocked.pdb"
   # Run megadock's blocking program to block heavy chain residues
   subprocess.run(["~/DockingSoftware/megadock-4.1.1/block " + heavyname + " H " + Hblock + " > " + heavyblocked], shell=True)
   # efine filename for light chain with blocked residues
   lightblocked = OUTPath + filename + "_light_blocked.pdb"
   # Run blocking program again to block ligth chain residues
   subprocess.run(["~/DockingSoftware/megadock-4.1.1/block " + lightname + " L " + Lblock + " > " + lightblocked], shell=True)

#*************************************************************************
   # Combine light and heavy chain blocked files

   # Define output filename
   outfile = OUTPath + filename + "_blocked.pdb"

   # Open heavy chain file
   with open(heavyblocked) as file:
      # Extract contents
      rows = file.readlines()
      # Get header from rows
      header = rows[0:4]
      # Get heavy chain contents (leave 'END' line)
      heavy = rows[4:-1]
   # Open light chain file
   with open(lightblocked) as file:
      # Extract contents
      rows = file.readlines()
      # Get light chain contents (leave 'END' line)
      light = rows[4:-1]
   # Combine header, heavy and light chains (light comes first apparently)
   combinedfile = header + light + heavy
   # Write the combined file
   with open(outfile, "w") as file:
      for line in combinedfile:
         file.write(line)

#*************************************************************************
   # Remove unneeded files

   subprocess.run(["rm "
   # int_res (interface residues file)
   + int_res
   # Heavy chain file
   + " " + heavyname
   # Light chain file
   + " " + lightname
   # Heavy blocked file
   + " " + heavyblocked
   # Light blocked file
   + " " + lightblocked], shell=True)

#*************************************************************************
# Block antigen chain residues
if sys.argv[4] == 'antigen':
   # Get antigen chain id
   agchainid = getantigenchainid(OG_file)
   # Create list for antigen interface residues:
   AG_res = []
   # Read int_res and extract residue numbers
   with open(int_res) as file:
      # Read rows in file
      rows = file.readlines()
      # Identify antigen chain residues
      for line in rows:
         if agchainid in line:
            contents = re.compile("([a-zA-Z]+)([0-9]+)").match(line)
            AG_res += [contents.group(2)]

#*************************************************************************
   # Get length of the antigen chain

   # Set antigen chain length as variable
   AGlength = ''

   # Get length of antigen chain from file
   with open(Ag_file) as file:
      # Read rows in file
      rows = file.readlines()
      # Identify terminal antigen chain residue
      for line in rows:
         if 'TER ' and agchainid in line and 'ATOM' not in line:
            AGcontents = line.split()
            # Get length of chain
            AGlength = AGcontents[4]

#*************************************************************************
   # Create list of residues to be blocked
   AGblock = []
   for i in range(int(AGlength)+1):
      if str(i) not in AG_res:
         AGblock += [str(i)]
   # Turn AGblock into string
   AGblock = ",".join(AGblock)

#*************************************************************************
   # Block residues in the antigen chain

   # Get input file basename
   filename = os.path.basename(Ag_file).split('.')[0]
   # Define output file name
   AGblocked = OUTPath + filename + "_blocked.pdb"
   # Run megadock's blocking program to block antigen chain residues
   subprocess.run(["~/DockingSoftware/megadock-4.1.1/block " + Ag_file + " " + agchainid + " " + AGblock + " > " + AGblocked], shell=True)

#*************************************************************************
   # Remove unneeded files

   subprocess.run(["rm "
   # int_res (interface residues file)
   + int_res], shell=True)