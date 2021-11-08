#!/usr/bin/env python3
"""
Program: split-antibody-antigen-files
File:    split-antibody-antigen-files.py

Version: V1.0
Date: 04.11.21
Function:   Library:   Functions for split-antibody-antigen-files,extracts and processes antigen and antibody chains from a PDB file 
          for input to docking algorithms.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody (that may or may not be bound by an antigen(s)) and returns the antibody and antigen(s) chains as separate PDB files. The antigen chain is processed (randomly rotated and transformed) before being written to the new PDB file.

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
import os
import random

#*************************************************************************

def getantigenchainid(PDBfile):
   """
   Read input file and extract the chain identifier for the antigen chain
   (if present)

   >>> getantigenchainid("test/test1.pdb")
   'None'
   >>> getantigenchainid("test/test2.pdb")
   'C'
   >>> getantigenchainid("test/test3.pdb")
   'Multiple chains'
   >>>

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

   >>> extractantibodychains("test/test1.pdb")
   'Multiple antigen chains'
   >>> extractantibodychains("test/test3.pdb")
   'No antigen'
   >>> extractantibodychains("test/test4.pdb")
   antibody_chains

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
      antibody_chains = os.system("pdbgetchain H,L " + PDBfile)
   return antibody_chains

#*************************************************************************

def extractantigenchain(PDBfile):
   """
   Search input PDB file for number of antigen chains then extract the antigen chain if there is a single antigen chain present

   >>> extractantibodychains("test1.pdb")
   'Multiple antigen chains'
   >>> extractantibodychains("test2.pdb")
   processed_antigen_chain
   >>> extractantibodychains("test3.pdb")
   'No antigen'
   >>> extractantibodychains("test4.pdb")
   processed_antigen_chain

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
      processed_antigen_chain = os.system("pdbgetchain " + agchainid + " " + PDBfile
      #Rotate the antigen chain
      + " | pdbrotate -x " + str((random.randint(45,315))) + " -y " + str((random.randint(45,315))) + " -z " + str((random.randint(45,315)))
      #Translate the antigen chain
      + " | pdbtranslate -x " + str((random.randint(-25,25))) + " -y " + str((random.randint(-25,25))) + " -z " + str((random.randint(-25,25))))
   #Return the processed antibody chain
   return processed_antigen_chain

#*************************************************************************