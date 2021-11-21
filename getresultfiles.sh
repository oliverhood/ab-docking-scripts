#! /bin/sh
"""
Program: getresultfiles
File:    getresultfiles.sh

Version:  V1.0
Date:     21.11.2021
Function: Extract result PDB files from directories created by testdockingprogs_master.py script into new directory 'result_files'

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program moves the PDB files created by multiple runs in testmegadock_vs_megadockblocked script into a single directory with runs labelled to compare docked structure results in PyMol.

--------------------------------------------------------------------------

Usage:
======

getresultfiles.sh

N.b. call this script in directory that testmegadock_vs_megadockblocked was run in

--------------------------------------------------------------------------

Revision History:
=================

"""
#*************************************************************************
# Make Directory to put docked structures in
mkdir result_files
# Loop through result directories to extract docked structures
for file in ./run*
   do
      # Copy the the megadock result
      cp ${file}/1yqv_0_abDag.pdb result_files/${file}_megadock.pdb
      # Copy the megadock blocked antibody result
      cp ${file}/1yqv_0_ab_bDag.pdb result_files/${file}_megadock_blocked_ab.pdb
      # Copy the megadock blocked antigen result
      cp ${file}/1yqv_0_ab_b1Dag.pdb result_files/${file}_megadock_blocked_ag.pdb
      # Copy the megadock ranked result
      cp ${file}/1yqv_0_ab_rDag.pdb result_files/${file}_megadock_ranked.pdb
   done
