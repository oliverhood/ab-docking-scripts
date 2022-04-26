#!/usr/bin/env python3
"""
Program: testmegadock_vs_megadockblocked
File:    testmegadock_vs_megadockblocked.py

Version:  V1.0
Date:     18.11.21
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
V1.0   18.11.21   Original   By: OECH
V1.1   20.11.21   Change to block antigen residues   By: OECH

"""

#*************************************************************************

# Import Libraries
import sys
import os
import subprocess
import time
import re
import statistics

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
# Collect method scores to get average scores etc
MEGADOCK_all = []
MEGADOCK_ca = []
BLOCKED_all = []
BLOCKED_ca = []
RANKED_all = []
RANKED_ca = []
BLOCKED_RANKED_all = []
BLOCKED_RANKED_ca = []

#*************************************************************************

# For loop to run megadock and megadock_blocked 50 times
for i in range(2):
   # Give run number
   run = "Run " + str(i)
   dockingresults += ["", run]

#*************************************************************************

   # Make new directory to put results in
   OUTPath_i = OUTPath + "run" + str(i) + "/"
   #Make directory
   subprocess.run(["mkdir " + OUTPath_i], shell=True)
   # Split input file into antibody/antigen components (using splitantibodyantigenchains.py)
   subprocess.run(["~/ab-docking-scripts/splitantibodyantigenchains.py " + PDBfile + " " + OUTPath_i], shell=True)
   # Get the base filename from the input file
   filename = os.path.basename(PDBfile).split('.')[0]
   # Get the filenames for the split antibody/antigen chains
   ab_filename = OUTPath_i + "%s_ab.pdb" % filename
   ag_filename = OUTPath_i + "%s_ag.pdb" % filename
   # Define filename for the docked antigen
   Dag_filename = OUTPath_i + "%s_Dag.pdb" % filename

#*************************************************************************
   # MEGADOCK

   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())
   # Name docking method for results file
   method = "Megadock-4.1.1 | CPU Single Node | " + current_time
   # Run Megadock-4.1.1
   subprocess.run(["~/ab-docking-scripts/runmegadock.py " + ab_filename + " " + ag_filename + " " + OUTPath_i], shell=True)

   # Evaluate docking result
   output=subprocess.check_output(["~/ab-docking-scripts/runprofit.py " + PDBfile + " " + ab_filename + " " + Dag_filename + " " + OUTPath_i], shell=True)
   output = str(output, 'utf-8')
   # Extract the result lines from output
   contents = output.split('\n')
   all_atoms = contents[0]
   CA_atoms = contents[1]
   # Add lines to results file
   dockingresults += [method]
   dockingresults += [all_atoms]
   dockingresults += [CA_atoms]
   # Add spacer line before next method
   dockingresults += " "
   # Get floats from result lines
   RMSD_all = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", all_atoms)
   RMSD_ca = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", CA_atoms)
   # Add floats to result lists
   for item in RMSD_all:
      MEGADOCK_all += [float(item)]
   for item in RMSD_ca:
      MEGADOCK_ca += [float(item)]

