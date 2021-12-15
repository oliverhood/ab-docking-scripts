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
   ('All atoms RMSD:  10.751', 'CA atoms RMSD:   10.572', 'Correctly predicted residue pairs:       0.24324324324324326', 'Correctly predicted residues (antibody): 0.5789473684210527', 'Correctly predicted residues (antigen):  0.6428571428571429')
   >>> evaluate_results('test/test8_OG.pdb', 'test/test8_ab.pdb', 'test/test8_Dag.pdb')
   ('All atoms RMSD:  1.652', 'CA atoms RMSD:   1.622', 'Single PDB file needed as input', 'Single PDB file needed as input', 'Single PDB file needed as input')

   """
   # Check whether input is single file (antibody+antigen) or separate files (antibody, antigen)
   if len(args) > 1:
      single_file=False
   # If the input is a single PDB file containing both the antibody and antigen chains
   if single_file:   
      # Define the docked_file
      docked_file = args[0]
      # Run the relevant profit script, capture results in 'result'
      result_profit = subprocess.check_output([f"~/ab-docking-scripts/runprofit_single.py {OG_file} {docked_file}"], shell=True)
      result_profit = str(result_profit, 'utf-8')
      # Extract the result lines from output
      contents = result_profit.split('\n')
      all_atoms = contents[0]
      CA_atoms = contents[1]
      # Get interface evaluation metrics using evaluate_interface.py
      result_interface = subprocess.check_output([f"~/ab-docking-scripts/evaluate_interface.py {OG_file} {docked_file}"], shell=True)
      result_interface = str(result_interface, 'utf-8')
      # Extract the result lines from output
      contents = result_interface.split('\n')
      res_pairs = contents[2]
      ab_res = contents[3]
      ag_res = contents[4]
   # If the input contains separate PDB files for the antibody and docked antigen chains
   if not single_file:
      # Set Title
      # Define the input files
      Ab_file = args[0]
      Dag_file = args[1]
      # Run the relevant profit script, capture results in 'result'
      result_profit = subprocess.check_output([f"~/ab-docking-scripts/runprofit.py {OG_file} {Ab_file} {Dag_file}"], shell=True)
      result_profit = str(result_profit, 'utf-8')
      # Extract the result lines from output
      contents = result_profit.split('\n')
      all_atoms = contents[0]
      CA_atoms = contents[1]
      res_pairs = "Single PDB file needed as input"
      ab_res = "Single PDB file needed as input"
      ag_res = "Single PDB file needed as input"
   # Return docking results
   return all_atoms, CA_atoms, res_pairs, ab_res, ag_res

#*************************************************************************

def getlowestscore(list):
   """
   Take a list of scores as input and output the lowest score.
   """
   bestscore = 10
   for item in list:
      if item < bestscore:
         bestscore = item
   return bestscore

#*************************************************************************

def gethighestscore(list):
   """
   Take a list of scores as input and output the highest score.
   """
   bestscore = 0
   for item in list:
      if item > bestscore:
         bestscore = item
   return bestscore

#*************************************************************************

def getnumberhits(list):
   """
   Take a list of RMSD values as input and output the number of 'hits', scores below an RMSD of 3.
   """
   hits = 0
   for item in list:
      if item < 3.0:
         hits +=1
   return hits

#*************************************************************************

# Testing functions
if __name__ == "__main__":
    import doctest
    doctest.testmod()