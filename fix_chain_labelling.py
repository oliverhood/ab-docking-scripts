#!/usr/bin/env python3
"""
Program: fix_chain_labelling
File:    fix_chain_labelling.py

Version:  V1.0
Date:     05.12.2023
Function: Fix chain labelling in Haddock output files

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============


--------------------------------------------------------------------------

Usage:
======
Run with bioptools in path

--------------------------------------------------------------------------

Revision History:
=================
V1.0   05.12.23   Original   By: OECH

"""

#*************************************************************************

# Import libraries
import subprocess, os
from dockingtools_lib import getantigenchainid

#*************************************************************************

# Collect PDB IDs from dir
list_ids = []

# Get filenames in current directory
files = os.listdir()

# Extract PDB IDs
for item in files:
   if '_Rosetta' in item:
      pdb_id = item.split('_Rosetta')[0]
      list_ids += [pdb_id]

#*************************************************************************

# Function to fix chain labelling for input
def fix_chain_labelling(PDBfile, resultfile):
   # Define output filename
   outfilename = f"{resultfile}_split_labelled.pdb"
   # Get ag chain id
   agchainid = getantigenchainid(PDBfile)
   # Define executable
   exe=f"pdbchain {resultfile} | pdbrenum -c L,H,{agchainid} > {outfilename}"
   # Run executable
   subprocess.run([exe], shell=True)

#*************************************************************************

# Run relabelling on haddock files
for pdb in list_ids:
   # Define filenames
   PDBfile = f"{pdb}.pdb"
   haddock_water = f"{pdb}_nohydrogens_Haddock_waters_result.pdb"
   haddock_nowater = f"{pdb}_nohydrogens_Haddock_nowaters_result.pdb"
   # Run on waters
   fix_chain_labelling(PDBfile, haddock_water)
   # Run on no waters
   fix_chain_labelling(PDBfile, haddock_nowater)

   