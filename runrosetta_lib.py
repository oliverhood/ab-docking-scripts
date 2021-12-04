#!/usr/bin/env python3
"""
Program: runrosetta_lib
File:    runrosetta._lib.py

Version:  V1.0
Date:     03.12.21
Function:   Library: Functions for runrosetta.py program, takes a PDB file containing an antibody and an antigen as input and runs the Rosetta docking algorithm on them, extracting the top scoring structure as the output.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing an antibody and an antigen as input, pre-processes the file using the Rosetta 'prepack' protocol, generates __ docked structures using the Rosetta 'protein-protein docking' protocol, then extracts the top scoring structure as the docking result.

--------------------------------------------------------------------------

Usage:
======
runrosetta.py PDBfile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   03.12.2021   Original   By: OECH

"""

#*************************************************************************

# Import Libraries

import os
from dockingtools_lib import (getantigenchainid, writefile)

#*************************************************************************

def writeprepack_flags(PDBfile):
   """
   Write the prepack_flags file needed to run the Rosetta prepack protocol.

   >>> writeprepack_flags('test/test6.pdb')
   -database /home/oliverh/DockingSoftware/rosetta/rosetta/main/database

   -in:file:s 1yqv_0_processed.pdb
   -docking:partners HL_Y

   -ex1
   -ex2aro

   -out:suffix _prepack

   """
   # Get the antigen chain ID from the input PDB file
   agchainid = getantigenchainid(PDBfile)
   # Get the input filename
   filename = os.path.basename(PDBfile).split('.')[0]
   # Write list of prepack_flags contents
   flags = [
      # Location of the rosetta database
      "-database /home/oliverh/DockingSoftware/rosetta/rosetta/main/database", 
      # Spacer
      "", 
      # Input filename
      f"-in:file:s {PDBfile}", 
      # Docking partners (Heavy/Light chain, Antigen chain)
      f"-docking:partners HL_{agchainid}", 
      # Spacer
      "", 
      # Common flags (given by Rosetta protocol)
      "-ex1", 
      "-ex2aro", 
      # Spacer
      "", 
      # Output file suffix
      "-out:suffix _prepack"]
   # Define flags filename
   prepack_flags = "prepack_flags"
   # Write prepack_flags file
   writefile(prepack_flags, flags)
   # Return the flags list
   for item in flags:
      print(item)

#*************************************************************************

def writedocking_flags(PDBfile, nstructures=25):
   """
   Write the docking_flags file needed to run the Rosetta docking protocol.

   >>> writedocking_flags('test/test6.pdb')
   -database /home/oliverh/DockingSoftware/rosetta/rosetta/main/database

   -in:file:s 1yqv_0_processed_prepack_0001.pdb
   -docking:partners HL_Y
   -nstruct 25

   -ex1
   -ex2aro

   -out:suffix _local_dock
  
   """
   # Get the antigen chain ID from the input PDB file
   agchainid = getantigenchainid(PDBfile)
   # Get the input filename
   filename = os.path.basename(PDBfile).split('.')[0]
   # Define prepacked filename (output of Rosetta prepack)
   prepacked_filename = filename + "_prepack_0001.pdb"
   # Write list of docking_flags contents
   flags = [
      # Location of the rosetta database
      "-database /home/oliverh/DockingSoftware/rosetta/rosetta/main/database", 
      # Spacer
      "", 
      # Input file
      f"-in:file:s {prepacked_filename}", 
      # Docking partners (Heavy/Light chain, Antigen chain)
      f"-docking:partners HL_{agchainid}", 
      # Number of output structures
      f"-nstruct {nstructures}", 
      # Spacer
      "", 
      # Common flags (given by Rosetta protocol)
      "-ex1", 
      "-ex2aro", 
      # Spacer
      "", 
      # Output file suffix
      "-out:suffix _local_dock"]
   # Define flags filename
   docking_flags = "docking_flags"
   # Write docking_flags file
   writefile(docking_flags, flags)
   # Return the flags list
   for item in flags:
      print(item)

#*************************************************************************

def getbestresult(docking_scores):
   """
   Find best docking result from docking files, copy to new file 'Docking result (with number)'

   """
   # Open score file
   with open(docking_scores) as file:
      # Split into rows
      rows = file.readlines()
   # Extract 'score' lines
   scores = []
   for line in rows:
      if 'SCORE' in line:
         scores += [line]
   # Get header from scores
   scores_header = scores[0].split()
   # Get index of I_sc score
   I_sc_index = scores_header.index("I_sc")
   # Find best scoring docked structure
   # Initialise top (lowest) score
   top_score = 0
   best_structure = 'None'
   # Loop through scores
   for item in scores[1:]: #Excluding header row
      individual_scores = item.split()
      I_sc = float(individual_scores[I_sc_index])
      if I_sc < top_score:
         top_score = I_sc
         best_structure = individual_scores[-1] # Last item is name of scored structure
   # Define file name of best structure
   docking_outfile = best_structure + ".pdb"
   # Return best docked structure
   return(docking_outfile)

#*************************************************************************

# Testing functions
if __name__ == "__main__":
    import doctest
    doctest.testmod()