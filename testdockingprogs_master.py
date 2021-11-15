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

#*************************************************************************

# Specify input file
PDBfile = sys.argv[1]

# Get output path from command line (if present)
OUTPath = './'
try:
   OUTPath = sys.argv[4] + '/'
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
Dag_filename = "%s_Dag.pdb" % filename

#*************************************************************************

# Run Megadock-4.1.1
subprocess.run(["~/ab-docking-scripts/runmegadock.py " + ab_filename + " " + ag_filename + " " + OUTPath], shell=True)

# Evaluate docking result
subprocess.run(["~/ab-docking-scripts/runprofit.py " + PDBfile + " " + ab_filename + " " + Dag_filename + " " + OUTPath], shell=True)

