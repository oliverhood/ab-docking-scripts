#!/usr/bin/env python3
"""
Program: runpiper
File:    runpiper.py

Version:  V1.0
Date:     25.11.2021
Function: Take an antibody and an antigen file as input and run the piper docking algorithm on them.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes an antibody and an antigen chain as input, processes them for input into piper, runs the docking algorithm, then makes clusters of the output structures and finds the centre of the largest cluster, outputting this centre as the docking result.

--------------------------------------------------------------------------

Usage:
======
runpiper.py OG_file receptorfile ligandfile OUTPath

Note: Piper takes a long time to run (~2 hours per receptor/ligand pair) so run in background using:

nohup nice -10 runpiper.py <receptor> <ligand> <OUTPath> &> sysouts.txt &

--------------------------------------------------------------------------

Revision History:
=================
V1.0   25.11.2021   Original   By: OECH


"""

#*************************************************************************

# Import Libraries

import os
import sys
import subprocess

#*************************************************************************

# Define input files

# Define original (unsplit) PDB file
OG_file = sys.argv[1]

# Define receptor (antibody) file
receptor = sys.argv[2]

# Define ligand (antigen) file
ligand = sys.argv[3]

# Get outpath from command line (if present)
OUTPath = './'
try:
   OUTPath = sys.argv[4] + '/'
except IndexError:
   OUTPath = './'

#*************************************************************************

# Process input files

# Process receptor
subprocess.run([f"~/DockingSoftware/piper/protein_prep/prepare.py {receptor}"], shell=True)
# Get original receptor file name
receptor_name = os.path.basename(receptor).split('.')[0]
# Define processed receptor filename
receptor_processed = receptor_name + "_pnon.pdb"
# Move processed receptor to OUTPath directory
subprocess.run([f"mv {receptor_processed} {OUTPath}"], shell=True)
# Define new processed receptor filename
receptor_processed = OUTPath + receptor_name + "_pnon.pdb"

# Process ligand
subprocess.run([f"~/DockingSoftware/piper/protein_prep/prepare.py {ligand}"], shell=True)
# Get original ligand file name
ligand_name = os.path.basename(ligand).split('.')[0]
# Define processed ligand filename
ligand_processed = ligand_name + "_pnon.pdb"
# Move processed receptor to OUTPath directory
subprocess.run([f"mv {ligand_processed} {OUTPath}"], shell=True)
# Define new processed receptor file
ligand_processed = OUTPath + ligand_name + "_pnon.pdb"

#*************************************************************************
# Mask non-interface residues

# Write maskfile using maskNIres.py
subprocess.run([f"~/ab-docking-scripts/maskNIres.py {OG_file} {receptor} {ligand} {OUTPath}"], shell=True)

# Define maskfile name (+location)
OG_filename = os.path.basename(OG_file).split('.')[0]
maskfile = OUTPath + OG_filename + "_maskfile.pdb"


#*************************************************************************

# Run piper on processed files
subprocess.run([f"~/DockingSoftware/piper/piper --maskrec={maskfile} -p ~/DockingSoftware/piper/prms/atoms.prm -f ~/DockingSoftware/piper/prms/coeffs.0.0.6.antibody.prm -r ~/DockingSoftware/piper/prms/rots.prm {receptor_processed} {ligand_processed}"], shell=True)

#*************************************************************************

# Process piper output files

# Create pairwise RMSD matrices
subprocess.run([f"sblu measure pwrmsd -n 1000 --only-CA --only-interface --rec {receptor_processed} -o clustermat.000.00 {ligand_processed} ft.000.00 ~/DockingSoftware/piper/prms/rots.prm"], shell=True)

# Run clustering on the matrix
subprocess.run([f"sblu docking cluster -o clustermat.000.00.clusters clustermat.000.00"], shell=True)

# Generate cluster centers without minimising models
subprocess.run([f"sblu docking gen_cluster_pdb -l 1 clustermat.000.00.clusters ft.000.00 ~/DockingSoftware/piper/prms/rots.prm {ligand_processed} -o lig.000"], shell=True)

# Output Dag PDB file will always be called 'lig.000.00.pdb'

#*************************************************************************
# Combine antibody and docked antigen files to give a single output file

# Get input filename
inputfilename = os.path.basename(OG_file).split('.')[0]
# Define output file name
resultfile = OUTPath + inputfilename + "_Piper_result.pdb"
# Define Dag filename
dag_filename = "lig.000.00.pdb"
# Combine antibody and Dag files
with open(receptor) as file:
   # Extract contents
   ab = file.readlines()
   # Open docked antigen file
with open(dag_filename) as file:
   # Extract contents
   dag = file.readlines()
   # Combine antibody and docked antigen files
AbDag = ab + dag
# Write new PDB file
with open(resultfile, "w") as file:
   for line in AbDag:
   # Skip lines containing 'END'
      if 'END' not in line.strip('\n'):
         file.write(line)


#*************************************************************************

# Remove unneeded files (keeping ft.000.00 bc it takes so long to generate, better safe than sorry!)
subprocess.run([f"rm clustermat.000.00 clustermat.000.00.clusters"], shell=True)