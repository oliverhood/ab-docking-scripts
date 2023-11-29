#!/usr/bin/env python3
"""
Program: rundockq
File:    rundockq.py

Version:  V1.0
Date:     29.11.2023
Function:   Run DockQ on docking outputs.
Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============


--------------------------------------------------------------------------

Usage:
======
Run in 'docking_outputs'

--------------------------------------------------------------------------

Revision History:
=================
V1.0   29.11.23   Original   By: OECH

"""

#*************************************************************************

# Import Libraries
import subprocess, json, os
from runhaddock_lib import fix_chain_labelling

#*************************************************************************

# Collect PDB IDs from files in run2

# Initiate list for IDs
list_ids = []

# Get list of filenames in run2
files = os.listdir('run2')

# Extract PDB IDs
for item in files:
   if '_Rosetta' in item:
      pdb_id = item.split('_Rosetta')[0]
      list_ids += [pdb_id]

#*************************************************************************

# Function to run DockQ
def run_dockq(model, native):
   output = []
   infile = model.split('.pdb')[0]
   outfile=f"{infile}_dockq.txt"
   # Run DockQ, write to outfile
   subprocess.run([f"dockq.sh {model} {native} -model_chain1 H L -native_chain1 H L -no_needle >> {outfile}"], shell=True)
   # Collect DockQ metrics
   with open(outfile) as file:
      contents = file.readlines()
      output += [contents[25].split('\n')[0].split(' ')[1]] # DockQ
      output += [contents[24].split('\n')[0].split(' ')[1]] # LRMS
      output += [contents[23].split('\n')[0].split(' ')[1]] # iRMS
      output += [contents[22].split('\n')[0].split(' ')[1]] # Fnonnat
      output += [contents[21].split('\n')[0].split(' ')[1]] # Fnat
   # Delete results file (cleanliness)
   subprocess.run([f"rm {outfile}"], shell=True)
   # Return out
   return(output)

#*************************************************************************
# Initiate output_dict
output_dict = {}

# Run DockQ on each run
for complex in list_ids:
   complex_dict = {} #dict for each PDB
   for i in range(3): # Add run to dict
      # Filenames
      native = f"run{i}/{complex}.pdb"
      megadock = f"run{i}/{complex}_MegadockRanked_result.pdb"
      piper = f"run{i}/{complex}_nohydrogens_Piper_result.pdb"
      rosetta = f"run{i}/{complex}_Rosetta_result.pdb"
      haddock_nw = f"run{i}/{complex}_nohydrogens_Haddock_nowaters_result.pdb"
      haddock_w = f"run{i}/{complex}_nohydrogens_Haddock_waters_result.pdb"
      # Fix haddock chain labelling
      fix_chain_labelling(native, haddock_nw)
      fix_chain_labelling(native, haddock_w)
      # Run DockQ
      dockq_results = {}
      # Megadock
      megadock_result = run_dockq(megadock, native)
      dockq_results["Megadock"] = megadock_result
      # Piper
      piper_result = run_dockq(piper, native)
      dockq_results["Piper"] = piper_result
      # Rosetta
      rosetta_result = run_dockq(rosetta, native)
      dockq_results["Rosetta"] = rosetta_result
      # Haddock no waters
      haddock_nw_result = run_dockq(haddock_nw, native)
      dockq_results["Haddock No Waters"] = haddock_nw_result
      # Haddock waters
      haddock_w_result = run_dockq(haddock_w, native)
      dockq_results["Haddock Waters"] = haddock_w_result
      # Add to complex_dict
      complex_dict[f"run{i}"] = dockq_results
   # Add complex dict to output dict
   output_dict[complex] = complex_dict

#*************************************************************************

# Dump to JSON
outputfilename = "dockq_results.json"
with open(outputfilename, "w'") as file:
   json.dump(output_dict, file)