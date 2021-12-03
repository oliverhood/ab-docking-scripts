#!/usr/bin/env python3
"""
Program: dockingtools_lib
File:    dockingtools_lib.py

Version:  V1.0
Date:     03.12.2021
Function:   Library: Library of frequently used functions in the 'Antibody-Antigen Docking' Project.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This library contains a number of functions that I frequently need in scripts for the 'Antibody-Antigen Docking' Project.

--------------------------------------------------------------------------

Revision History:
=================
V1.0   03.12.2021   Original   By: OECH

"""

#*************************************************************************

# Import Libraries


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