#*************************************************************************
   # MEGADOCK BLOCKED Antibody
   # Run blockNIres.py on split input files
   subprocess.run(["~/ab-docking-scripts/blockNIres.py " + PDBfile + " " + ab_filename + " " + ag_filename + " antibody " + OUTPath_i], shell=True)

   # Define filename for the blocked antibody file
   ab_blocked = OUTPath_i + "%s_ab_blocked.pdb" % filename

   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())
   # Name docking method for results file
   method = "Megadock-4.1.1 | CPU Single Node | Blocked Antibody | " + current_time
   # Run Megadock-4.1.1
   subprocess.run(["~/ab-docking-scripts/runmegadock.py " + ab_blocked + " " + ag_filename + " " + OUTPath_i], shell=True)

   # Change ab_filename to differentiate between megadock and megadock blocked files
   ab_b_filename = OUTPath_i + "%s_ab_" % filename + "b.pdb"
   # Copy ab file to new file ab_b.pdb
   subprocess.run(["cp " + ab_filename + " " + ab_b_filename], shell =True)
   # Evaluate docking result
   output=subprocess.check_output(["~/ab-docking-scripts/runprofit.py " + PDBfile + " " + ab_b_filename + " " + Dag_filename + " " + OUTPath_i], shell=True)
   output = str(output, 'utf-8')
   # Extract the result lines from output
   contents = output.split('\n')
   all_atoms = contents[0]
   CA_atoms = contents[1]
   # Add lines to results file
   dockingresults += [method]
   dockingresults += [all_atoms]
   dockingresults += [CA_atoms]
   # Add spacer line before next method
   dockingresults += " "
   # Get floats from result lines
   RMSD_all = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", all_atoms)
   RMSD_ca = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", CA_atoms)
   # Add floats to result lists
   for item in RMSD_all:
      BLOCKED_all += [float(item)]
   for item in RMSD_ca:
      BLOCKED_ca += [float(item)]

   #**********************************************************************

   # MEGADOCK BLOCKED Antigen
   # Run blockNIres.py on split input files
   #subprocess.run(["~/ab-docking-scripts/blockNIres.py " + PDBfile + " " + ab_filename + " " + ag_filename + " antigen " + OUTPath_i], shell=True)

   # Define filename for the blocked antigen file
   ##ag_blocked = OUTPath_i + "%s_ag_blocked.pdb" % filename
   # Change ab_filename to differentiate between megadock and megadock blocked files
   #ab_b1_filename = OUTPath_i + "%s_ab_" % filename + "b1.pdb"
   # Copy ab file to new file ab_b.pdb
   #subprocess.run(["cp " + ab_filename + " " + ab_b1_filename], shell =True)   

   # Get date and time that method is being run at
   #current_time = time.strftime(r"%d.%m.%Y   %H:%M:%S", time.localtime())
   # Name docking method for results file
   #method = "Megadock-4.1.1   CPU Single Node   Blocked Antigen   " + current_time
   # Run Megadock-4.1.1
   #subprocess.run(["~/ab-docking-scripts/runmegadock.py " + ab_filename + " " + ag_blocked + " " + OUTPath_i], shell=True)

   # Evaluate docking result
   #output=subprocess.check_output(["~/ab-docking-scripts/runprofit.py " + PDBfile + " " + ab_b1_filename + " " + Dag_filename + " " + OUTPath_i], shell=True)
   #output = str(output, 'utf-8')
   # Extract the result lines from output
   #contents = output.split('\n')
   #all_atoms = contents[0]
   #CA_atoms = contents[1]
   # Add lines to results file
   #dockingresults += [method]
   #dockingresults += [all_atoms]
   #dockingresults += [CA_atoms]
   # Add spacer line before next method
   #dockingresults += " "

#*************************************************************************
   # MEGADOCK RANKED

   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())
   # Name docking method for results file
   method = "Megadock-4.1.1 | CPU Single Node | ZRANK Ranked Output | " + current_time

   # Run Megadockranked on unblocked antibody/antigen files
   subprocess.run(["~/ab-docking-scripts/runmegadockranked.py " + ab_filename + " " + ag_filename + " " + OUTPath_i], shell=True)
   #Rename ab file so combined file output has new name
   ab_r_filename = OUTPath_i + "%s_ab_" % filename + "r.pdb"
   # Copy ab file to new file ab_r.pdb
   subprocess.run(["cp " + ab_filename + " " + ab_r_filename], shell =True) 
   # Define Dag output filename
   Dag_rank_filename = OUTPath_i + "%s_megadockranked_Dag.pdb" % filename

   # Evaluate docking result
   output=subprocess.check_output(["~/ab-docking-scripts/runprofit.py " + PDBfile + " " + ab_r_filename + " " + Dag_rank_filename + " " + OUTPath_i], shell=True)
   output = str(output, 'utf-8')
   # Extract the result lines from output
   contents = output.split('\n')
   all_atoms = contents[0]
   CA_atoms = contents[1]
   # Add lines to results file
   dockingresults += [method]
   dockingresults += [all_atoms]
   dockingresults += [CA_atoms]
   # Add spacer line before next method
   dockingresults += " "
   # Get floats from result lines
   RMSD_all = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", all_atoms)
   RMSD_ca = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", CA_atoms)
   # Add floats to result lists
   for item in RMSD_all:
      RANKED_all += [float(item)]
   for item in RMSD_ca:
      RANKED_ca += [float(item)]


#*************************************************************************
   # MEGADOCK blocked antibody + ZRank

    # Run blockNIres.py on split input files
   subprocess.run(["~/ab-docking-scripts/blockNIres.py " + PDBfile + " " + ab_filename + " " + ag_filename + " antibody " + OUTPath_i], shell=True)

   # Change ab_filename to differentiate between megadock and megadock blocked files
   ab_brank_filename = OUTPath_i + "%s_ab_" % filename + "blockedrank.pdb"
   # Copy ab file to new file ab_b.pdb
   subprocess.run(["cp " + ab_filename + " " + ab_brank_filename], shell =True) 

   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())
   # Name docking method for results file
   method = "Megadock-4.1.1 | CPU Single Node | Blocked Antibody | ZRANK Ranked Output | " + current_time
   # Run Megadock-4.1.1
   subprocess.run(["~/ab-docking-scripts/runmegadockranked.py " + ab_brank_filename + " " + ag_filename + " " + OUTPath_i], shell=True)

   
   # Evaluate docking result
   output=subprocess.check_output(["~/ab-docking-scripts/runprofit.py " + PDBfile + " " + ab_brank_filename + " " + Dag_filename + " " + OUTPath_i], shell=True)
   output = str(output, 'utf-8')
   # Extract the result lines from output
   contents = output.split('\n')
   all_atoms = contents[0]
   CA_atoms = contents[1]
   # Add lines to results file
   dockingresults += [method]
   dockingresults += [all_atoms]
   dockingresults += [CA_atoms]
   # Add spacer line before next method
   dockingresults += " "
   # Get floats from result lines
   RMSD_all = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", all_atoms)
   RMSD_ca = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", CA_atoms)
   # Add floats to result lists
   for item in RMSD_all:
      BLOCKED_RANKED_all += [float(item)]
   for item in RMSD_ca:
      BLOCKED_RANKED_ca += [float(item)]

