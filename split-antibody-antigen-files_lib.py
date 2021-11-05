#!/usr/bin/env python3
"""
Program: split-antibody-antigen-files
File:    split-antibody-antigen-files.py

Version: V1.0
Date: 04.11.21
Function: Extract and process antigen and antibody chains from a PDB file 
          for input to docking algorithms.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody (that
may or may not be bound by an antigen(s)) and returns the antibody and 
antigen(s) chains as separate PDB files. The antigen chain is processed 
(randomly rotated and transformed) before being written to the new PDB 
file.

--------------------------------------------------------------------------

Usage:
======
split-antibody-antigen-files PDBFILE

--------------------------------------------------------------------------

Revision History:
=================
V1.0   04.11.21   Original   By: OECH
"""

#*************************************************************************

# Import Libraries
import sys
from bioptools import (pdbgetchain, pdbtranslate, pdbrotate)

#*************************************************************************

def getantigenchainid(PDBfile):
   """
   Read input file and extract the chain identifier for the antigen chain
   (if present)

   >>> getantigenchainid("test1.pdb")
   None
   >>> getantigenchainid("test2.pdb")
   'C'
   >>> getantigenchainid("test3.pdb")
   'C'
   'D'
   >>>

   """
   #Set antigen_count to zero
   antigen_count = 0
   #Give a default chainid
   agchainid = 'No Antigen'
   #Open PDB file
   with open(PDBfile) as file:
      #Read rows in file
      rows = file.readlines()
      #Identify Antigen chains from PDB Header
      for line in rows:
         if 'CHAIN A' in line:
            #Increase antigen_count by 1
            antigen_count += 1
            #Split the line into individual words
            contents=line.split()
            #Extract the antigen chainid
            agchainid = contents[4]
         #Break loop when first ATOM coordinate is encountered
         if 'ATOM' in line:
            break
   return agchainid