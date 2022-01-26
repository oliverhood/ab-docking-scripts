#!/usr/bin/env python3
"""
Program: testdockingprogs_master
File:    testdockingprogs_master.py

Version:  V1.0
Date:     12.11.21
Function: Split input file into its antibody/antigen components for input into docking algorithms, run docking algorithm then evaluate the result using ProFit.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody/antigen complex as input, splits the file into its component chains, runs these chains through a docking algorithm, then evaluates the result using the ProFit program. The docking and evaluation steps are repeated for each docking algorithm specified.

--------------------------------------------------------------------------

Usage:
======
testdockingprogs_master.py PDBFile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   12.11.21   Original   By: OECH

"""

#*************************************************************************

# Import Libraries
import sys, os, subprocess, time, re, statistics
from threading import Timer
from dockingtools_lib import evaluate_results, getlowestscore, gethighestscore, getnumberhits, writefile, getantigenchainid
from testdockingprogs_master_lib import run_megadock, run_piper, run_rosetta, program_prompt

#*************************************************************************

# Specify input file
PDBfile = sys.argv[1]

# Get output path from command line (if present)
OUTPath = './'
try:
   OUTPath = sys.argv[2] + '/'
except IndexError:
   print('No output directory specified, writing files to current directory')
   OUTPath = './'

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

# Collect method scores to get averages etc

# Megadock
MD_all = []
MD_ca = []
MD_res_pairs = []
MD_ab_res = []
MD_ag_res = []

# Piper
Piper_all = []
Piper_ca = []
Piper_res_pairs = []
Piper_ab_res = []
Piper_ag_res = []

# Rosetta
Rosetta_all = []
Rosetta_ca = []
Rosetta_res_pairs = []
Rosetta_ab_res = []
Rosetta_ag_res = []

#*************************************************************************

# Prompt user for programs to run

# Megadock
run_megadock_bool = True
#run_megadock_bool = program_prompt('Megadock')

# Piper
run_piper_bool = True
#run_piper_bool = program_prompt('Piper')

# Rosetta
run_rosetta_bool = True
#run_rosetta_bool = program_prompt('Rosetta')

#*************************************************************************

# Get the base filename from the input file
inputfilename = os.path.basename(PDBfile).split('.')[0]
# Print starting docking
print(f"Starting docking program on {inputfilename}...")
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

   # Split input file into antibody/antigen components (using splitantibodyantigenchains.py)
   subprocess.run([f"~/ab-docking-scripts/splitantibodyantigenchains.py {PDBfile} {OUTPath_i}"], shell=True)
   # Get the filenames for the split antibody/antigen chains
   ab_filename = OUTPath_i + "%s_ab.pdb" % inputfilename
   ag_filename = OUTPath_i + "%s_ag.pdb" % inputfilename

#*************************************************************************

   # MEGADOCK
   
   if run_megadock_bool:
      run_megadock(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults)

#*************************************************************************

   # Piper

   if run_piper_bool:
      run_piper(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults)

#*************************************************************************

   # Rosetta

   if run_rosetta_bool:
      run_rosetta(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults)

#*************************************************************************

   # Indicate end of run
   dockingresults += [f"***** End of Run {str(i)} *****"]
   # Spacer
   dockingresults += [" "]
   # Indicate end of run
   print(f"{run} complete.")

#*************************************************************************

# Calculate average scores, best result etc from lists of results
print("Calculating results...", end='')

# Add header to results file
dockingresults += ["Summary Evalutation Metrics"]
dockingresults += ["==========================="]

# List scoring metrics
scores_all = [MD_all, MD_ca, MD_res_pairs, MD_ab_res, MD_ag_res,
Piper_all, Piper_ca, Piper_res_pairs, Piper_ab_res, Piper_ag_res, Rosetta_all, Rosetta_ca, Rosetta_res_pairs, Rosetta_ab_res, Rosetta_ag_res
]

