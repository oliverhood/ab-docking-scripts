#!/usr/bin/env python3
"""
Program: testdockingprogs_master_lib
File:    testdockingprogs_master_lib_v2.py

Version:  V2.0
Date:     24.05.23
Function: Libray: Library of functions for testdockingprogs_master which splits input file into its antibody/antigen components for input into docking algorithms, run docking algorithm then evaluate the result using ProFit.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody/antigen complex as input, splits the file into its component chains, runs these chains through a docking algorithm, then evaluates the result using the ProFit program. The docking and evaluation steps are repeated for each docking algorithm specified.

--------------------------------------------------------------------------

Usage:
======
testdockingprogs_master_v2.py PDBFile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   25.01.22   Original   By: OECH
V2.0   24.05.23   Modified for testdockingprogs_master_v2.py   By: OECH

"""

#*************************************************************************

# Import libraries
from cProfile import run
import sys, os, subprocess, time, re, statistics
from threading import Timer
from dockingtools_lib import evaluate_results, getlowestscore, gethighestscore, getnumberhits, writefile, getantigenchainid

#*************************************************************************

# MEGADOCK Function
def run_megadock(inputfilename, ab_filename, ag_filename, OUTPath_i):
   """
   Function to run megadock program.

   """
   # Print starting megadock
   print("Starting Megadock...", end='', flush=True)
   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())

   # Run Megadockranked on unblocked antibody/antigen files
   subprocess.run(["~/ab-docking-scripts/runmegadockranked.py " + ab_filename + " " + ag_filename + " " + OUTPath_i], shell=True)

   # Define output filename
   megadock_resultfile = OUTPath_i + inputfilename + "_MegadockRanked_result.pdb"

   # Print complete megadock
   print(f"Megadock docking completed.")
   print(f"Result file located at {megadock_resultfile}")


# *************************************************************************

# Piper function
def run_piper(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i):
    """
    Function to run Piper program.

    """
    # Print starting piper
    print("Starting Piper...", end='', flush=True)
    # Get date and time that method is being run at
    current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())

    # Run piper
    subprocess.run([f"~/ab-docking-scripts/runpiper.py {PDBfile} {ab_filename} {ag_filename} {OUTPath_i}"], shell=True)

    # Define output filename
    piper_resultfile = OUTPath_i + inputfilename + "_nohydrogens_Piper_result.pdb"

    # Print complete piper
    print(f"Piper docking completed.")
    print(f"Result file located at {piper_resultfile}")

#*************************************************************************


# Rosetta function
def run_rosetta(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i):
   """"
   Function to run the Rosetta program.

   """
   # Starting rosetta
   print("Starting Rosetta...", end='', flush=True)
   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())

   # Run Rosetta on input files (performing 50 runs within the program)
   subprocess.run([f"~/ab-docking-scripts/runrosetta.py {PDBfile} {ab_filename} {ag_filename} 50 {OUTPath_i}"], shell=True)

   # Define output filename
   rosetta_resultfile = OUTPath_i + inputfilename + "_Rosetta_result.pdb"


   # Print complete rosetta
   print(f"Rosetta docking completed.")
   print(f"Result file located at {rosetta_resultfile}")

#*************************************************************************

# Haddock function

def run_haddock(PDBfile, inputfilename, ab_filename, ag_filename, OUTPath_i):
   """
   Function to run haddock program (with and without waters).

   """
   # Print starting Haddock
   print("Starting Haddock...", end='', flush=True)
   # Get date and time that method is being run at
   current_time = time.strftime(r"%d.%m.%Y | %H:%M:%S", time.localtime())

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

   # Define output waters filename
   haddock_nowaters_resultfile = haddock_out + inputfilename + "_nohydrogens_Haddock_nowaters_result.pdb_split_labelled.pdb"

   # Change back to starting directory
   os.chdir(cwd)

   # Print complete haddock
   print(f"Haddock docking completed.")
   print(f"Result files located at: ")
   print(f"{haddock_waters_resultfile}")
   print(f"{haddock_nowaters_resultfile}")

#*************************************************************************
