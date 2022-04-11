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

# ZDOCK
ZDOCK_all = []
ZDOCK_ca = []
ZDOCK_res_pairs = []
ZDOCK_ab_res = []
ZDOCK_ag_res = []

# Haddock Waters
Hw_all = []
Hw_ca = []
Hw_res_pairs = []
Hw_ab_res = []
Hw_ag_res = []

# Haddock nowaters
Ha_all = []
Ha_ca = []
Ha_res_pairs = []
Ha_ab_res = []
Ha_ag_res = []

#*************************************************************************

# Prompt user for programs to run

# Megadock
run_megadock_bool = False
#run_megadock_bool = program_prompt('Megadock')

# Piper
run_piper_bool = False
#run_piper_bool = program_prompt('Piper')

# Rosetta
run_rosetta_bool = False
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
      run_megadock(input_nohydrogens, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults, MD_all, MD_ca, MD_res_pairs, MD_ab_res, MD_ag_res)

#*************************************************************************

   # Piper

   if run_piper_bool:
      run_piper(input_nohydrogens, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults, Piper_all, Piper_ca, Piper_res_pairs, Piper_ab_res, Piper_ag_res)

#*************************************************************************

   # Rosetta

   if run_rosetta_bool:
      run_rosetta(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults, Rosetta_all, Rosetta_ca, Rosetta_res_pairs, Rosetta_ab_res, Rosetta_ag_res)

#*************************************************************************

   # ZDOCK

   if run_zdock_bool:
      run_zdock(input_nohydrogens, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults, ZDOCK_all, ZDOCK_ca, ZDOCK_res_pairs, ZDOCK_ab_res, ZDOCK_ag_res)

#*************************************************************************

   # Haddock

   if run_haddock_bool:
      run_haddock(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults, Ha_all, Ha_ca, Ha_res_pairs, Ha_ab_res, Ha_ag_res, Hw_all, Hw_ca, Hw_res_pairs, Hw_ab_res, Hw_ag_res)

#*************************************************************************

   # Indicate end of run
   dockingresults += [f"***** End of Run {str(i)} *****"]
   # Spacer
   dockingresults += [" "]
   # Indicate end of run
   print(f"{run} complete.")

#*************************************************************************

# Calculate average scores, best result etc from lists of results
print("Calculating results...", end='', flush=True)

# Add header to results file
dockingresults += ["Summary Evalutation Metrics"]
dockingresults += ["==========================="]

# List scoring metrics
scores_all = [MD_all, MD_ca, MD_res_pairs, MD_ab_res, MD_ag_res,
Piper_all, Piper_ca, Piper_res_pairs, Piper_ab_res, Piper_ag_res, Rosetta_all, Rosetta_ca, Rosetta_res_pairs, Rosetta_ab_res, Rosetta_ag_res
, ZDOCK_all, ZDOCK_ca, ZDOCK_res_pairs, ZDOCK_ab_res, ZDOCK_ag_res, Hw_all, Hw_ca, Hw_res_pairs, Hw_ab_res, Hw_ag_res, Ha_all, Ha_ca, Ha_res_pairs, Ha_ab_res, Ha_ag_res]

# Write results to individual files (see if this works, something else is going wrong below)

# Write results directory
subprocess.run([f"mkdir {directory}/results"], shell=True)

# Megadock
if run_megadock_bool:

   MD_all_out = f"{directory}/results/{inputfilename}_MD_all.txt"
   MD_ca_out = f"{directory}/results/{inputfilename}_MD_ca.txt"
   MD_res_pairs_out = f"{directory}/results/{inputfilename}_MD_res_pairs.txt"
   MD_ab_res_out = f"{directory}/results/{inputfilename}_MD_ab_res.txt"
   MD_ag_res_out = f"{directory}/results/{inputfilename}_MD_ag_res.txt"

   # MD_all
   with open(MD_all_out, "w") as file:
      for line in MD_all:
         file.write(f"{line} /n")

   # MD_ca
   with open(MD_ca_out, "w") as file:
      for line in MD_ca:
         file.write(f"{line} /n")

   # MD_res_pairs
   with open(MD_res_pairs_out, "w") as file:
      for line in MD_res_pairs:
         file.write(f"{line} /n")

   # MD_ab_res
   with open(MD_ab_res_out, "w") as file:
      for line in MD_ab_res:
         file.write(f"{line} /n")

   # MD_ag_res
   with open(MD_ag_res_out, "w") as file:
      for line in MD_ag_res:
         file.write(f"{line} /n")

