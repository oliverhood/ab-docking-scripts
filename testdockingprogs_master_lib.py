#!/usr/bin/env python3
"""
Program: testdockingprogs_master_lib
File:    testdockingprogs_master_lib.py

Version:  V1.0
Date:     12.11.21
Function: Libray: Library of functions for testdockingprogs_master which splits input file into its antibody/antigen components for input into docking algorithms, run docking algorithm then evaluate the result using ProFit.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody/antigen complex as input, splits the file into its component chains, runs these chains through a docking algorithm, then evaluates the result using the ProFit program. The docking and evaluation steps are repeated for each docking algorithm specified.

--------------------------------------------------------------------------

Usage:
======
testdockingprogs_master.py PDBFile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   25.01.22   Original   By: OECH

"""

#*************************************************************************

# Import libraries
from cProfile import run
import sys, os, subprocess, time, re, statistics
from threading import Timer
from dockingtools_lib import evaluate_results, getlowestscore, gethighestscore, getnumberhits, writefile, getantigenchainid

#*************************************************************************

# MEGADOCK Function
def run_megadock(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults, MD_all, MD_ca, MD_res_pairs, MD_ab_res, MD_ag_res):
   """
   Function to run megadock program.

   """
   # Print starting megadock
   print("Starting Megadock...", end='', flush=True)
   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())
   # Name docking method for results file
   method = "Megadock-4.1.1 | CPU Single Node | ZRANK Ranked Output | " + current_time
   # Add method title to docking results
   dockingresults += [method]

   # Run Megadockranked on unblocked antibody/antigen files
   subprocess.run(["~/ab-docking-scripts/runmegadockranked.py " + ab_filename + " " + ag_filename + " " + OUTPath_i], shell=True)

   # Define output filename
   megadock_resultfile = OUTPath_i + inputfilename + "_MegadockRanked_result.pdb"

   # Evaluate Docking Result
   results = evaluate_results(PDBfile, megadock_resultfile)

   # Get result scores, add to dockingresults, list of results
   dockingresults += ["Scores:"]
   dockingresults += ["======="]
   # All atoms RMSD
   all_atoms = results[0]
   dockingresults += [all_atoms]
   # CA atoms RMSD
   CA_atoms = results[1]
   dockingresults += [CA_atoms]
   # Header for proportion results
   dockingresults += ["Proportion of correctly predicted interface residues (0-1):"]
   # Proportion of residue contact pairs
   res_pairs = results[2]
   dockingresults += [res_pairs]
   # Proportion of ab interface residues
   ab_res = results[3]
   dockingresults += [ab_res]
   # Proportion of ag interface residues
   ag_res = results[4]
   dockingresults += [ag_res]
   # Spacer
   dockingresults += [" "]

   # Get floats from result lines
   # all_atoms RMSD
   all_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", all_atoms)
   # CA atoms RMSD
   CA_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", CA_atoms)
   # Residue pairs
   res_pairs_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", res_pairs)
   # Ab residues
   ab_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ab_res)
   # Ag residues
   ag_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ag_res)

   # Add floats to summary lists
   for item in all_atoms_float:
      MD_all += [float(item)]
   for item in CA_atoms_float:
      MD_ca += [float(item)]
   for item in res_pairs_float:
      MD_res_pairs += [float(item)]
   for item in ab_res_float:
      MD_ab_res += [float(item)]
   for item in ag_res_float:
      MD_ag_res += [float(item)]

   # Print complete megadock
   print("Done")

#*************************************************************************

