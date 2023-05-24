#!/usr/bin/env python3
"""
Program: testdockingprogs_master
File:    testdockingprogs_master_v2.py

Version:  V2.0
Date:     24.05.23
Function: Split input file into its antibody/antigen components for input into docking algorithms, run docking algorithm then evaluate the result using ProFit.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody/antigen complex as input, splits the file into its component chains, runs these chains through a docking algorithm, then evaluates the result using the ProFit program. The docking and evaluation steps are repeated for each docking algorithm specified.

--------------------------------------------------------------------------

Usage:
======
testdockingprogs_master_v2.py PDBFile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   12.11.21   Original   By: OECH
V2.0   24.05.23   Modified   By: OECH

"""

#*************************************************************************

# Import Libraries
import sys, os, subprocess, time, re, statistics
from threading import Timer
from dockingtools_lib import evaluate_results, getlowestscore, gethighestscore, getnumberhits, writefile, getantigenchainid
from testdockingprogs_master_lib import run_megadock, run_piper, run_rosetta, program_prompt, run_zdock, run_haddock

#*************************************************************************

# Specify input file
PDBfile = sys.argv[1]

# Get current working directory
directory = os.getcwd()
# Get output path from command line (if present)
OUTPath = directory + "/"
try:
   OUTPath = sys.argv[2] + '/'
except IndexError:
   print('No output directory specified, writing files to current directory')
   OUTPath = directory + "/"

#*************************************************************************

# Filter input file for number of antigen chains, end run if no chains or multiple antigen chains present
agchainid = getantigenchainid(PDBfile)

# Multiple chains
if agchainid == 'Multiple chains':
   sys.exit(f"Input file {PDBfile} contains multiple antigen chains, exiting program.")

# No chains
if agchainid == 'No chains':
   sys.exit(f"Input file {PDBfile} contains no antigen chains, exiting program.")

#*************************************************************************

# Get today's date
current_date = time.strftime(r"%d.%m.%Y", time.localtime())
current_date_f2 = time.strftime(r"%d_%m_%Y", time.localtime())
# Create Results file header
header = "Docking test on " + PDBfile + "   " + current_date
spacer = ""
# Create list starting with results file header
dockingresults = [header,spacer]

#*************************************************************************

# Prompt user for programs to run
"""
This section is now redundant but easier to leave boolean statements in than change the subsequent code for now.
"""

# Megadock
run_megadock_bool = True
#run_megadock_bool = program_prompt('Megadock')

# Piper
run_piper_bool = True
#run_piper_bool = program_prompt('Piper')

# Rosetta
run_rosetta_bool = True
#run_rosetta_bool = program_prompt('Rosetta')

# ZDOCK
run_zdock_bool = False
#run_zdock_bool = program_prompt('ZDOCK')

# Haddock
run_haddock_bool = True
#run_haddock_bool = program_prompt('Haddock')