#!/usr/bin/env python3
"""
Program: evaluate_results_4x_methods
File:    evaluate_results_4x_methods.py

Version:  V1.0
Date:     31.08.23
Function:   Run evaluate_interface on outputs from full suite of docking methods
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
V1.0   31.08.23   Original   By: OECH

"""

#*************************************************************************

# Import libraries
import sys, os, subprocess, json

#*************************************************************************

# Dictionary for evaluation metrics
evaluation_outputs = {}

#*************************************************************************

# Function to evaluate file
def evaluate_decoy(decoyfile, OG_file):
    output = []
    infile = decoyfile.split('.pdb')[0]
    outfile = f"{infile}_eval.txt"
    # Run evaluation script, write to results file
    subprocess.run([f"~/ab-docking-scripts/evaluate_interface.py {OG_file} {decoyfile} >> {outfile}"], shell=True) 
    # Save contents of results file to output
    with open(outfile) as file:
        contents = file.readlines()
        for line in contents:
            clean_line = line.split('\n')[0]
            output += [clean_line]
    # Delete results file (cleanliness)
    subprocess.run([f"rm {outfile}"], shell=True)
    return(output)

#*************************************************************************

# Filter through files in run3 to get complexes with completed results
list_ids = []

# Run ls > list_pdbs.txt
subprocess.run([f"cd run2; ls >> list_pdbs.txt; cd .."], shell=True)

# Open txt file
with open('run2/list_pdbs.txt') as file:
    contents = file.readlines()
    for item in contents:
        if '_Megadock' in item:
            pdb_id = item.split('_Mega')[0]
            list_ids += [pdb_id]

#*************************************************************************

# Function to collect results
def collect_results(pdb_id, run: int):
    # Process ins
    run = f"run{run}"
    OG_file = f"{run}/{item}.pdb"
    #List outs
    output_dict = {}
    outputs = []
    # Megadock
    megadock_in = f"{run}/{pdb_id}_MegadockRanked_result.pdb"
    megadock_out = evaluate_decoy(megadock_in, OG_file)
    output_dict["Megadock"] = megadock_out
    # Piper
    piper_in = f"{run}/{pdb_id}_nohydrogens_Piper_result.pdb"
    piper_out = evaluate_decoy(piper_in, OG_file)
    output_dict["Piper"] = piper_out
    # Rosetta
    rosetta_in = f"{run}/{pdb_id}_Rosetta_result.pdb"
    rosetta_out = evaluate_decoy(rosetta_in, OG_file)
    output_dict["Rosetta"] = rosetta_out
    # Haddock no waters
    haddock_nw_in = f"{run}/{pdb_id}_nohydrogens_Haddock_nowaters_result.pdb_split_labelled.pdb"
    haddock_nw_out = evaluate_decoy(haddock_nw_in, OG_file)
    output_dict["Haddock No Waters"] = haddock_nw_out
    # Haddock waters
    haddock_w_in = f"{run}/{pdb_id}_nohydrogens_Haddock_waters_result.pdb_split_labelled.pdb"
    haddock_w_out = evaluate_decoy(haddock_w_in, OG_file)
    output_dict["Haddock Waters"] = haddock_w_out
    # Write dict to list
    outputs += [output_dict]
    # Return output
    return(outputs)

#*************************************************************************

# Get results for each run for each PDB
for item in list_ids:
    # Output
    out_dict = {}
    # run0
    run0 = collect_results(item, 0)
    out_dict["run0"] = run0
    # run1
    run1 = collect_results(item, 1)
    out_dict["run1"] = run1
    # run2
    run2 = collect_results(item, 2)
    out_dict["run2"] = run2
    # Add outputs to eval_output dict
    evaluation_outputs[item] = out_dict

#*************************************************************************

# Dump to JSON
outputfilename = f"results.json"
with open(outputfilename, "w") as file:
    json.dump(evaluation_outputs, file)