#!/usr/bin/env python3
"""
Program: runprofit
File:    runprofit.py

Version: V1.0
Date:    10.11.21
Function:   Library:   Functions for runprofit, processes the output files of docking algorithms run on split antibody/antigen structures to compare them to the original antibody/antigen structures using ProFit.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============


--------------------------------------------------------------------------

Usage:
======


--------------------------------------------------------------------------

Revision History:
=================


"""

#*************************************************************************

# Import Libraries

import os

#*************************************************************************

def combineabdagfiles(Ab_file, DAg_file, OUTPath=''):
   """
   Write new PDB file containing the contents of Ab_file and DAg_file with 'END' lines removed from each

   >>> combineabdagfiles('test/test5_ab.pdb', 'test/test5_dag.pdb')
   'Writing test5_AbDag.pdb'
   >>>
   """   
   # Get the base filename from input files
   filename = os.path.basename(Ab_file).split('.')[0].split('_')[0]
   # Define new filename
   ab_dag_name = "%s_AbDag.pdb" % filename
   # Open antibody file
   with open(Ab_file) as file:
      # Extract contents
      ab = file.readlines()
   # Open docked antigen file
   with open(DAg_file) as file:
      # Extract contents
      dag = file.readlines()
   # Combine antibody and docked antigen files
   AbDag = ab + dag
   # Write new PDB file
   with open(str(OUTPath+ab_dag_name), "w") as file:
      for line in AbDag:
         # Skip lines containing 'END'
         if 'END' not in line.strip('\n'):
            file.write(line)
   # Return written file 
   return "Writing " + ab_dag_name

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

def writecontrolscript(PDBfile, OUTPath=''): # Input file must be the unsplit PDB
   """
   Write control script for profit using the antigen chainid from the original PDB file for the argument 'rzone'

   >>> writecontrolscript('test/test5.pdb')
   'Writing test5.prf'

   """
   # Get the base filename from the input file
   filename = os.path.basename(PDBfile).split('.')[0]
   # Define the script filename
   scriptname = "%s.prf" % filename
   # Get the antigen's chain id
   agchainid = getantigenchainid(PDBfile)
   # Create antigen chain argument
   ag_arg = "rzone " + agchainid + "*:" + agchainid + "*"
   # Create list of lines to add to script
   script = ["align L*:L*", "align H*:H* APPEND", "fit", ag_arg, "ratoms ca"]
   # Write script file
   with open(str(OUTPath+scriptname), "w") as file:
      for line in script:
         file.write("%s\n" % line)
   return "Writing " + scriptname

#*************************************************************************

# Testing functions
if __name__ == "__main__":
    import doctest
    doctest.testmod()