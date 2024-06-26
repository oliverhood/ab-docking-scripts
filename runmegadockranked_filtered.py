#!/usr/bin/env python3
"""
Program: runmegadockranked
File:    runmegadockranked.py

Version: V1.0
Date:    18.11.21
Function: Run input antibody and antigen files through the Megadock docking algorithm and extract the top-ranked docked ligand into a new PDB file.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a receptor (antibody), ligand (antigen), and their bound complex as input. The residues at the binding interface between the proteins is determined and non-interface residues are 'blocked' using the blockNIres program

--------------------------------------------------------------------------

Usage:
======
runmegadockranked.py receptorfile ligandfile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   19.11.2021   Original   By: OECH


"""

#*************************************************************************

#Import Libraries

import sys
import os
import subprocess
from runprofit_lib import combineabdagfiles

#*************************************************************************
# Get input files

# Define receptor (antibody) file
receptor = sys.argv[1]
# Define ligand (antigen) file
ligand = sys.argv[2]
# Get output path from command line (if present)
OUTPath = ''
try:
   OUTPath = sys.argv[3] + '/'
except IndexError:
   OUTPath = './'

#*************************************************************************
# Add hydrogens to input files

# Get input file basename
filenamecontents = os.path.basename(receptor).split('.')[0].split('_')
inputfilename = filenamecontents[0] + "_" + filenamecontents[1]
# Define output antibody file name
antibody_hydrogens = OUTPath + inputfilename + "_ab_hydrogens.pdb"
# Define output antigen file name
antigen_hydrogens = OUTPath + inputfilename + "_ag_hydrogens.pdb"
# Antibody file
subprocess.run([f"pdbhadd -a {receptor} {antibody_hydrogens}"], shell=True)
# Antigen file
subprocess.run([f"pdbhadd -a {ligand} {antigen_hydrogens}"], shell=True)

#*************************************************************************
# Run Megadock
subprocess.run([f"~/DockingSoftware/megadock-4.1.1/megadock -R {antibody_hydrogens} -L {antigen_hydrogens} -o megadock.out"], shell=True)
# Define output filename
outfile = OUTPath+inputfilename + "_megadockranked_Dag.pdb"

#*************************************************************************
# Run ZRank on megadock outfileq
subprocess.run(["~/DockingSoftware/zdock3.0.2/zrank megadock.out 1 2000"], shell=True)

# Extracting top ranked output

# Initiate min out variable
min_out = 0

# Read Zrank out file
with open('megadock.out.zr.out') as file:
   # Read lines
   rows = file.readlines()
   # Identify highest scoring output
   for line in rows:
      contents = line.split()
      if float(contents[1]) < min_out:
         min_out = float(contents[1])
         # Get number of the top hit
         top_hit = contents[0]

# define gen_decoy function
def gen_decoy(outfile, antigen_hydrogens, top_hit):
    # Extract top docking result from megadock using decoygen
    subprocess.run(["~/DockingSoftware/megadock-4.1.1/decoygen " + outfile + " " + antigen_hydrogens + " megadock.out " + top_hit], shell=True)

gen_decoy(outfile, antigen_hydrogens, top_hit)

#*************************************************************************

# Combine ab and dag files to give single docked output file

# Output filename
resultfile = OUTPath + inputfilename + "_MegadockRanked_result.pdb"
# Open antibody file
with open(receptor) as file:
   # Extract contents
   ab = file.readlines()
   # Open docked antigen file
with open(outfile) as file:
   # Extract contents
   dag = file.readlines()
   # Combine antibody and docked antigen files
AbDag = ab + dag
# Write new PDB file
with open(resultfile, "w") as file:
   for line in AbDag:
   # Skip lines containing 'END'
      if 'END' not in line.strip('\n'):
         file.write(line)

#*************************************************************************

# Function to get second, third megadock output
def filter_output(index: int):
    # Define indices score lists
    scores = []
    # Define dictionary indices:scores
    score_dict = {} #format == index:score
    # Set initial min_out
    min_out = 0
    # Open file
    with open('megadock.out.zr.out') as file:
       # Read lines
       rows = file.readlines()
       # Identify highest scoring output
       for line in rows:
          contents = line.split()
          index = contents[0]
          score = contents [1]
          scores += [score]
          score_dict[index] = score
    # Sort list of scores
    scores_sorted = scores.sort()
    # Get required score (second/third best etc)
    score_out = scores_sorted[index]
    # return index of second/third/etc best score
    for number, score in score_dict:
        if score == score_out:
            return number

#*************************************************************************

# Filter for ab-ag distance

# Get distance between ab and ag
abagdist = subprocess.check_output(f"abagdist {resultfile}")

# Add filtering
if float(abagdist) >= 10.0:
    next_hit =




result = subprocess.check_output("profit -f" + " " + script + " " + OG_nohydrogens + " " + docked_nohydrogens + " | grep 'RMS' | tail -2", shell=True)
