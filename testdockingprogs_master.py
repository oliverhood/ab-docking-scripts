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
from dockingtools_lib import evaluate_results, getlowestscore, gethighestscore, getnumberhits, writefile

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

# Repeat docking 3 times on PDB file, different orientation each time
for i in range(3):
   # Get run number
   run = "Run " +str(i)
   # Make new directory to put results in
   OUTPath_i = OUTPath + f"run{str(i)}/"
   # Make directory
   os.mkdir(OUTPath_i)

#*************************************************************************

   # Split input file into antibody/antigen components (using splitantibodyantigenchains.py)
   subprocess.run([f"~/ab-docking-scripts/splitantibodyantigenchains.py {PDBfile} {OUTPath}"], shell=True)
   # Get the base filename from the input file
   inputfilename = os.path.basename(PDBfile).split('.')[0]
   # Get the filenames for the split antibody/antigen chains
   ab_filename = OUTPath + "%s_ab.pdb" % inputfilename
   ag_filename = OUTPath + "%s_ag.pdb" % inputfilename

#*************************************************************************

   # MEGADOCK

   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())
   # Name docking method for results file
   method = "Megadock-4.1.1 | CPU Single Node | ZRANK Ranked Output | " + current_time
   # Add method title to docking results
   dockingresults += [method]

   # Run Megadockranked on unblocked antibody/antigen files
   subprocess.run(["~/ab-docking-scripts/runmegadockranked.py " + ab_filename + " " + ag_filename + " " + OUTPath_i], shell=True)

   # Define output filename
   megadock_resultfile = OUTPath_i + inputfilename + "_MegadockRanked_result.pdb"

   # Evaluate Docking Result
   results = evaluate_results(PDBfile, megadock_resultfile)

   # Get result scores, add to dockingresults, list of results
   dockingresults += ["Scores:"]
   dockingresults += ["======="]
   # All atoms RMSD
   all_atoms = results[0]
   dockingresults += [all_atoms]
   # CA atoms RMSD
   CA_atoms = results[1]
   dockingresults += [CA_atoms]
   # Header for proportion results
   dockingresults += ["Proportion of correctly predicted interface residues (0-1):"]
   # Proportion of residue contact pairs
   res_pairs = results[2]
   dockingresults += [res_pairs]
   # Proportion of ab interface residues
   ab_res = results[3]
   dockingresults += [ab_res]
   # Proportion of ag interface residues
   ag_res = results[4]
   dockingresults += [ag_res]

   # Get floats from result lines
   # all_atoms RMSD
   all_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", all_atoms)
   # CA atoms RMSD
   CA_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", CA_atoms)
   # Residue pairs
   res_pairs_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", res_pairs)
   # Ab residues
   ab_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ab_res)
   # Ag residues
   ag_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ag_res)

   # Add floats to summary lists
   for item in all_atoms_float:
      MD_all += [float(item)]
   for item in CA_atoms_float:
      MD_ca += [float(item)]
   for item in res_pairs_float:
      MD_res_pairs += [float(item)]
   for item in ab_res_float:
      MD_ab_res += [float(item)]
   for item in ag_res_float:
      MD_ag_res += [float(item)]

