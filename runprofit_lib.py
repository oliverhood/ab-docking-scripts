#!/usr/bin/env python3
"""
Program: runprofit
File:    runprofit.py

Version: V1.0
Date:    
Function: Process the output files of docking algorithms run on split antibody/antigen structures to compare them to the original antibody/antigen structures using ProFit.

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

def combineabdagfiles(Ab_file, DAg_file):
   """
   Write new PDB file containing the contents of Ab_file and DAg_file with 'END' lines removed from each

   """   
   # Get the base filename from input files
   filename = os.path.basename(Ab_file).split('.')[0]

   # Define new filename
   ab_dag_name = "%s_Dag.pdb" % filename

   # Open antibody file
   with open(Ab_file) as file:
      # Extract contents
      ab = file.readlines()

   # Open docked antigen file
   with open(DAg_file) as file:
      dag = file.readlines()

   # Combine antibody and docked antigen files
   AbDag = ab + dag

   # Write new PDB file
   with open(ab_dag_name, "w") as file:
      for line in AbDag:
         # Skip lines containing 'END'
         if 'END' not in line.strip('\n'):
            file.write(line)
   # Return written file (?)
   return ab_dag_name