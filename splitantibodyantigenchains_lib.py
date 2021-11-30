#!/usr/bin/env python3
"""
Program: splitantibodyantigenchains_lib
File:    splitantibodyantigenchains_lib.py

Version: V1.0
Date: 04.11.21
Function:   Library:   Functions for splitantibodyantigenchains, extracts and processes antigen and antibody chains from a PDB file 
          for input to docking algorithms.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody (that may or may not be bound by an antigen(s)) and returns the antibody and antigen(s) chains as separate PDB files. The antigen chain is processed (randomly rotated and transformed) before being written to the new PDB file.

--------------------------------------------------------------------------

Usage:
======
splitantibodyantigenchains.py PDBFILE OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   04.11.21   Original   By: OECH
"""

#*************************************************************************

# Import Libraries
import sys
import os
import random
import subprocess
from subprocess import PIPE

#*************************************************************************

def getantigenchainid(PDBfile):
   """
   Read input file and extract the chain identifier for the antigen chain
   (if present)

   >>> getantigenchainid("test/test1.pdb")
   'No chains'
   >>> getantigenchainid("test/test2.pdb")
   'C'
   >>> getantigenchainid("test/test3.pdb")
   'Multiple chains'
   >>> getantigenchainid('test/test4.pdb')
   'C'

   """
   #Set antigen_count to zero
   antigen_count = 0
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
   #Return chainid for single antigen chain
   if antigen_count == 1:
      return agchainid
   elif antigen_count > 1:
      return 'Multiple chains'
   else:
      return 'No chains'

#*************************************************************************

def extractantibodychains(PDBfile):
   """
   Search input file for the number of antigen chains then extract the antibody chains if there is a single antigen chain

   >>> extractantibodychains('test/test1.pdb')
   'test/test1.pdb has no antigen'
   >>> extractantibodychains('test/test3.pdb')
   'test/test3.pdb has multiple antigen chains'

   """
   #Get the antigen's chain id
   agchainid = getantigenchainid(PDBfile)
   #Filter out files with multiple or no antigen chains
   if agchainid == 'Multiple chains':
      return PDBfile + ' has multiple antigen chains'
   elif agchainid == 'No chains':
      return PDBfile + ' has no antigen'
   else:
      #Extract the antibody chains
      get_antibody_chains = subprocess.run(["pdbgetchain H,L " + PDBfile], shell=True, universal_newlines=True, stdout=subprocess.PIPE)
   antibody_chains = get_antibody_chains.stdout
   return antibody_chains

#*************************************************************************

def extractantigenchain(PDBfile):
   """
   Search input PDB file for number of antigen chains then extract the antigen chain if there is a single antigen chain present

   >>> extractantibodychains("test/test1.pdb")
   'test/test1.pdb has no antigen'
   >>> extractantibodychains("test/test3.pdb")
   'test/test3.pdb has multiple antigen chains'

   """
   #Get the antigen's chain id
   agchainid = getantigenchainid(PDBfile)
   #Filter out files with multiple or no antigen chains
   if agchainid == 'Multiple chains':
      return PDBfile + ' has multiple antigen chains'
   elif agchainid == 'No chains':
      return PDBfile + ' has no antigen'
   else:
      #Extract the antigen chain
      get_processed_antigen_chain = subprocess.run(["pdbgetchain " + agchainid + " " + PDBfile
      #Rotate the antigen chain
      + " | pdbrotate -x " + str((random.randint(-8,8))) + " -y " + str((random.randint(-8,8))) + " -z " + str((random.randint(-8,8)))
      #Translate the antigen chain
      + " | pdbtranslate -x " + str((random.randint(2,5))) + " -y " + str((random.randint(2,5))) + " -z " + str((random.randint(2,5)))], stdout=subprocess.PIPE, universal_newlines=True, shell=True)
   processed_antigen_chain = get_processed_antigen_chain.stdout
   #Return the processed antibody chain
   return processed_antigen_chain

#*************************************************************************

# Testing functions
if __name__ == "__main__":
    import doctest
    doctest.testmod()