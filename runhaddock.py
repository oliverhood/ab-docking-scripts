#!/usr/bin/env python3
"""
Program: runhaddock
File:    runhaddock.py

Version:  V1.0
Date:     15.02.2022
Function: Run input antibody and antigen files through the haddock protein docking algorithm, output a single result file.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes an antibody file and an antigen file as input for the haddock protein docking program, a single PDB file will be extracted as a result with waters included and without waters included (waters should be better?).

--------------------------------------------------------------------------

Usage:
======
runhaddock.py antibody antigen OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   15.02.22   Original   By: OECH

"""

#*************************************************************************

# Import libraries
