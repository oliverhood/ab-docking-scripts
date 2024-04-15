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
from .runhaddock_lib import clean_inputs, fix_chain_labelling, generate_unambig_tbl, rewrite_unambig_tbl, generate_run_param, edit_run_cns, extract_best_results

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

# Define unambig_tbl filename
unambig_tbl = './antibody-antigen-unambig.tbl'

# Rewrite unambig_tbl file to include segIDs
rewrite_unambig_tbl(unambig_tbl)

#*************************************************************************

# Generate run.param file
generate_run_param(ab_filename, ag_filename, OUTPath)

#*************************************************************************

# Run haddock2.4 for first time
subprocess.run([f"/home/oliverh/DockingSoftware/haddock2.4/Haddock/RunHaddock.py"], shell=True)

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
subprocess.run(["cd run1; /home/oliverh/DockingSoftware/haddock2.4/Haddock/RunHaddock.py"], shell=True)

#*************************************************************************

# Move back to start directory
subprocess.run(["pwd"], shell=True)

# Extract result files

# Get base input filename
inputfilename = ab_filename.split('_ab')[0]

# Extract files
extract_best_results(inputfilename)

#*************************************************************************

# Split antibody chains and relabel chains for final result file

# Define nowaters resultfile
resultfile_nowaters = f"{inputfilename}_Haddock_nowaters_result.pdb"

# Define waters resultfile
resultfile_waters = f"{inputfilename}_Haddock_waters_result.pdb"

# Run fix_chain_labelling on nowaters file
fix_chain_labelling(antigen, resultfile_nowaters)

# Run fix_chain_labelling on waters file
fix_chain_labelling(antigen, resultfile_waters)

#*************************************************************************