# Piper
if run_piper_bool:

   Piper_all_out = f"{directory}/results/{inputfilename}_Piper_all.txt"
   Piper_ca_out = f"{directory}/results/{inputfilename}_Piper_ca.txt"
   Piper_res_pairs_out = f"{directory}/results/{inputfilename}_Piper_res_pairs.txt"
   Piper_ab_res_out = f"{directory}/results/{inputfilename}_Piper_ab_res.txt"
   Piper_ag_res_out = f"{directory}/results/{inputfilename}_Piper_ag_res.txt"

   # Piper_all
   with open(Piper_all_out, "w") as file:
      for line in Piper_all:
         file.write(f"{line} /n")

   # Piper_ca
   with open(Piper_ca_out, "w") as file:
      for line in Piper_ca:
         file.write(f"{line} /n")

   # Piper_res_pairs
   with open(Piper_res_pairs_out, "w") as file:
      for line in Piper_res_pairs:
         file.write(f"{line} /n")

   # Piper_ab_res
   with open(Piper_ab_res_out, "w") as file:
      for line in Piper_ab_res:
         file.write(f"{line} /n")

   # MD_ag_res
   with open(Piper_ag_res_out, "w") as file:
      for line in Piper_ag_res:
         file.write(f"{line} /n")


# Rosetta
if run_rosetta_bool:

   Rosetta_all_out = f"{directory}/results/{inputfilename}_Rosetta_all.txt"
   Rosetta_ca_out = f"{directory}/results/{inputfilename}_Rosetta_ca.txt"
   Rosetta_res_pairs_out = f"{directory}/results/{inputfilename}_Rosetta_res_pairs.txt"
   Rosetta_ab_res_out = f"{directory}/results/{inputfilename}_Rosetta_ab_res.txt"
   Rosetta_ag_res_out = f"{directory}/results/{inputfilename}_Rosetta_ag_res.txt"

   # Rosetta_all
   with open(Rosetta_all_out, "w") as file:
      for line in Rosetta_all:
         file.write(f"{line} /n")

   # Rosetta_ca
   with open(Rosetta_ca_out, "w") as file:
      for line in Rosetta_ca:
         file.write(f"{line} /n")

   # Rosetta_res_pairs
   with open(Rosetta_res_pairs_out, "w") as file:
      for line in Rosetta_res_pairs:
         file.write(f"{line} /n")

   # Rosetta_ab_res
   with open(Rosetta_ab_res_out, "w") as file:
      for line in Rosetta_ab_res:
         file.write(f"{line} /n")

   # Rosetta_ag_res
   with open(Rosetta_ag_res_out, "w") as file:
      for line in Rosetta_ag_res:
         file.write(f"{line} /n")


# ZDOCK
if run_zdock_bool:

   ZDOCK_all_out = f"{directory}/results/{inputfilename}_ZDOCK_all.txt"
   ZDOCK_ca_out = f"{directory}/results/{inputfilename}_ZDOCK_ca.txt"
   ZDOCK_res_pairs_out = f"{directory}/results/{inputfilename}_ZDOCK_res_pairs.txt"
   ZDOCK_ab_res_out = f"{directory}/results/{inputfilename}_ZDOCK_ab_res.txt"
   ZDOCK_ag_res_out = f"{directory}/results/{inputfilename}_ZDOCK_ag_res.txt"

   # ZDOCK_all
   with open(ZDOCK_all_out, "w") as file:
      for line in ZDOCK_all:
         file.write(f"{line} /n")

   # ZDOCK_ca
   with open(ZDOCK_ca_out, "w") as file:
      for line in ZDOCK_ca:
         file.write(f"{line} /n")

   # ZDOCK_res_pairs
   with open(ZDOCK_res_pairs_out, "w") as file:
      for line in ZDOCK_res_pairs:
         file.write(f"{line} /n")

   # ZDOCK_ab_res
   with open(ZDOCK_ab_res_out, "w") as file:
      for line in ZDOCK_ab_res:
         file.write(f"{line} /n")

   # ZDOCK_ag_res
   with open(ZDOCK_ag_res_out, "w") as file:
      for line in ZDOCK_ag_res:
         file.write(f"{line} /n")


# Haddock waters
if run_haddock_bool:

   Hw_all_out = f"{directory}/results/{inputfilename}_Hw_all.txt"
   Hw_ca_out = f"{directory}/results/{inputfilename}_Hw_ca.txt"
   Hw_res_pairs_out = f"{directory}/results/{inputfilename}_Hw_res_pairs.txt"
   Hw_ab_res_out = f"{directory}/results/{inputfilename}_Hw_ab_res.txt"
   Hw_ag_res_out = f"{directory}/results/{inputfilename}_Hw_ag_res.txt"

   # Hw_all
   with open(Hw_all_out, "w") as file:
      for line in Hw_all:
         file.write(f"{line} /n")

   # Hw_ca
   with open(Hw_ca_out, "w") as file:
      for line in Hw_ca:
         file.write(f"{line} /n")

   # Hw_res_pairs
   with open(Hw_res_pairs_out, "w") as file:
      for line in Hw_res_pairs:
         file.write(f"{line} /n")

   # Hw_ab_res
   with open(Hw_ab_res_out, "w") as file:
      for line in Hw_ab_res:
         file.write(f"{line} /n")

   # Hw_ag_res
   with open(Hw_ag_res_out, "w") as file:
      for line in Hw_ag_res:
         file.write(f"{line} /n")


