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

import subprocess
import time

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

def writefile(filename, list):
   """
   Take a list as input and write it to a file in the current working directory

   """
   with open(str(filename), "w") as file:
      for line in list:
         file.write("%s\n" % line)

#*************************************************************************

def get_time():
   """
   Get the current date and time.

   """
   # Get time
   current_time = time.strftime(r"%d.%m.%Y   %H:%M:%S", time.localtime())
   # Return time
   return current_time

#*************************************************************************

def get_date():
   """
   Get the current date.

   """
   # Get date
   current_date = time.strftime(r"%d.%m.%Y", time.localtime())
   # Return date
   return current_date

#*************************************************************************

def evaluate_results(OG_file, *args, single_file=True):
   """
   Take either a single docked antibody/antigen structure, or separate antibody and antigen structures as input, run the relevant runprofit script on the structures and output the results into a results file. (Will later add functionality to determine the proportion of correctly predicted contacts)

   >>> evaluate_results('test/test8_OG.pdb', 'test/test8_single.pdb')
   ['Docking test on test/test8_OG.pdb   07.12.2021', '', 'Method name not specified', 'All atoms RMSD:  10.751', 'CA atoms RMSD:   10.572']
   >>> evaluate_results('test/test8_OG.pdb', 'test/test8_ab.pdb', 'test/test8_Dag.pdb')
   ['Docking test on test/test8_OG.pdb   07.12.2021', '', 'Method name not specified', 'All atoms RMSD:  1.652', 'CA atoms RMSD:   1.622']

   """
   # Initialise results list
   dockingresults = []
   # Check whether input is single file (antibody+antigen) or separate files (antibody, antigen)
   if len(args) > 1:
      single_file=False
   # If the input is a single PDB file containing both the antibody and antigen chains
   if single_file:   
      # Define the docked_file
      docked_file = args[0]
      # Run the relevant profit script, capture results in 'result'
      result = subprocess.check_output([f"~/ab-docking-scripts/runprofit_single.py {OG_file} {docked_file}"], shell=True)
      result = str(result, 'utf-8')
      # Extract the result lines from output
      contents = result.split('\n')
      all_atoms = contents[0]
      CA_atoms = contents[1]
      # Add method, results to dockingresults
      dockingresults += [method_title]
      dockingresults += [all_atoms]
      dockingresults += [CA_atoms]
      # Add spacer
      dockingresults += ""
   # If the input contains separate PDB files for the antibody and docked antigen chains
   if not single_file:
      # Set Title
      method_title = f"{method}"
      # Define the input files
      Ab_file = args[0]
      Dag_file = args[1]
      # Run the relevant profit script, capture results in 'result'
      result = subprocess.check_output([f"~/ab-docking-scripts/runprofit.py {OG_file} {Ab_file} {Dag_file}"], shell=True)
      result = str(result, 'utf-8')
      # Extract the result lines from output
      contents = result.split('\n')
      all_atoms = contents[0]
      CA_atoms = contents[1]
      # Add method, results to dockingresults
      dockingresults += [method_title]
      dockingresults += [all_atoms]
      dockingresults += [CA_atoms]
      # Add spacer
      dockingresults += ""
   # Return docking results
   return dockingresults

#*************************************************************************

# Testing functions
if __name__ == "__main__":
    import doctest
    doctest.testmod()