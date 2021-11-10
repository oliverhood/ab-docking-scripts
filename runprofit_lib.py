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

#*************************************************************************

def removePDBtail(PDBfile):
   """
   Remove the line 'END' from PDB files so they can be combined to give a single PDB file.

   """
   # Get the base filename from input file
   filename = os.path.basename(PDBfile).split('.')[0]

   # Specify new filename
   new_filename = "%s_strip.pdb" % filename

   # Open PDB file
   with open(PDBfile) as file:
      #Read rows in file
      rows = file.readlines()

   # Write new PDB file
   with open(new_filename, "w") as file:
      for line in rows:
         if 'END' not in line.strip('\n'):
            file.write(line)