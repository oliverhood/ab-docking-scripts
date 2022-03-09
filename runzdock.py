#!/usr/bin/env python3
"""
Program: runzdock
File:    runzdock.py

Version: V1.0
Date:    13.12.21 
Function: Run input antibody and antigen files through the Zdock docking algorithm and extract the top-ranked docked ligand into a new PDB file.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a receptor (antibody), ligand (antigen), and their bound complex as input. The residues at the binding interface between the proteins is determined and non-interface residues are 'blocked' using the blockNIres program

--------------------------------------------------------------------------

Usage:
======
runzdock.py receptorfile ligandfile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   13.12.21   Original   By: OECH


"""

#*************************************************************************

# Import libraries

import sys, os, subprocess

#*************************************************************************

# Define input files

# Define receptor (antibody) file
receptor = sys.argv[1]
# Define ligand (antigen) file
ligand = sys.argv[2]
# Get output path from command line (if present)
OUTPath = ''
try:
   OUTPath = sys.argv[3] + '/'
except IndexError:
   OUTPath = './'

#*************************************************************************

# Add hydrogens to input files

# Get input file basename
filenamecontents = os.path.basename(receptor).split('.')[0].split('_')
inputfilename = filenamecontents[0] + "_" + filenamecontents[1]
# Define output antibody file name
antibody_hydrogens = OUTPath + inputfilename + "_ab_hydrogens.pdb"
# Define output antigen file name
antigen_hydrogens = OUTPath + inputfilename + "_ag_hydrogens.pdb"
# Antibody file
subprocess.run([f"pdbhadd -a {receptor} {antibody_hydrogens}"], shell=True)
# Antigen file
subprocess.run([f"pdbhadd -a {ligand} {antigen_hydrogens}"], shell=True)

#*************************************************************************

# Run zdock
subprocess.run([f"~/DockingSoftware/zdock3.0.2/zdock -R {antibody_hydrogens} -L {antigen_hydrogens} -o {OUTPath}zdock.out"], shell=True)

#*************************************************************************

# Run zrank
subprocess.run([f"~/DockingSoftware/zdock3.0.2/zrank {OUTPath}zdock.out 1 2000"], shell=True)

# Extracting top ranked output
# Initiate min out variable
min_out = 0

# Read Zrank out file
with open(f'{OUTPath}zdock.out.zr.out') as file:
   # Read lines
   rows = file.readlines()
   # Identify highest scoring output
   for line in rows:
      contents = line.split()
      if float(contents[1]) < min_out:
         min_out = float(contents[1])
         # Get number of the top hit
         top_hit = contents[0]

# Print top_hit incase structures weren't generated (next block)
print(f"Best ZRANK hit is : {top_hit}")

#*************************************************************************

# Create output Dag files (up to number of top hit)

if int(top_hit) <= 2000:
   # Copy create_lig to directory
   subprocess.run([f"cp ~/DockingSoftware/zdock3.0.2/create_lig {OUTPath}"], shell=True)
   # Make create_lig executable
   subprocess.run([f"chmod +rwx {OUTPath}/create_lig"], shell=True)
   # Change directory to outpath
   subprocess.run([f"cd {OUTPath}"])
   # Run create.pl
   subprocess.run([f"~/DockingSoftware/zdock3.0.2/create.pl zdock.out {top_hit}"], shell=True)
   
   # Define best hit filename
   top_hit_filename = f"complex.{top_hit}.pdb"
   
   # Create combined resultfile including tophit as docked antigen

   # Output filename
   resultfile = OUTPath + inputfilename + "_ZDOCK_ranked_result.pdb"
   # Open antibody file
   with open(receptor) as file:
      # Extract contents
      ab = file.readlines()
   # Open docked antigen file
   with open(top_hit_filename) as file:
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
else:
   print("Top hit is above result 2000 - handle separately")

#*************************************************************************

# Tidy up unecessary files
subprocess.run(["rm ./complex*"], shell=True)