#! /bin/sh
#"""

#Program: testdockingprogs_shell
#File:    testdockingprogs_shell.sh

#Version:   V1.0
#Date:      15.12.2021
#Function:  Wrapper for running testdockingprogs_master.py on a full directory of PDB files.
 
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
      # Get current date again to find results file
      now2=$(date +%d_%m_%Y)
      # Get the file name (less .pdb)
      filename=$(basename $file .pdb)
      # Make new directory within docking_results
      mkdir $results_dir/$filename
      # Copy file to docking results directory
      cp $file $results_dir/$filename
      # Move to docking results directory
      cd $results_dir/$filename
      # Run testdockingprogs_master with docking_results as the output directory
      ~/ab-docking-scripts/testdockingprogs_master.py $file
      # Return to main docking results directory
      cd $pwd
      # Get results filename
      resultsfile=${results_dir}/${filename}/${filename}_dockingresults_${now2}.results.txt
      # Define output results_file
      output_results="dockingresult_${now}"
      # Run getsummaryresults on results file, run into results file
      ~/ab-docking-scripts/getsummaryresults.py $resultsfile >> $output_results
   done