# Piper function
def run_piper(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults, Piper_all, Piper_ca, Piper_res_pairs, Piper_ab_res, Piper_ag_res):
   """
   Function to run Piper program.

   """
   # Print starting piper
   print("Starting Piper...", end='', flush=True)
   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())
   # Name docking method for results file
   method = "Piper 2.0.0 | " + current_time
   # Add method title to docking results
   dockingresults += [method]

   # Run piper
   subprocess.run([f"~/ab-docking-scripts/runpiper.py {PDBfile} {ab_filename} {ag_filename} {OUTPath_i}"], shell=True)

   # Define output filename
   piper_resultfile = OUTPath_i + inputfilename + "_nohydrogens_Piper_result.pdb"

   # Evaluate docking result
   results = evaluate_results(PDBfile, piper_resultfile)

   # Get result scores, add to dockingresults, list of results
   dockingresults += ["Scores:"]
   dockingresults += ["======="]
   # All atoms RMSD
   all_atoms = results[0]
   dockingresults += [all_atoms]
   # CA atoms RMSD
   CA_atoms = results[1]
   dockingresults += [CA_atoms]
   # Header for proportion results
   dockingresults += ["Proportion of correctly predicted interface residues (0-1):"]
   # Proportion of residue contact pairs
   res_pairs = results[2]
   dockingresults += [res_pairs]
   # Proportion of ab interface residues
   ab_res = results[3]
   dockingresults += [ab_res]
   # Proportion of ag interface residues
   ag_res = results[4]
   dockingresults += [ag_res]
   # Spacer
   dockingresults += [" "]

   # Get floats from result lines
   # all_atoms RMSD
   all_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", all_atoms)
   # CA atoms RMSD
   CA_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", CA_atoms)
   # Residue pairs
   res_pairs_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", res_pairs)
   # Ab residues
   ab_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ab_res)
   # Ag residues
   ag_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ag_res)

   # Add floats to summary lists
   for item in all_atoms_float:
      Piper_all += [float(item)]
   for item in CA_atoms_float:
      Piper_ca += [float(item)]
   for item in res_pairs_float:
      Piper_res_pairs += [float(item)]
   for item in ab_res_float:
      Piper_ab_res += [float(item)]
   for item in ag_res_float:
      Piper_ag_res += [float(item)]

   # Print piper complete
   print("Done")

#*************************************************************************

# Rosetta function
def run_rosetta(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults, Rosetta_all, Rosetta_ca, Rosetta_res_pairs, Rosetta_ab_res, Rosetta_ag_res):
   """"
   Function to run the Rosetta program.

   """
   # Starting rosetta
   print("Starting Rosetta...", end='', flush=True)
   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())
   # Name docking method for results file
   method = f"Rosetta 3.13 | docking_prepack_protocol.default.linuxgccrelease | docking_protocol.default.linuxgccrelease | Best I_sc score | " + current_time
   # Add method title to docking results
   dockingresults += [method]

   # Run Rosetta on input files (performing 50 runs within the program)
   subprocess.run([f"~/ab-docking-scripts/runrosetta.py {PDBfile} {ab_filename} {ag_filename} 50 {OUTPath_i}"], shell=True)

   # Define output filename
   rosetta_resultfile = OUTPath_i + inputfilename + "_Rosetta_result.pdb"

   # Evaluate Docking Result
   results = evaluate_results(PDBfile, rosetta_resultfile)

   # Get result scores, add to dockingresults, list of results
   dockingresults += ["Scores:"]
   dockingresults += ["======="]
   # All atoms RMSD
   all_atoms = results[0]
   dockingresults += [all_atoms]
   # CA atoms RMSD
   CA_atoms = results[1]
   dockingresults += [CA_atoms]
   # Header for proportion results
   dockingresults += ["Proportion of correctly predicted interface residues (0-1):"]
   # Proportion of residue contact pairs
   res_pairs = results[2]
   dockingresults += [res_pairs]
   # Proportion of ab interface residues
   ab_res = results[3]
   dockingresults += [ab_res]
   # Proportion of ag interface residues
   ag_res = results[4]
   dockingresults += [ag_res]
   # Spacer
   dockingresults += [" "]

   # Get floats from result lines
   # all_atoms RMSD
   all_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", all_atoms)
   # CA atoms RMSD
   CA_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", CA_atoms)
   # Residue pairs
   res_pairs_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", res_pairs)
   # Ab residues
   ab_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ab_res)
   # Ag residues
   ag_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ag_res)

   # Add floats to summary lists
   for item in all_atoms_float:
      Rosetta_all += [float(item)]
   for item in CA_atoms_float:
      Rosetta_ca += [float(item)]
   for item in res_pairs_float:
      Rosetta_res_pairs += [float(item)]
   for item in ab_res_float:
      Rosetta_ab_res += [float(item)]
   for item in ag_res_float:
      Rosetta_ag_res += [float(item)]

   # Rosetta complete
   print("Done")

#*************************************************************************

