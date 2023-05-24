#! /bin/sh
#"""

#Program: run_testdockingprogs_master_v2
#File:    run_testdockingprogs_master_v2.sh

#Version:   V2.0
#Date:      24.05.2023
#Function:  Wrapper for running testdockingprogs_master_v2.py on a full directory of PDB files.

#Author: Oliver E. C. Hood

#--------------------------------------------------------------------------

#Description:
#============
#This script loops through every PDB file in a given directory, uses them as input for testdockingprogs_master.py, then concatenates the result file for each run into a single file.

#--------------------------------------------------------------------------

#Usage:
#======


#-------------------------------------------------------------------------
#>"""
#*************************************************************************

# Get current date
now=$(date +%d_%m_%Y)

# Get the starting directory, save to variable
pwd=`pwd`

# Make directory for docking results
mkdir ${pwd}/docking_results_$now
results_dir=${pwd}/docking_results_$now

# Loop through every PDB file in current directory
for file in ${pwd}/*.pdb
   do
      # Get the file name (less .pdb)
      filename=$(basename $file .pdb)
      # Make new directory within docking_results
      mkdir $results_dir/$filename
      # Copy file to docking results directory
      cp $file $results_dir/$filename
      # Move to docking results directory
      cd $results_dir/$filename
      # Run testdockingprogs_master with docking_results as the output directory
      ~/ab-docking-scripts/testdockingprogs_master_v2.py $file
      # Return to main docking results directory
      cd $pwd
   done
