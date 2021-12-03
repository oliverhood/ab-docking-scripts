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
from dockingtools_lib import getantigenchainid

#*************************************************************************

def preprocess(PDBfile):
   """
   Pre-process input PDB file using Rosetta's 'prepack' protocol

   """
   # Get the filename from the input file
   filename = os.path.basename(PDBfile).split('.')[0]
   # 