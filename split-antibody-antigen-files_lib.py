#!/usr/bin/env python3
"""
Program: split-antibody-antigen-files
File:    split-antibody-antigen-files.py

Version: V1.0
Date: 04.11.21
Function: Extract and process antigen and antibody chains from a PDB file 
          for input to docking algorithms.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody (that
may or may not be bound by an antigen(s)) and returns the antibody and 
antigen(s) chains as separate PDB files. The antigen chain is processed 
(randomly rotated and transformed) before being written to the new PDB 
file.

--------------------------------------------------------------------------

Usage:
======
split-antibody-antigen-files PDBFILE

--------------------------------------------------------------------------

Revision History:
=================
V1.0   04.11.21   Original   By: OECH
"""

#*************************************************************************

# Import Libraries
import sys
from bioptools import (pdbgetchain, pdbtranslate, pdbrotate)
import Bio.PDB

#*************************************************************************

