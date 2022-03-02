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
   subprocess.run([f"/home/oliverh/DockingSoftware/pdb-tools/pdbtools/pdb_chain.py {antibody} | /home/oliverh/DockingSoftware/pdb-tools/pdbtools/pdb_seg.py | pdbrenum > {ab_filename}_clean.pdb"], shell=True)
   # Clean antigen file using pdb_chain and pdb_seg
   subprocess.run([f"/home/oliverh/DockingSoftware/pdb-tools/pdbtools/pdb_chain.py {antigen} | /home/oliverh/DockingSoftware/pdb-tools/pdbtools/pdb_seg.py > {ag_filename}_clean.pdb"], shell=True)
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

def edit_run_cns(long=True):
   """
   Edit the run.cns file to change length of run. HADDOCK2.4 automatically determines protonation states as default >:( )
   """
   # Initiate new list of file contents
   run_cns_out = []
   # Open run.cns file
   run_cns = "./run1/run.cns"
   # If long = false]
   if not long:
      with open(run_cns) as file:
         lines = file.readlines()
      # Change length of run (if long = False)
         for row in lines:
            if 'structures_0=' in row:
               run_cns_out += ['{===>} structures_0=200;']
            if 'structures_1=' in row:
               run_cns_out += ['{===>} structures_1=10;']
            if 'anastruc_1=' in row:
               run_cns_out += ['{===>} anastruc_1=10;']
            else:
               run_cns_out += [row]
      # write new run.cns file
      writefile(run_cns, run_cns_out)

#*************************************************************************

def extract_best_results(inputfilename):
   """
   Extract two result files, one for the best structure with waters simulated and one for the best structure excluding waters.
   """
   # Find best non waters result
   file_list_nowaters = "./run1/structures/it1/file.list"
   with open(file_list_nowaters) as file:
      rows = file.readlines()
      best_result_nw = rows[0]
      best_result_nw = best_result_nw.split()[0].split(':')[1].split('"')[0]

   # Copy best no waters result to starting directory, give it new name
   subprocess.run([f"cp ./run1/structures/it1/{best_result_nw} ./{inputfilename}_Haddock_nowaters_result.pdb"], shell=True)

   # Find the best waters result
   file_list_waters = "./run1/structures/it1/water/file.list"
   with open(file_list_waters) as file:
      rows = file.readlines()
      best_result_w = rows[0]
      best_result_w = best_result_w.split()[0].split(':')[1].split('"')[0]

   # Copy best waters result to starting directory, giving it new name
   subprocess.run([f"cp ./run1/structures/it1/water/{best_result_w} ./{inputfilename}_Haddock_waters_result.pdb"], shell=True)
