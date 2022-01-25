#!/usr/bin/env python3
"""
Program: testdockingprogs_master_lib
File:    testdockingprogs_master_lib.py

Version:  V1.0
Date:     12.11.21
Function: Libray: Library of functions for testdockingprogs_master which splits input file into its antibody/antigen components for input into docking algorithms, run docking algorithm then evaluate the result using ProFit.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody/antigen complex as input, splits the file into its component chains, runs these chains through a docking algorithm, then evaluates the result using the ProFit program. The docking and evaluation steps are repeated for each docking algorithm specified.

--------------------------------------------------------------------------

Usage:
======
testdockingprogs_master.py PDBFile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   25.01.22   Original   By: OECH

"""