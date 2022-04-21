#!/usr/bin/env python3
"""
Program: extract_results
File:    extract_results.py

Version:  V1.0
Date:     21.04.22
Function: Filter through the output directories of tesdockingprogs_master to extract docking results.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes the log file for a docking run as input and filters through it to find the ids of files that were entered into the docking protocol. Result files for these files are opened to extract the evaluation metrics.

--------------------------------------------------------------------------

Usage:
======
extract_results.py logfile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   21.04.22   Original   By: OECH

"""

#*************************************************************************

# Import libraries

import sys, os, subprocess, json

#*************************************************************************

# Specify input file

LOGfile = sys.argv[1]

# Get current working directory
directory = os.getcwd()
# Get output path from command line (if present)
OUTPath = directory + "/"
try:
   OUTPath = sys.argv[2] + '/'
except IndexError:
   print('No output directory specified, writing files to current directory')
   OUTPath = directory + "/"

#*************************************************************************

# Get pdb ids from input file

# Initialise list
list_ids = []

# Open log file
with open(LOGfile) as file:
   # Read lines
   rows = file.readlines()
   # Filter for files that were run
   for line in rows:
      if 'Starting docking program on' in line:
         # Get filename
         file_id = line.split(' on ')[1]
         # Add to list
         list_ids += [file_id]

#*************************************************************************

# Create dictionary for results to go into
dict_results = {}

# Get results

#Get current directory
pwd = os.getcwd()

# Move to results directory if there
for item in list_ids:
   # Get path to location of logfile
   path = os.path.dirname(os.path.realpath(LOGfile))
   # Search through contents of path for docking_results directory
   for file in os.listdir(path):
      if file.startswith('docking_results'):
         # Define docking_results directory
         docking_results = file
   # Try changing to results directory
   try:
      subprocess.run([f"cd {path}/{docking_results}/{item}/results"], shell=True)
   except:
      print("No results directory found.")
   # If cd was sucessful
   else:
      # Define results file names
      # Megadock
      MD_all_out = f"{item}_MD_all.txt"
      MD_ca_out = f"{item}_MD_ca.txt"
      MD_res_pairs_out = f"{item}_MD_res_pairs.txt"
      MD_ab_res_out = f"{item}_MD_ab_res.txt"
      MD_ag_res_out = f"{item}_MD_ag_res.txt"
      # Piper
      Piper_all_out = f"{item}_Piper_all.txt"
      Piper_ca_out = f"{item}_Piper_ca.txt"
      Piper_res_pairs_out = f"{item}_Piper_res_pairs.txt"
      Piper_ab_res_out = f"{item}_Piper_ab_res.txt"
      Piper_ag_res_out = f"{item}_Piper_ag_res.txt"
      # Rosetta
      Rosetta_all_out = f"{item}_Rosetta_all.txt"
      Rosetta_ca_out = f"{item}_Rosetta_ca.txt"
      Rosetta_res_pairs_out = f"{item}_Rosetta_res_pairs.txt"
      Rosetta_ab_res_out = f"{item}_Rosetta_ab_res.txt"
      Rosetta_ag_res_out = f"{item}_Rosetta_ag_res.txt"
      # Haddock waters
      Hw_all_out = f"{item}_Hw_all.txt"
      Hw_ca_out = f"{item}_Hw_ca.txt"
      Hw_res_pairs_out = f"{item}_Hw_res_pairs.txt"
      Hw_ab_res_out = f"{item}_Hw_ab_res.txt"
      Hw_ag_res_out = f"{item}_Hw_ag_res.txt"
      # Haddock No waters
      Ha_all_out = f"{item}_Ha_all.txt"
      Ha_ca_out = f"{item}_Ha_ca.txt"
      Ha_res_pairs_out = f"{item}_Ha_res_pairs.txt"
      Ha_ab_res_out = f"{item}_Ha_ab_res.txt"
      Ha_ag_res_out = f"{item}_Ha_ag_res.txt"
      # Extract results from files
      # Megadock
      with open(MD_all_out) as file:
         MD_all = file.readlines()
      with open(MD_ca_out) as file:
         MD_ca = file.readlines()
      with open(MD_res_pairs_out) as file:
         MD_res_pairs = file.readlines()
      with open(MD_ab_res_out) as file:
         MD_ab_res = file.readlines()
      with open(MD_ag_res_out) as file:
         MD_ag_res = file.readlines()
      megadock_dict = {"Megadock":[MD_all, MD_ca, MD_res_pairs, MD_ab_res, MD_ag_res]}
      # Piper
      with open(Piper_all_out) as file:
         Piper_all = file.readlines()
      with open(Piper_ca_out) as file:
         Piper_ca = file.readlines()
      with open(Piper_res_pairs_out) as file:
         Piper_res_pairs = file.readlines()
      with open(Piper_ab_res_out) as file:
         Piper_ab_res = file.readlines()
      with open(Piper_ag_res_out) as file:
         Piper_ag_res = file.readlines()
      piper_dict = {"Piper":[Piper_all, Piper_ca, Piper_res_pairs, Piper_ab_res, Piper_ag_res]}
      # Rosetta
      with open(Rosetta_all_out) as file:
         Rosetta_all = file.readlines()
      with open(Rosetta_ca_out) as file:
         Rosetta_ca = file.readlines()
      with open(Rosetta_res_pairs_out) as file:
         Rosetta_res_pairs = file.readlines()
      with open(Rosetta_ab_res_out) as file:
         Rosetta_ab_res = file.readlines()
      with open(Rosetta_ag_res_out) as file:
         Rosetta_ag_res = file.readlines()
      Rosetta_dict = {"Rosetta":[Rosetta_all, Rosetta_ca, Rosetta_res_pairs, Rosetta_ab_res, Rosetta_ag_res]}
      # Haddock waters
      with open(Hw_all_out) as file:
         Hw_all = file.readlines()
      with open(Hw_ca_out) as file:
         Hw_ca = file.readlines()
      with open(Hw_res_pairs_out) as file:
         Hw_res_pairs = file.readlines()
      with open(Hw_ab_res_out) as file:
         Hw_ab_res = file.readlines()
      with open(Hw_ag_res_out) as file:
         Hw_ag_res = file.readlines()
      haddock_water_dict = {"Haddock waters":[Hw_all, Hw_ca, Hw_res_pairs, Hw_ab_res, Hw_ag_res]}
      # Haddock no waters
      with open(Ha_all_out) as file:
         Ha_all = file.readlines()
      with open(Ha_ca_out) as file:
         Ha_ca = file.readlines()
      with open(Ha_res_pairs_out) as file:
         Ha_res_pairs = file.readlines()
      with open(Ha_ab_res_out) as file:
         Ha_ab_res = file.readlines()
      with open(Ha_ag_res_out) as file:
         Ha_ag_res = file.readlines()
      haddock_nowater_dict = {"Haddock no waters":[Ha_all, Ha_ca, Ha_res_pairs, Ha_ab_res, Ha_ag_res]}
      # Add results dictionaries to main dictionary
      dict_results[item] = [megadock_dict, piper_dict, Rosetta_dict, haddock_water_dict, haddock_nowater_dict]

# Write dict_results to json file
outputfilename = "results.json"
# write output json file
with open(outputfilename, "w") as file:
   json.dump(dict_results, file)