# Haddock no waters
if run_haddock_bool:

   Ha_all_out = f"{directory}/results/{inputfilename}_Ha_all.txt"
   Ha_ca_out = f"{directory}/results/{inputfilename}_Ha_ca.txt"
   Ha_res_pairs_out = f"{directory}/results/{inputfilename}_Ha_res_pairs.txt"
   Ha_ab_res_out = f"{directory}/results/{inputfilename}_Ha_ab_res.txt"
   Ha_ag_res_out = f"{directory}/results/{inputfilename}_Ha_ag_res.txt"

   # Ha_all
   with open(Ha_all_out, "w") as file:
      for line in Ha_all:
         file.write(f"{line} /n")

   # Ha_ca
   with open(Ha_ca_out, "w") as file:
      for line in Ha_ca:
         file.write(f"{line} /n")

   # Ha_res_pairs
   with open(Ha_res_pairs_out, "w") as file:
      for line in Ha_res_pairs:
         file.write(f"{line} /n")

   # Ha_ab_res
   with open(Ha_ab_res_out, "w") as file:
      for line in Ha_ab_res:
         file.write(f"{line} /n")

   # Ha_ag_res
   with open(Ha_ag_res_out, "w") as file:
      for line in Ha_ag_res:
         file.write(f"{line} /n")

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
zdock_name = "ZDOCK | ZRANK Ranked Output"
haddock_waters_name = "Haddock2.4 | Protein-Protein | Waters "
haddock_nowaters_name = "Haddock2.4 | Protein-Protein | No Waters"

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

# ZDOCK
dockingresults += [zdock_name]
# Average RMSD
dockingresults += [f"Average RMSD", "All atoms:   " + str(avg_scores[15]), "CA atoms:   " + str(avg_scores[16])]
# Best RMSD
dockingresults += ["Best Score", "All atoms:   " + str(lowest_scores[15]), "CA atoms:   " + str(lowest_scores[16])]
# Number of good hits
dockingresults += ["Number of good hits (<3.0 RMSD):   " + str(num_hits[15])]
# Header for average proportion values
dockingresults += ["Average percentage of correctly predicted interface residues"]
# Avg. proportion of res-pairs
dockingresults += ["Residue pair predictions:   " + str(avg_scores[17])]
# Avg. antibody residues
dockingresults += ["Antibody residue predictions:   " + str(avg_scores[18])]
# Avg. antigen residues
dockingresults += ["Antigen residue predictions:   " + str(avg_scores[19])]
dockingresults += [" "]

# Haddock Waters
dockingresults += [haddock_waters_name]
# Average RMSD
dockingresults += [f"Average RMSD", "All atoms:   " + str(avg_scores[20]), "CA atoms:   " + str(avg_scores[21])]
# Best RMSD
dockingresults += ["Best Score", "All atoms:   " + str(lowest_scores[20]), "CA atoms:   " + str(lowest_scores[21])]
# Number of good hits
dockingresults += ["Number of good hits (<3.0 RMSD):   " + str(num_hits[20])]
# Header for average proportion values
dockingresults += ["Average percentage of correctly predicted interface residues"]
# Avg. proportion of res-pairs
dockingresults += ["Residue pair predictions:   " + str(avg_scores[22])]
# Avg. antibody residues
dockingresults += ["Antibody residue predictions:   " + str(avg_scores[23])]
# Avg. antigen residues
dockingresults += ["Antigen residue predictions:   " + str(avg_scores[24])]
dockingresults += [" "]

# Haddock Waters
dockingresults += [haddock_nowaters_name]
# Average RMSD
dockingresults += [f"Average RMSD", "All atoms:   " + str(avg_scores[25]), "CA atoms:   " + str(avg_scores[26])]
# Best RMSD
dockingresults += ["Best Score", "All atoms:   " + str(lowest_scores[25]), "CA atoms:   " + str(lowest_scores[26])]
# Number of good hits
dockingresults += ["Number of good hits (<3.0 RMSD):   " + str(num_hits[25])]
# Header for average proportion values
dockingresults += ["Average percentage of correctly predicted interface residues"]
# Avg. proportion of res-pairs
dockingresults += ["Residue pair predictions:   " + str(avg_scores[27])]
# Avg. antibody residues
dockingresults += ["Antibody residue predictions:   " + str(avg_scores[28])]
# Avg. antigen residues
dockingresults += ["Antigen residue predictions:   " + str(avg_scores[29])]
dockingresults += [" "]

# Finish calculating results
print("Done")

#*************************************************************************
# writing results...
print("Writing results file...", end='', flush=True)
# Define results file name
results_file = f"{OUTPath}{inputfilename}_dockingresults_{current_date_f2}.results.txt"
# Write results file
writefile(results_file, dockingresults)

# Run complete
print("Done")
print(f"Docking run on {inputfilename} complete.")

#*************************************************************************