#!/usr/bin/env python3
"""
Program: runhaddock_lib
File:    runhaddock_lib.py

Version:  V1.0
Date:     15.02.2022
Function:   Library: Run input antibody and antigen files through the haddock protein docking algorithm, output a single result file.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes an antibody file and an antigen file as input for the haddock protein docking program, a single PDB file will be extracted as a result with waters included and without waters included (waters should be better?).

--------------------------------------------------------------------------

Usage:
======
runhaddock.py antibody antigen OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   15.02.22   Original   By: OECH

"""

#*************************************************************************

# Import libraries
import subprocess
from dockingtools_lib import writefile

#*************************************************************************

def clean_inputs(antibody, antigen, ab_filename, ag_filename):
   """
   Clean input files for entry into haddock.
   """
   print("Cleaning input files...", end='')
   # clean antibody file using pdb_chain and pdb_seg
   subprocess.run([f"~/DockingSoftware/pdb-tools/pdbtools pdb_chain.py {antibody} | ~/DockingSoftware/pdb-tools/pdbtools/pdb_seg.py | pdbrenum > {ab_filename}_clean.pdb"], shell=True)
   # Clean antigen file using pdb_chain and pdb_seg
   subprocess.run([f"~/DockingSoftware/pdb-tools/pdbtools pdb_chain.py {antigen} | ~/DockingSoftware/pdb-tools/pdbtools/pdb_seg.py > {ag_filename}_clean.pdb"], shell=True)
   print("Done")

#*************************************************************************

def generate_unambig_tbl(ab_filename):
   # Define clean antibody filename
   ab_clean = ab_filename + "_clean.pdb"
   # Run restrain_bodies script on antibody file to generate unambig restraints table
   subprocess.run([f"~/DockingSoftware/haddock-tools/restrain_bodies.py {ab_clean} > antibody-antigen-unambig.tbl"], shell=True)

#*************************************************************************

def generate_run_param(ab_filename, ag_filename, OUTPath):
   """
   Write run.param file for haddock.
   """
   # Define list of lines for run.param
   lines = ["HADDOCK_DIR=/home/oliverh/DockingSoftware/haddock2.4", "N_COMP=2", f"PDB_FILE1={OUTPath}{ab_filename}_clean.pdb", f"PDB_FILE2={OUTPath}{ag_filename}_clean.pdb", "PROJECT_DIR=./", "PROT_SEGID_1=A", "PROT_SEGID_2=B", "RUN_NUMBER=1", "UNAMBIG_TBL=antibody-antigen-unambig.tbl"]
   # Write run.param file
   writefile("run.param", lines)

#*************************************************************************

def get_his_protonation(PDBfile):
   """
   Run an input PDB file through the molprobity script provided by Haddock to determine the protonation state of histidines, save protonation states (if HisD or HisE) in a dictionary.
   """
   # Initialise res_e list
   res_e = []
   # Initialise res_d list
   res_d = []
   # Initialise full list
   full_list = []
   # Run molprobity on file, save output
   protonation = subprocess.check_output([f"~/DockingSoftware/haddock-tools/molprobity.py {PDBfile}"], shell=True)
   # Decode output
   protonation = str(protonation, 'utf-8')
   # Split output into list
   protonation = protonation.split('\n')
   # Search output for hisD or hisE
   for line in protonation[2:]:
      if 'HISE' in line:
         line.split(' ')
         res_e += [line[2]]
      if 'HISD' in line:
         line.split(' ')
         res_d += [line[2]]
   # If res_d not empty
   if res_d:
      # Add contents of res_d to full_list
      for item in res_d:
         full_list += [f"{item} - HISD"]
   # If res_e not empty
   if res_e:
      # Add contents of res_e to full_list
      for item in res_e:
         full_list += [f"{item} - HISE"]
   # If full_list not empty return contents
   if full_list:
      return full_list
   else:
      print("No HisE or HisD residues.")

#*************************************************************************

def edit_run_cns()