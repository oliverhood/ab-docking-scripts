#!/usr/bin/env python3
"""
Program: evaluate_interface
File:    evaluate_interface.py

Version:  V1.0
Date:     14.12.2021 
Function: Take an original PDB file containing an antibody-antigen complex and another PDB file containing a docked antibody-antigen complex as input then calculate the percentage of correctly predicted interface residues and contacts.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes two PDB files as input: one 'original' file containing an experimentally determined antibody-antigen complex structure, and one docked file containing the result of a docking algorithm. The contacts made between the antibody and antigen chains in each file are determined using chaincontacts and the percentage of correctly predicted contacts is given as output.

--------------------------------------------------------------------------

Usage:
======
evaluate_interface.py OG_file docked_file OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   14.12.2021   Original   By: OECH


"""

#*************************************************************************

# Import libraries

import sys, subprocess, os
from dockingtools_lib import getantigenchainid

#*************************************************************************

# Define inputs

# Original PDB file
OG_file = sys.argv[1]
# Docked PDB file
docked_file = sys.argv[2]
# Get output path from command line (if present)
OUTPath = './'
try:
   OUTPath = sys.argv[3] + '/'
except IndexError:
   OUTPath = './'

#*************************************************************************

# Run chaincontacts program

# Get input filename (OG_file)
OG_filename = os.path.basename(OG_file).split('.')[0]
# Get input filename (docked_file)
docked_filename = os.path.basename(docked_file).split('.')[0]

# Define OG chain contacts filename
OG_contacts = OUTPath + OG_filename + "_interface_contacts"

# Get antigen chain ID
agchainid = getantigenchainid(OG_file)

# Run chaincontacts on original PDB file
subprocess.run([f"chaincontacts -r 4.0 -x LH -y {agchainid} {OG_file} > {OG_contacts}"], shell=True)

# Define docked chain contacts file name
docked_contacts = OUTPath + docked_filename + "_interface_contacts"

# Run chaincontacts on docked PDB file
subprocess.run([f"chaincontacts -r 4.0 -x LH -y {agchainid} {docked_file} > {docked_contacts}"], shell=True)

#*************************************************************************
# Retrieving interface contacts

# OG file
# Initialise list of residue pairs
OG_res_pairs = []
OG_ab_residues = []
OG_ag_residues = []
# Initialise number of contacts, list of contacts (per pair)
OG_total_contacts = 0
OG_dict_contacts_res_pair = {}
# Get interface residues/contacts from OG_file
with open(OG_contacts) as file:
   # extract contents
   rows = file.readlines()[8:] # skip the header rows
   # Loop through each line separately
   for line in rows:
      # Extract contents
      contents = line.split()
      # Get residues (chain ID + residue ID)
      ab_res = str(f"{contents[1]}{contents[3]}")
      ag_res = str(f"{contents[6]}{contents[8]}")
      # Add residues to relevant list
      if ab_res not in OG_ab_residues:
         OG_ab_residues += [ab_res]
      if ag_res not in OG_ag_residues:
         OG_ag_residues += [ag_res]
      # Define residue pair
      res_pair = f"{ab_res}-{ag_res}"
      # Add pair to relevant list
      OG_res_pairs += [res_pair]
      # Get number of contacts
      contacts = int(contents[10])
      # Increase sum of contacts
      OG_total_contacts += contacts
      # Add number of contacts to dictionary entry for residue pair
      OG_dict_contacts_res_pair[res_pair] = contacts

# Docked file
# Initialise list of residue pairs
docked_res_pairs = []
docked_ab_residues = []
docked_ag_residues = []
# Initialise number of contacts, list of contacts (per pair)
docked_total_contacts = 0
docked_dict_contacts_res_pair = {}
# Get interface residues/contacts from OG_file
with open(docked_contacts) as file:
   # extract contents
   rows = file.readlines()[8:] # skip the header rows
   # Loop through each line separately
   for line in rows:
      # Extract contents
      contents = line.split()
      # Get residues (chain ID + residue ID)
      ab_res = str(f"{contents[1]}{contents[3]}")
      ag_res = str(f"{contents[6]}{contents[8]}")
      # Add residues to relevant list
      if ab_res not in docked_ab_residues:
         docked_ab_residues += [ab_res]
      if ag_res not in docked_ag_residues:
         docked_ag_residues += [ag_res]
      # Define residue pair
      res_pair = f"{ab_res}-{ag_res}"
      # Add pair to relevant list
      docked_res_pairs += [res_pair]
      # Get number of contacts
      contacts = int(contents[10])
      # Increase sum of contacts
      docked_total_contacts += contacts
      # Add number of contacts to dictionary entry for residue pair
      docked_dict_contacts_res_pair[res_pair] = contacts

#*************************************************************************

# Compare original vs predicted contacts

# Num. interface residues

# Original file
# Antibody interface residues
OG_total_ab_res = len(OG_ab_residues)
# Antigen interface residues
OG_total_ag_res = len(OG_ag_residues)
# Total number of interface residues
OG_total_int_res = OG_total_ab_res + OG_total_ag_res
# Residue pairs
OG_total_res_pairs = len(OG_res_pairs)

# Count of residues correctly predicted
correct_ab_res = 0
correct_ag_res = 0
correct_res_pairs = 0
# Antibody residues
for res in docked_ab_residues:
   if res in OG_ab_residues:
      correct_ab_res += 1

# Antigen residues
for res in docked_ag_residues:
   if res in OG_ag_residues:
      correct_ag_res += 1

# Residue pairs
for res_pair in docked_res_pairs:
   if res_pair in OG_res_pairs:
      correct_res_pairs += 1

# Calculate correctly predicted antibody residues
ab_res_proportion = correct_ab_res/OG_total_ab_res
# Calculate correctly predicted antigen residues
ag_res_proportion = correct_ag_res/OG_total_ag_res
# Calculate correctly predicted residue pairs
res_pair_proportion = correct_res_pairs/OG_total_res_pairs

# Calculate number of correctly predicted contacts within residue pair
# Initialise value
count_correct_num_contacts = 0
# Loop through dictionary keys
for res_pair in docked_dict_contacts_res_pair.keys():
   # Check if key is also in OG_res_pairs
   if res_pair in OG_dict_contacts_res_pair.keys():
      # Check if the number of contacts is the same
      if OG_dict_contacts_res_pair[res_pair] == docked_dict_contacts_res_pair[res_pair]:
         # Add to count of correct contacts
         count_correct_num_contacts += 1

#*************************************************************************

# Print evaluation results
print(f"Proportion of correctly predicted interface residues (0-1):")
print(f"============================================================")
print(f"Correctly predicted residue pairs:       {res_pair_proportion}")
print(f"Correctly predicted residues (antibody): {ab_res_proportion}")
print(f"Correctly predicted residues (antigen):  {ag_res_proportion}")