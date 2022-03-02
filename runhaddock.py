#!/usr/bin/env python3
"""
Program: runhaddock
File:    runhaddock.py

Version:  V1.0
Date:     15.02.2022
Function: Run input antibody and antigen files through the haddock protein docking algorithm, output a single result file.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes an antibody file and an antigen file as input for the haddock protein docking program, a single PDB file will be extracted as a result with waters included and without waters included (waters should be better?).

--------------------------------------------------------------------------

Usage:
======
runhaddock.py antibody antigen length OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   15.02.22   Original   By: OECH

"""

#*************************************************************************

# Import libraries
import sys, os, subprocess
from runhaddock_lib import clean_inputs, generate_unambig_tbl, generate_run_param, edit_run_cns, extract_best_results

#*************************************************************************

# Get input files

# antibody
antibody = sys.argv[1]

# antigen
antigen = sys.argv[2]

# length
length = sys.argv[3]

# Get output path from command line (if present)
OUTPath = './'
try:
   OUTPath = sys.argv[4] + '/'
except IndexError:
   print('No output directory specified, writing files to current directory')
   OUTPath = './'

#*************************************************************************

# Get input filenames

# Antibody
ab_filename = os.path.basename(antibody).split('.')[0]
# Antigen
ag_filename = os.path.basename(antigen).split('.')[0]

# Clean input files
clean_inputs(antibody, antigen, ab_filename, ag_filename)

#*************************************************************************

# Generate unambig_tbl file
generate_unambig_tbl(ab_filename)

#*************************************************************************

# Generate run.param file
generate_run_param(ab_filename, ag_filename, OUTPath)

#*************************************************************************

# Run haddock2.4 for first time
subprocess.run([f"/home/DockingSoftware/haddock2.4/Haddock/RunHaddock.py"], shell=True)

#*************************************************************************

# Edit CNS file
# Determine whether the run should be long or short
long=False
if length.lower() == 'long':
   long=True
# Edit file
edit_run_cns(long)

#*************************************************************************

# Move to run1 directory, run haddock2.4 again
subprocess.run(["cd run1"], shell=True)
subprocess.run(["/home/DockingSoftware/haddock2.4/Haddock/RunHaddock.py"], shell=True)

#*************************************************************************

# Move back to start directory
subprocess.run(["cd .."], shell=True)

# Extract result files

# Get base input filename
inputfilename = ab_filename.split('_ab')[0]

# Extract files
extract_best_results(inputfilename)

#*************************************************************************