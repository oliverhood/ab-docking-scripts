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

   """
   # Get the antigen chain ID from the input PDB file
   agchainid = getantigenchainid(PDBfile)
   # Get the input filename
   filename = os.path.basename(PDBfile).split('.')[0]
   # Define processed file name (output of splitantibodyantigenchains_rosetta.py)
   processed_filename = filename + "_processed.pdb"
   # Write list of prepack_flags contents
   flags = [
      # Location of the rosetta database
      "-database /home/oliverh/DockingSoftware/rosetta/rosetta/main/database", 
      # Spacer
      "", 
      # Input filename
      f"-in:file:s {processed_filename}", 
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

#*************************************************************************

def writedocking_flags(PDBfile, nstructures=25):
   """
   Write the docking_flags file needed to run the Rosetta docking protocol.
  
   """
   # Get the antigen chain ID from the input PDB file
   agchainid = getantigenchainid(PDBfile)
   # Get the input filename
   filename = os.path.basename(PDBfile).split('.')[0]
   # Define prepacked filename (output of Rosetta prepack)
   prepacked_filename = filename + "_processed_prepack_0001.pdb"
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

#*************************************************************************

