#!/usr/bin/env python3
"""
Program: analyse_antigens
File:    analyse_antigens.py

Version:  V1.0
Date:     17.02.2022
Function: Perform analysis on antigens to determine whether there is a conformational change upon antibody binding.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============


--------------------------------------------------------------------------

Usage:
======

--------------------------------------------------------------------------

Revision History:
=================
V1.0   15.02.22   Original   By: OECH

"""

#*************************************************************************

# Import Libraries
import sys, os, subprocess, re
from dockingtools_lib import getantigenchainid

#*************************************************************************

# Define input files

# Complex file
complex = sys.argv[1]
# Free antigen
antigen = sys.argv[2]
# Free antibody
antibody = sys.argv[3]
# Get output path from command line (if present)
OUTPath = './'
try:
   OUTPath = sys.argv[4] + '/'
except IndexError:
   OUTPath = './'

#*************************************************************************

# Find interface residues in complex

# Define location for interface residues file
int_res = OUTPath + "int_res"

# Run findif.pl to identify interface residues, writing result to int_res
subprocess.run(["~/ab-docking-scripts/findif.pl -x " + complex + " " + antigen + " " + antibody + " > " + int_res], shell=True)

#*************************************************************************

# Get antigen interface residues

# Initialise list for antigen residues
ag_int_res = []

# Get antigen chain ID (single chain)
agchainid = getantigenchainid(complex)

# Read int_res and extract residue numbers
with open(int_res) as file:
   # Read rows in file
   rows = file.readlines()
   # Identify antigen chain residues
   for line in rows:
      if str(agchainid) in line:
         contents = re.compile("([a-zA-Z]+)([0-9]+)").match(line)
         ag_int_res += [contents.group(2)]

#*************************************************************************

# Write profit script

