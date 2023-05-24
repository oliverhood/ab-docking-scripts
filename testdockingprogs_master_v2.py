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
from testdockingprogs_master_lib_v2 import run_megadock, run_piper, run_rosetta, run_haddock

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

#*************************************************************************

# Get the base filename from the input file
inputfilename = os.path.basename(PDBfile).split('.')[0]
# Print starting docking
print(f"Starting docking program on {inputfilename}...", flush=True)
# Repeat docking 3 times on PDB file, different orientation each time
for i in range(3):
   # Get run number
   run = "Run " +str(i)
   # Print start of run to command line
   print(f"Starting {run}...")
   # Make new directory to put results in
   OUTPath_i = OUTPath + f"run{str(i)}/"
   # Make directory
   os.mkdir(OUTPath_i)

#*************************************************************************

   # New filename
   input_nohydrogens = f"{OUTPath_i}{inputfilename}_nohydrogens.pdb"
   # Strip hydrogens from input file
   subprocess.run([f"pdbhstrip {PDBfile} {input_nohydrogens}"], shell=True)

#*************************************************************************

   # Split input file into antibody/antigen components (using splitantibodyantigenchains.py)
   subprocess.run([f"~/ab-docking-scripts/splitantibodyantigenchains.py {input_nohydrogens} {OUTPath_i}"], shell=True)
   # Define input file no hydrogens filename
   nohydrogens_filename = f"{inputfilename}_nohydrogens"
   # Get the filenames for the split antibody/antigen chains
   ab_filename = OUTPath_i + "%s_ab.pdb" % nohydrogens_filename
   ag_filename = OUTPath_i + "%s_ag.pdb" % nohydrogens_filename

#*************************************************************************

   # MEGADOCK

   if run_megadock_bool:
       run_megadock(inputfilename, ab_filename, ag_filename, OUTPath_i)

#*************************************************************************

   # Piper

   if run_piper_bool:
       run_piper(input_nohydrogens, inputfilename, ab_filename, ag_filename, OUTPath_i)

#*************************************************************************

   # Rosetta

   if run_rosetta_bool:
       run_rosetta(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i)

#*************************************************************************

   # Haddock

   if run_haddock_bool:
       run_haddock(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults, Ha_all, Ha_ca,
                   Ha_res_pairs, Ha_ab_res, Ha_ag_res, Hw_all, Hw_ca, Hw_res_pairs, Hw_ab_res, Hw_ag_res)

#*************************************************************************

   # Indicate end of run
   dockingresults += [f"***** End of Run {str(i)} *****"]
   # Spacer
   dockingresults += [" "]
   # Indicate end of run
   print(f"{run} complete.")
