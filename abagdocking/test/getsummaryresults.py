#!/usr/bin/env python3
"""
Program: getsummaryresults
File:    getsummaryresults.py

Version:  V1.0
Date:     16.12.21
Function: Read the results file from testdockignprogs_master and extract the summary results for evaluation of docking programs across all targets.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes the results file from testdockingprogs_master as input and extracts the summary results from the file footer, returning them as individual results to the command line so they can be collated into a final results file.

--------------------------------------------------------------------------

Usage:
======
getsummaryresults.py results_file

--------------------------------------------------------------------------

Revision History:
=================
V1.0   12.11.21   Original   By: OECH

"""

#*************************************************************************

# Import libraries
import sys, itertools, os

#*************************************************************************

# Define input file
result_file = sys.argv[1]

#*************************************************************************

# Get input filename
inputfilename = os.path.basename(result_file).split('_dockingresults_')[0]
result_date = os.path.basename(result_file).split('_dockingresults_')[1]

#*************************************************************************

# Define lists of method indices
megadock_index = []
piper_index = []
rosetta_index = []

# Define lists of method results
megadock_results = []
piper_results = []
rosetta_results = []
all_methods = [megadock_results, piper_results, rosetta_results]

# Define list of summary results
summary_results = []

# Open input file
with open(result_file) as file:
   # Split into lines
   rows = file.readlines()
   # Get the index of method names, summary results header
   # Start cycler
   rows_cycle = itertools.cycle(rows)
   next(rows_cycle)
   for line in rows:
      # Define next line
      next_line = next(rows_cycle)
      # Megadock
      if 'Megadock-4.1.1' in line and 'Scores:' in next_line:
         megadock_index += [rows.index(line)]
      # Piper
      if 'Piper 2.0.0' in line and 'Scores:' in next_line:
         piper_index += [rows.index(line)]
      # Rosetta
      if 'Rosetta 3.13' in line and 'Scores:' in next_line:
         rosetta_index += [rows.index(line)]
      # Summary scores
      if 'Summary Evalutation Metrics' in line:
         summary_index = rows.index(line)
# Extract Method results
# Megadock
for index in megadock_index:
   with open(result_file) as file:
      megadock_results += [file.readlines()[index:(index+9)]]
# Piper
for index in piper_index:
   with open(result_file) as file:
      piper_results += [file.readlines()[index:(index+10)]]
# Rosetta
for index in rosetta_index:
   with open(result_file) as file:
      rosetta_results += [file.readlines()[index:(index+9)]]
# Extract summary results
with open(result_file) as file:
   summary_results += [file.readlines()[summary_index:]]

# Print input file name and date of test
print(f"Docking test on {inputfilename} | {result_date}")
print(f"===================================")
print("")

# Print Method results
for method in all_methods:
   i = 1
   for result in method:
      print(f"run{i}")
      i = i+1
      for line in result:
         print(line.strip('\n'))
      print("")

# Print Summary result
for result in summary_results:
   for line in result:
      print(line.strip('\n'))