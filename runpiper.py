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
runpiper.py receptorfile ligandfile OUTPath

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

# Define receptor (antibody) file
receptor = sys.argv[1]

# Define ligand (antigen) file
ligand = sys.argv[2]

# Get outpath from command line (if present)
OUTPath = './'
try:
   OUTPath = sys.argv[3] + '/'
except IndexError:
   OUTPath = './'

#*************************************************************************

# Process input files

# Process receptor
subprocess.run([f"~/DockingSoftware/piper/protein_prep/prepare.py {receptor}"], shell=True)
# Get original receptor file name
receptor_name = os.path.basename(receptor).split('.')[0]
# Define processed receptor filename
receptor_processed = OUTPath + receptor_name + "_pnon.pdb"

# Process ligand
subprocess.run([f"~/DockingSoftware/piper/protein_prep/prepare.py {ligand}"], shell=True)
# Get original ligand file name
ligand_name = os.path.basename(ligand).split('.')[0]
# Define processed ligand filename
ligand_processed = OUTPath + ligand_name + "_pnon.pdb"

#*************************************************************************

# Run piper on processed files
subprocess.run([f"~/DockingSoftware/piper/piper -p ~/DockingSoftware/piper/prms/atoms.prm -f ~/DockingSoftware/piper/prms/coeffs.0.0.6.antibody.prm -r ~/DockingSoftware/piper/prms/rots.prm {receptor_processed} {ligand_processed}"], shell=True)

#*************************************************************************

# Process piper output files

# Create pairwise RMSD matrices
subprocess.run([f"sblu measure pwrmsd -n 1000 --only-CA --only-interface --rec {receptor_processed} -o clustermat.000.00 {ligand_processed} ft.000.00 ~/DockingSoftware/piper/prms/rots.prm"], shell=True)

# Run clustering on the matrix
subprocess.run([f"sblu docking cluster -o clustermat.000.00.clusters clustermat.000.00"], shell=True)

# Generate cluster centers without minimising models
subprocess.run([f"sblu docking gen_cluster_pdb -l 1 clustermat.000.00.clusters ft.000.00 ~/DockingSoftware/piper/prms/rots.prm {ligand_processed} -o lig.000"], shell=True)

# Output PDB file will always be called 'lig.000.00.pdb'

#*************************************************************************

# Remove unneeded files (keeping ft.000.00 bc it takes so long to generate, better safe than sorry!)
subprocess.run([f"rm clustermat.000.00 clustermat.000.00.clusters"], shell=True)