#*************************************************************************

   # Indicate end of run
   dockingresults += ["**********"]

#*************************************************************************
# Calculate average scores, best result etc from lists of results
scores_all = [MEGADOCK_all, MEGADOCK_ca, BLOCKED_all, BLOCKED_ca, RANKED_all, RANKED_ca, BLOCKED_RANKED_all, BLOCKED_RANKED_ca]

# Function to get best (lowest) score from list
def getbestscore(list):
   bestscore = 10
   for item in list:
      if item < bestscore:
         bestscore = item
   return bestscore

# Function to get number of good (<3.0 RMSD) hits
def getnumberhits(list):
   hits = 0
   for item in list:
      if item < 3.0:
         hits +=1
   return hits

# Calculate scores for each method
avg_scores = []
best_scores = []
num_hits = []
for item in (scores_all):
   avg_scores += [statistics.mean(item)]
   best_scores += [getbestscore(item)]
   num_hits += [getnumberhits(item)]

# Write scores to dockingresults
# Define method names
Megadock_name = "Megadock-4.1.1 | CPU Single Node"
Blocked_name = "Megadock-4.1.1 | CPU Single Node | Blocked Antibody"
Ranked_name = "Megadock-4.1.1 | CPU Single Node | ZRANK Ranked Output"
Blocked_ranked_name = "Megadock-4.1.1 | CPU Single Node | Blocked Antibody | ZRANK Ranked Output"

# Write summary scores header
dockingresults += ["Summary Evaluation Metrics"]
dockingresults += ["=========================="]

# Write scores to dockingresults
# Megadock
dockingresults += [Megadock_name]
dockingresults += [f"Average RMSD", "All atoms:   " + str(avg_scores[0]), "CA atoms:   " + str(avg_scores[1])]
dockingresults += ["Best Score", "All atoms:   " + str(best_scores[0]), "CA atoms:   " + str(best_scores[1])]
dockingresults += ["Number of good hits (<3.0 RMSD)", str(num_hits[0])]
dockingresults += [" "]
# Megadock blocked
dockingresults += [Blocked_name]
dockingresults += ["Average RMSD", "All atoms:   " + str(avg_scores[2]), "CA atoms:   " + str(avg_scores[3])]
dockingresults += ["Best Score", "All atoms:   " + str(best_scores[2]), "CA atoms:   " + str(best_scores[3])]
dockingresults += ["Number of good hits (<3.0 RMSD)", str(num_hits[2])]
dockingresults += [" "]
# Megadock Ranked
dockingresults += [Ranked_name]
dockingresults += ["Average RMSD", "All atoms:   " + str(avg_scores[4]), "CA atoms:   " + str(avg_scores[5])]
dockingresults += ["Best Score", "All atoms:   " + str(best_scores[4]), "CA atoms:   " + str(best_scores[5])]
dockingresults += ["Number of good hits (<3.0 RMSD)", str(num_hits[4])]
dockingresults += [" "]
# Megadock blocked and ranked
dockingresults += [Blocked_ranked_name]
dockingresults += ["Average RMSD", "All atoms:   " + str(avg_scores[6]), "CA atoms:   " + str(avg_scores[7])]
dockingresults += ["Best Score", "All atoms:   " + str(best_scores[6]), "CA atoms:   " + str(best_scores[7])]
dockingresults += ["Number of good hits (<3.0 RMSD):", str(num_hits[6])]
dockingresults += [" "]


#*************************************************************************

# Write results file
results_file = open(str(OUTPath + filename + "_" + "dockingresults_" + current_date_f2), "w")
for line in dockingresults:
   results_file.write("%s\n" % line)
results_file.close()

#*************************************************************************

# Remove _ab, _ag, _Dag files, _ab_blocked, and ab_b files
subprocess.run(["rm " + ab_filename + " " + ag_filename + " " + Dag_filename + " " + ab_blocked + " " + ab_b_filename], shell=True)