#*************************************************************************

   # Piper

   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())
   # Name docking method for results file
   method = "Piper 2.0.0 | " + current_time
   # Add method title to docking results
   dockingresults += [method]

   # Run piper
   subprocess.run([f"~/ab-docking-scripts/runpiper.py {ab_filename} {ag_filename} {OUTPath_i}"], shell=True)

   # Define output filename
   piper_resultfile = OUTPath_i + inputfilename + "_Piper_result.pdb"

   # Evaluate docking result
   results = evaluate_results(PDBfile, piper_resultfile)

   # Get result scores, add to dockingresults, list of results
   dockingresults += ["Scores:"]
   dockingresults += ["======="]
   # All atoms RMSD
   all_atoms = results[0]
   dockingresults += [all_atoms]
   # CA atoms RMSD
   CA_atoms = results[1]
   dockingresults += [CA_atoms]
   # Header for proportion results
   dockingresults += ["Proportion of correctly predicted interface residues (0-1):"]
   # Proportion of residue contact pairs
   res_pairs = results[2]
   dockingresults += [res_pairs]
   # Proportion of ab interface residues
   ab_res = results[3]
   dockingresults += [ab_res]
   # Proportion of ag interface residues
   ag_res = results[4]
   dockingresults += [ag_res]

   # Get floats from result lines
   # all_atoms RMSD
   all_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", all_atoms)
   # CA atoms RMSD
   CA_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", CA_atoms)
   # Residue pairs
   res_pairs_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", res_pairs)
   # Ab residues
   ab_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ab_res)
   # Ag residues
   ag_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ag_res)

   # Add floats to summary lists
   for item in all_atoms_float:
      Piper_all += [float(item)]
   for item in CA_atoms_float:
      Piper_ca += [float(item)]
   for item in res_pairs_float:
      Piper_res_pairs += [float(item)]
   for item in ab_res_float:
      Piper_ab_res += [float(item)]
   for item in ag_res_float:
      Piper_ag_res += [float(item)]

#*************************************************************************

   # Rosetta
   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())
   # Name docking method for results file
   method = f"Rosetta 3.13 | docking_prepack_protocol.default.linuxgccrelease | docking_protocol.default.linuxgccrelease | Best I_sc score | " + current_time
   # Add method title to docking results
   dockingresults += [method]

   # Run Rosetta on input files (performing 50 runs within the program)
   subprocess.run([f"~/ab-docking-scripts/runrosetta.py {PDBfile} {ab_filename} {ag_filename} 50 {OUTPath_i}"], shell=True)

   # Define output filename
   rosetta_resultfile = OUTPath_i + inputfilename + "_Rosetta_result.pdb"

   # Evaluate Docking Result
   results = evaluate_results(PDBfile, rosetta_resultfile)

   # Get result scores, add to dockingresults, list of results
   dockingresults += ["Scores:"]
   dockingresults += ["======="]
   # All atoms RMSD
   all_atoms = results[0]
   dockingresults += [all_atoms]
   # CA atoms RMSD
   CA_atoms = results[1]
   dockingresults += [CA_atoms]
   # Header for proportion results
   dockingresults += ["Proportion of correctly predicted interface residues (0-1):"]
   # Proportion of residue contact pairs
   res_pairs = results[2]
   dockingresults += [res_pairs]
   # Proportion of ab interface residues
   ab_res = results[3]
   dockingresults += [ab_res]
   # Proportion of ag interface residues
   ag_res = results[4]
   dockingresults += [ag_res]

   # Get floats from result lines
   # all_atoms RMSD
   all_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", all_atoms)
   # CA atoms RMSD
   CA_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", CA_atoms)
   # Residue pairs
   res_pairs_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", res_pairs)
   # Ab residues
   ab_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ab_res)
   # Ag residues
   ag_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ag_res)

   # Add floats to summary lists
   for item in all_atoms_float:
      Rosetta_all += [float(item)]
   for item in CA_atoms_float:
      Rosetta_ca += [float(item)]
   for item in res_pairs_float:
      Rosetta_res_pairs += [float(item)]
   for item in ab_res_float:
      Rosetta_ab_res += [float(item)]
   for item in ag_res_float:
      Rosetta_ag_res += [float(item)]

#*************************************************************************

   # Indicate end of run
   dockingresults += [f"***** End of Run {str(i)} *****"]

#*************************************************************************

# Calculate average scores, best result etc from lists of results

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

#*************************************************************************

# Define results file name
results_file = f"{OUTPath}{inputfilename}_dockingresults_{current_date_f2}"
# Write results file
writefile(results_file, dockingresults)

with open(results_file, "w") as file:
   for line in dockingresults:
       file.write("%s\n" % line)

#*************************************************************************