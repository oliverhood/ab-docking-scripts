#!/usr/bin/env python3
"""
Program: runprofit
File:    runprofit.py

Version: V1.0
Date:    
Function: Process the output files of docking algorithms run on split antibody/antigen structures to compare them to the original antibody/antigen structures using ProFit.

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


"""

#*************************************************************************

# Import Libraries

import sys
import os
import subprocess
from runprofit_lib import (combineabdagfiles, getantigenchainid, writecontrolscript)

#*************************************************************************

# Get input files from command line
# Original PDB file
OG_file = sys.argv[1]
# Antibody file
Ab_file = sys.argv[2]
# Docked antigen file
DAg_file = sys.argv[3]
# Get output path from command line (if present)
OUTPath = ''
try:
   OUTPath = sys.argv[4] + '/'
except IndexError:
   print('No output directory specified, writing files to current directory')
   OUTPath = './'

# Combine the antibody and docked antigen files
testfile = str(combineabdagfiles(Ab_file, DAg_file, OUTPath))

# Write the profit control script
script = str(writecontrolscript(OG_file))

# Run profit
result = subprocess.check_output(['profit','-f',script,OG_file,testfile, " | grep 'RMS' | tail -2"])
result = str(result, 'utf-8')