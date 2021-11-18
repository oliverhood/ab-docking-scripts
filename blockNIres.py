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

blockNIres.py OG_file Ab_file Ag_file OUTPath

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

# Run 