# Calculate scores for each method
avg_scores = []
lowest_scores = []
highest_scores = []
num_hits = []
for item in (scores_all):
   avg_scores += [statistics.mean(item)]
   lowest_scores += [getlowestscore(item)]
   highest_scores += [gethighestscore(item)]
   num_hits += [getnumberhits(item)]

# Write scores to dockingresults
# Method names
megadock_name = "Megadock-4.1.1 | CPU Single Node | ZRANK Ranked Output"
piper_name = "Piper 2.0.0"
rosetta_name = "Rosetta 3.13 | docking_prepack_protocol.default.linuxgccrelease | docking_protocol.default.linuxgccrelease | Best I_sc score"

# Megadock
dockingresults += [megadock_name]
# Average RMSD
dockingresults += [f"Average RMSD", "All atoms:   " + str(avg_scores[0]), "CA atoms:   " + str(avg_scores[1])]
# Best RMSD
dockingresults += ["Best Score", "All atoms:   " + str(lowest_scores[0]), "CA atoms:   " + str(lowest_scores[1])]
# Number of good hits
dockingresults += ["Number of good hits (<3.0 RMSD):   " + str(num_hits[0])]
# Header for average proportion values
dockingresults += ["Average percentage of correctly predicted interface residues"]
# Avg. proportion of res-pairs
dockingresults += ["Residue pair predictions:   " + str(avg_scores[2])]
# Avg. antibody residues
dockingresults += ["Antibody residue predictions:   " + str(avg_scores[3])]
# Avg. antigen residues
dockingresults += ["Antigen residue predictions:   " + str(avg_scores[4])]
dockingresults += [" "]

# Piper
dockingresults += [piper_name]
# Average RMSD
dockingresults += [f"Average RMSD", "All atoms:   " + str(avg_scores[5]), "CA atoms:   " + str(avg_scores[6])]
# Best RMSD
dockingresults += ["Best Score", "All atoms:   " + str(lowest_scores[5]), "CA atoms:   " + str(lowest_scores[6])]
# Number of good hits
dockingresults += ["Number of good hits (<3.0 RMSD):   " + str(num_hits[5])]
# Header for average proportion values
dockingresults += ["Average percentage of correctly predicted interface residues"]
# Avg. proportion of res-pairs
dockingresults += ["Residue pair predictions:   " + str(avg_scores[7])]
# Avg. antibody residues
dockingresults += ["Antibody residue predictions:   " + str(avg_scores[8])]
# Avg. antigen residues
dockingresults += ["Antigen residue predictions:   " + str(avg_scores[9])]
dockingresults += [" "]

# Rosetta
dockingresults += [rosetta_name]
# Average RMSD
dockingresults += [f"Average RMSD", "All atoms:   " + str(avg_scores[10]), "CA atoms:   " + str(avg_scores[11])]
# Best RMSD
dockingresults += ["Best Score", "All atoms:   " + str(lowest_scores[10]), "CA atoms:   " + str(lowest_scores[11])]
# Number of good hits
dockingresults += ["Number of good hits (<3.0 RMSD):   " + str(num_hits[10])]
# Header for average proportion values
dockingresults += ["Average percentage of correctly predicted interface residues"]
# Avg. proportion of res-pairs
dockingresults += ["Residue pair predictions:   " + str(avg_scores[12])]
# Avg. antibody residues
dockingresults += ["Antibody residue predictions:   " + str(avg_scores[13])]
# Avg. antigen residues
dockingresults += ["Antigen residue predictions:   " + str(avg_scores[14])]
dockingresults += [" "]

# Finish calculating results
print("Done")

#*************************************************************************
# writing results...
print("Writing results file...", end='')
# Define results file name
results_file = f"{OUTPath}{inputfilename}_dockingresults_{current_date_f2}.results.txt"
# Write results file
writefile(results_file, dockingresults)

# Run complete
print("Done")
print(f"Docking run on {inputfilename} complete.")

#*************************************************************************