# ZDOCK function
def run_zdock(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults, ZDOCK_all, ZDOCK_ca, ZDOCK_res_pairs, ZDOCK_ab_res, ZDOCK_ag_res):
   """
   Function to run zdock ranked program.

   """
   # Print starting zdock
   print("Starting ZDOCK...", end='', flush=True)
   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())
   # Name docking method for results file
   method = "ZDOCK |  ZRANK Ranked Output | " + current_time
   # Add method title to docking results
   dockingresults += [method]

   # Run zdock ranked on files
   subprocess.run([f"~/ab-docking-scripts/runzdock.py {ab_filename} {ag_filename} {OUTPath_i}"], shell=True)

   # Define output filename
   zdock_resultfile = OUTPath_i + inputfilename + "_ZDOCK_ranked_result.pdb"

   # Evaluate Docking Result
   results = evaluate_results(PDBfile, zdock_resultfile)

   # Get result scores, add to dockingresults, list of results
   dockingresults += ["Scores:"]
   dockingresults += ["======="]
   # All atoms RMSD
   all_atoms = results[0]
   dockingresults += [all_atoms]
   # CA atoms RMSD
   CA_atoms = results[1]
   dockingresults += [CA_atoms]
   # Header for proportion results
   dockingresults += ["Proportion of correctly predicted interface residues (0-1):"]
   # Proportion of residue contact pairs
   res_pairs = results[2]
   dockingresults += [res_pairs]
   # Proportion of ab interface residues
   ab_res = results[3]
   dockingresults += [ab_res]
   # Proportion of ag interface residues
   ag_res = results[4]
   dockingresults += [ag_res]
   # Spacer
   dockingresults += [" "]

   # Get floats from result lines
   # all_atoms RMSD
   all_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", all_atoms)
   # CA atoms RMSD
   CA_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", CA_atoms)
   # Residue pairs
   res_pairs_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", res_pairs)
   # Ab residues
   ab_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ab_res)
   # Ag residues
   ag_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ag_res)

   # Add floats to summary lists
   for item in all_atoms_float:
      ZDOCK_all += [float(item)]
   for item in CA_atoms_float:
      ZDOCK_ca += [float(item)]
   for item in res_pairs_float:
      ZDOCK_res_pairs += [float(item)]
   for item in ab_res_float:
      ZDOCK_ab_res += [float(item)]
   for item in ag_res_float:
      ZDOCK_ag_res += [float(item)]

   # Print complete zdock
   print("Done")

#*************************************************************************

# Haddock function

