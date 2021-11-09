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
   >>> extractantibodychains("test/test4.pdb")
   REMARK 950 CHAIN-TYPE  LABEL ORIGINAL
   REMARK 950 CHAIN L     L     A
   REMARK 950 CHAIN H     H     B
   REMARK 950 CHAIN A     C     C
   ATOM      1  N   ASP L   1      23.963  -0.947  -1.031  1.00 37.52           N  
   ATOM      2  CA  ASP L   1      25.119  -0.797  -1.881  1.00 32.56           C  
   ATOM      3  C   ASP L   1      25.715   0.493  -1.356  1.00 29.72           C  
   ATOM      4  O   ASP L   1      24.964   1.396  -0.971  1.00 28.87           O  
   ATOM      5  CB  ASP L   1      24.721  -0.606  -3.341  1.00 34.71           C  
   ATOM      6  CG  ASP L   1      24.061  -1.777  -4.067  1.00 35.11           C  
   ATOM      7  OD1 ASP L   1      23.841  -2.849  -3.496  1.00 35.99           O  
   ATOM      8  OD2 ASP L   1      23.798  -1.612  -5.255  1.00 38.08           O  
   ATOM      9  H1  ASP L   1      23.429  -0.061  -1.100  1.00 20.00           H  
   ATOM     10  H2  ASP L   1      23.417  -1.821  -1.194  1.00 20.00           H  
   ATOM     11  H3  ASP L   1      24.348  -0.968  -0.067  1.00 20.00           H  
   TER      12      ASP L   1                                                      
   ATOM   1022  N   GLN H   1      53.626  -9.527 -20.890  1.00 47.05           N  
   ATOM   1023  CA  GLN H   1      53.065  -8.221 -21.175  1.00 45.24           C  
   ATOM   1024  C   GLN H   1      51.591  -8.519 -20.891  1.00 40.44           C  
   ATOM   1025  O   GLN H   1      51.089  -9.519 -21.415  1.00 39.85           O  
   ATOM   1026  CB  GLN H   1      53.350  -7.855 -22.663  1.00 52.20           C  
   ATOM   1027  CG  GLN H   1      52.676  -8.630 -23.848  1.00 61.79           C  
   ATOM   1028  CD  GLN H   1      52.713 -10.160 -23.726  1.00 66.73           C  
   ATOM   1029  OE1 GLN H   1      53.667 -10.694 -23.137  1.00 69.55           O  
   ATOM   1030  NE2 GLN H   1      51.676 -10.926 -24.065  1.00 67.03           N  
   ATOM   1031  H1  GLN H   1      53.092 -10.197 -21.491  1.00 20.00           H  
   ATOM   1032  H2  GLN H   1      54.629  -9.655 -21.094  1.00 20.00           H  
   ATOM   1033  H3  GLN H   1      53.385  -9.812 -19.917  1.00 20.00           H  
   ATOM   1034 HE21 GLN H   1      51.822 -11.902 -24.048  1.00  0.00           H  
   ATOM   1035 HE22 GLN H   1      50.827 -10.505 -24.333  1.00  0.00           H  
   TER    1036      GLN H   1                                                      
   MASTER        4    0    0    0    0    0    0    0   25    2    0    0          
   END                                                                             
   0

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
      get_antibody_chains = subprocess.run(["pdbgetchain H,L " + PDBfile], stdout=subprocess.PIPE, universal_newlines=True, shell=True)
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
      + " | pdbrotate -x " + str((random.randint(45,315))) + " -y " + str((random.randint(45,315))) + " -z " + str((random.randint(45,315)))
      #Translate the antigen chain
      + " | pdbtranslate -x " + str((random.randint(-25,25))) + " -y " + str((random.randint(-25,25))) + " -z " + str((random.randint(-25,25)))], stdout=subprocess.PIPE, universal_newlines=True, shell=True)
   processed_antigen_chain = get_processed_antigen_chain.stdout
   #Return the processed antibody chain
   return processed_antigen_chain

#*************************************************************************

# Testing functions
if __name__ == "__main__":
    import doctest
    doctest.testmod()