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
import sys
import os
import subprocess
from datetime import date

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

# Split input file into antibody/antigen components (using splitantibodyantigenchains.py)
subprocess.run(["~/ab-docking-scripts/splitantibodyantigenchains.py " + PDBfile + " " + OUTPath], shell=True)
# Get the base filename from the input file
filename = os.path.basename(PDBfile).split('.')[0]
# Get the filenames for the split antibody/antigen chains
ab_filename = OUTPath + "%s_ab.pdb" % filename
ag_filename = OUTPath + "%s_ag.pdb" % filename
# Define filename for the docked antigen
Dag_filename = OUTPath + "%s_Dag.pdb" % filename

#*************************************************************************

# Get today's date
today = date.today()
todaydot = today.strftime("%d.%m.%Y")
today_ = today.strftime("%d_%m_%Y")
# Create Results file header
header = "Docking test using " + PDBfile + " " + todaydot
# Create list starting with results file header
dockingresults = [header]

#*************************************************************************

# Name docking method for results file
method = "Megadock-4.1.1 CPU Single Node"
# Run Megadock-4.1.1
subprocess.run(["~/ab-docking-scripts/runmegadock.py " + ab_filename + " " + ag_filename + " " + OUTPath], shell=True)

# Evaluate docking result
output=subprocess.check_output(["~/ab-docking-scripts/runprofit.py " + PDBfile + " " + ab_filename + " " + Dag_filename + " " + OUTPath], shell=True)
output = str(output, 'utf-8')
# Extract the result lines from output
contents = output.split('\n')
all_atoms = contents[1]
CA_atoms = contents[2]
# Add lines to results file
dockingresults += [method]
dockingresults += [all_atoms]
dockingresults += [CA_atoms]

#*************************************************************************

# Write results file
results_file = open(str(OUTPath + filename + "_" + "dockingresults_" + today_), "w")
for line in dockingresults:
   results_file.write(line)
results_file.close()

#*************************************************************************

# Remove _ab and _ag files
subprocess.run(["rm " + ab_filename + " " + ag_filename], shell=True)