def run_haddock(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i, dockingresults, Ha_all, Ha_ca, Ha_res_pairs, Ha_ab_res, Ha_ag_res, Hw_all, Hw_ca, Hw_res_pairs, Hw_ab_res, Hw_ag_res):
   """
   Function to run haddock program (with and without waters).

   """
   # Print starting Haddock
   print("Starting Haddock...", end='', flush=True)
   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())
   # Name docking method for results file
   method_waters = "Haddock2.4 | Protein-Protein Docking | Waters | " + current_time
   method_nowaters = "Haddock2.4 | Protein-Protein Docking | No Waters | " + current_time
   # Add waters method to docking results
   dockingresults += [method_waters]

   # Define haddock_out directory name
   haddock_out = f"{OUTPath_i}/haddock_out/"
   # Create 'Haddock_out' directory
   subprocess.run([f"mkdir {haddock_out}"], shell=True)
   # Move input files to haddock_out
   subprocess.run([f"cp {PDBfile} {ab_filename} {ag_filename} {haddock_out}"], shell=True)
   # Find current directory
   cwd = f"{os.getcwd()}/"
   # Change to haddock_out directory
   os.chdir(haddock_out)
   
   # Run Haddock on input files
   subprocess.run([f"~/ab-docking-scripts/runhaddock.py {ab_filename} {ag_filename} short {haddock_out}"], shell=True)

   # Define output waters filename
   haddock_waters_resultfile = haddock_out + inputfilename + "_nohydrogens_Haddock_waters_result.pdb_split_labelled.pdb"

   # Evaluate waters docking result
   results_waters = evaluate_results(PDBfile, haddock_waters_resultfile)

   # Get result scores, add to dockingresults, list of results
   dockingresults += ["Scores"]
   dockingresults += ["======="]
   # All atoms RMSD
   all_atoms = results_waters[0]
   dockingresults += [all_atoms]
   # CA atoms RMSD
   CA_atoms = results_waters[1]
   dockingresults += [CA_atoms]
   # Header for proportion results
   dockingresults += ["Proportion of correctly predicted interface residues (0-1):"]
   # Proportion of residue contact pairs
   res_pairs = results_waters[2]
   dockingresults += [res_pairs]
   # Proportion of ab interface residues
   ab_res = results_waters[3]
   dockingresults += [ab_res]
   # Proportion of ag interface residues
   ag_res = results_waters[4]
   dockingresults += [ag_res]
   # Spacer
   dockingresults += [" "]

   # Get floats from result lines
   # all_atoms RMSD
   all_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", all_atoms)
   # CA atoms RMSD
   CA_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", CA_atoms)
   # Residue pairs
   res_pairs_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", res_pairs)
   # Ab residues
   ab_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ab_res)
   # Ag residues
   ag_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ag_res)

   # Add floats to summary lists
   for item in all_atoms_float:
      Hw_all += [float(item)]
   for item in CA_atoms_float:
      Hw_ca += [float(item)]
   for item in res_pairs_float:
      Hw_res_pairs += [float(item)]
   for item in ab_res_float:
      Hw_ab_res += [float(item)]
   for item in ag_res_float:
      Hw_ag_res += [float(item)]

   # Add nowaters method to docking results
   dockingresults += [method_nowaters]

   # Define output waters filename
   haddock_nowaters_resultfile = haddock_out + inputfilename + "_nohydrogens_Haddock_nowaters_result.pdb_split_labelled.pdb"

   # Evaluate waters docking result
   results_nowaters = evaluate_results(PDBfile, haddock_nowaters_resultfile)

   # Get result scores, add to dockingresults, list of results
   dockingresults += ["Scores"]
   dockingresults += ["======="]
   # All atoms RMSD
   all_atoms = results_nowaters[0]
   dockingresults += [all_atoms]
   # CA atoms RMSD
   CA_atoms = results_nowaters[1]
   dockingresults += [CA_atoms]
   # Header for proportion results
   dockingresults += ["Proportion of correctly predicted interface residues (0-1):"]
   # Proportion of residue contact pairs
   res_pairs = results_nowaters[2]
   dockingresults += [res_pairs]
   # Proportion of ab interface residues
   ab_res = results_nowaters[3]
   dockingresults += [ab_res]
   # Proportion of ag interface residues
   ag_res = results_nowaters[4]
   dockingresults += [ag_res]
   # Spacer
   dockingresults += [" "]

   # Get floats from result lines
   # all_atoms RMSD
   all_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", all_atoms)
   # CA atoms RMSD
   CA_atoms_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", CA_atoms)
   # Residue pairs
   res_pairs_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", res_pairs)
   # Ab residues
   ab_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ab_res)
   # Ag residues
   ag_res_float = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", ag_res)

   # Add floats to summary lists
   for item in all_atoms_float:
      Ha_all += [float(item)]
   for item in CA_atoms_float:
      Ha_ca += [float(item)]
   for item in res_pairs_float:
      Ha_res_pairs += [float(item)]
   for item in ab_res_float:
      Ha_ab_res += [float(item)]
   for item in ag_res_float:
      Ha_ag_res += [float(item)]

   # Change back to starting directory
   os.chdir(cwd)

   # Print complete haddock
   print("Done")

#*************************************************************************

# Timer function
def program_prompt(program):
   """
   Function to prompt user for input (decide which docking programs to use per run, if no input is given in 10s then default is for program to run).
   """
   
   ans = 'y'

   # Define function to return run boolean
   def run_bool(ans, run=True):
      if ans == 'y':
         run=True
      if ans == 'n':
         run=False
      else:
         print("Answer yes or no")
      return run

   # Set timer
   t = Timer(10.0, run_bool(ans))

   while True:
      t.start()
      # Ask for input
      # Input string
      query = input(f"Run program? (y/n):\n")
      if query:
         ans = query[0].lower
         if query[0].lower() == '' or not ans in ['y','n']:
            print("Answer yes or no")
         else:
            run_bool(ans)
            break
      else:
         break
      t.cancel()

   # Return run
   return run