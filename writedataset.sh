#! /bin/sh
"""
Program: writedataset
File:    writedataset.sh

Version: V1.0
Date:    09.11.21
Function: Run splitantibodyantigenchains.py on all PDB files in specified directory

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program iterates through all the PDB files in the specified directory and uses them as input for the splitantibodyantigenchains.py script for output into a specifiec directory.

--------------------------------------------------------------------------

Usage:
======
writedataset.sh

--------------------------------------------------------------------------

Revision History:
=================
V1.0   09.11.21   Original   By: OECH

"""

#*************************************************************************

# Specify directory containing unprocessed PDB files
for file in /serv/data/af2/cleanpdbstructures/*.pdb
# Run splitantibodyantigenchains.py on files
do
~/ab-docking-scripts/splitantibodyantignechains.py $file /home/oliverh/docking-dataset
done

#*************************************************************************