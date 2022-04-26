#!/usr/bin/env python3
"""
Program: analyse_antigens
File:    analyse_antigens.py

Version:  V1.0
Date:     17.02.2022
Function: Perform analysis on antigens to determine whether there is a conformational change upon antibody binding.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============


--------------------------------------------------------------------------

Usage:
======

--------------------------------------------------------------------------

Revision History:
=================
V1.0   15.02.22   Original   By: OECH

"""

#*************************************************************************

# Import Libraries
import sys, os, subprocess, re
from dockingtools_lib import getantigenchainid, writefile

#*************************************************************************

# Define input files

# Complex file
PDBfile = sys.argv[1]
# Free antigen
antigen = sys.argv[2]
# Get output path from command line (if present)
OUTPath = './'
try:
   OUTPath = sys.argv[3] + '/'
except IndexError:
   OUTPath = './'

#*************************************************************************

# Split input complex into two files
subprocess.run([f"/home/oliverh/ab-docking-scripts/splitantibodyantigenchains.py {PDBfile}"], shell=True)

# Define split protein filenames

# Define input filename
inputfilename = os.path.basename(PDBfile).split('.')[0]

# Define antibody filename
split_antibody = f"{inputfilename}_ab.pdb"

# Define antigen filename
split_antigen = f"{inputfilename}_ag.pdb"

#*************************************************************************

# Find interface residues in complex

# Define location for interface residues file
int_res = OUTPath + "int_res"

# Run findif.pl to identify interface residues, writing result to int_res
subprocess.run(["~/ab-docking-scripts/findif.pl -x " + PDBfile + " " + split_antigen + " " + split_antibody + " > " + int_res], shell=True)

#*************************************************************************

# Get antigen interface residues

# Initialise list for antigen residues
ag_int_res = []

# Get antigen chain ID (single chain)
agchainid = getantigenchainid(PDBfile)

# Read int_res and extract residue numbers
with open(int_res) as file:
   # Read rows in file
   rows = file.readlines()
   # Identify antigen chain residues
   for line in rows:
      if str(agchainid) in line:
         contents = re.compile("([a-zA-Z]+)([0-9]+)").match(line)
         ag_int_res += [contents.group(2)]

#*************************************************************************

# Get length of antigen chain from file
with open(complex) as file:
   # Read rows in file
   rows = file.readlines()
   # IDentify terminal antigen chain residue
   for line in rows:
      if 'TER' and f"{agchainid}" in line and 'ATOM' not in line:
         AGcontents = line.split()
         AGlength = AGcontents[4]

#*************************************************************************

# Generate list of non-interface antigen residues
ag_NI_res = []
for i in range(int(AGlength)+1):
   if str(i) not in ag_int_res:
      ag_NI_res += [str(agchainid + str(i))]

#*************************************************************************

# Write profit control script
list_AG_zones = []
# Add non interface residues to list
for item in ag_NI_res:
   string = f"ZONE {item}-{item}"
   list_AG_zones += [string]
# Create list of lines to add to script
script = []
for item in list_AG_zones:
   script += [item]
script += [f"align {agchainid}*:{agchainid}*", "FIT", "ratoms ca"]

# Get the base filename from the input file
filename = os.path.basename(PDBfile).split('.')[0]
# Define the script filename
scriptname = "%s.prf" % filename
# Define outfile
PRFfile = OUTPath + scriptname
# Write script file
writefile(PRFfile, script)

#*************************************************************************

# Run profit, returning the RMS values across all atoms and across CA atoms
result = subprocess.check_output([f"profit -f {PRFfile} {PDBfile} {antigen} | grep 'RMS' | tail -2"], shell=True)
# Decode results
result = str(result, 'utf-8')
# Split result text into list
result = result.split()
# Set all_atoms RMSD
all_atoms = result[1]
# set CA atoms RMSD
CA_atoms = result[3]
# Print RMSD values
print('All atoms RMSD:   '+all_atoms)
print('CA atoms RMSD:    '+CA_atoms)