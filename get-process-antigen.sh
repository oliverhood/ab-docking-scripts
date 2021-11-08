#! /bin/sh
"""
Program: get-process-antigen
File: get-process-antigen.sh

Version: V1.0
Date: 08.11.21
Function: Extract and process antigen chains from PDB files for input into docking algorithms.

Author: Oliver E.C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody (that may or may not be bound by an antigen(s)) and returns the the antibody and 
antigen(s) chains as separate PDB files. The antigen chain is processed 
(randomly rotated and transformed) before being written to the new PDB 
file.

--------------------------------------------------------------------------

Usage:
======

get-process-antigen.sh PDBFile

--------------------------------------------------------------------------

Revision History:
=================
V1.0   08.11.21   Original   By: OECH

"""

#*************************************************************************

for file in /serv/data/af2/cleanpdbstructures/*.pdb
   do
      chainid=$(grep 'CHAIN A' $file | awk '{print $5}')
      if [ -z "$chainid" ]
         then
            :
      elif
      else
         pdbgetchain $chainid $file | pdbtranslate -x $(($RANDOM%50-25)) -y $(($RANDOM%50-25)) -z $(($RANDOM%50-25)) | pdbrotate -x $((($RANDOM%270)+45)) -y $((($RANDOM%270)+45)) -z $((($RANDOM%270)+45)) > $(basename ${file##*/pdb} .pdb)_Ag.pdb ;
      fi
   done