"""
Program: split_abag_chains_lib
File:    split_abag_chains_lib.py

Version: V1.0
Date: 04.11.21
Function:   Library:   Functions for split_abag_chains, extracts and processes antigen and antibody chains from a PDB file
          for input to docking algorithms.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody (that may or may not be bound by an antigen(s)) and returns the antibody and antigen(s) chains as separate PDB files. The antigen chain is processed (randomly rotated and transformed) before being written to the new PDB file.

--------------------------------------------------------------------------

Usage:
======
split_abag_chains.py PDBFILE OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   04.11.21   Original   By: OECH
"""

#*************************************************************************

# Import Libraries
import random
import subprocess
from abagdocking.utils.util import call_script

#*************************************************************************

def get_antigen_chain_label(pdb_file: str):
    """
    Read input file and extract the chain identifier for the antigen chain
    (if present)

    >>> get_antigen_chain_label("test/test1.pdb")
    'No chains'
    >>> get_antigen_chain_label("test/test2.pdb")
    'C'
    >>> get_antigen_chain_label("test/test3.pdb")
    'Multiple chains'
    >>> get_antigen_chain_label('test/test4.pdb')
    'C'

    """
    #Set antigen_count to zero
    antigen_count = 0
    #Open PDB file
    with open(pdb_file) as file:
       #Read rows in file
       rows = file.readlines()
       #Identify Antigen chains from PDB Header
       for line in rows:
          if 'CHAIN A' in line:
             #Increase antigen_count by 1
             antigen_count += 1
             #Split the line into individual words
             contents=line.split()
             #Extract the antigen chainid
             agchainid = contents[4]
          #Break loop when first ATOM coordinate is encountered
          if 'ATOM' in line:
             break
    #Return chainid for single antigen chain
    if antigen_count == 1:
        return agchainid
    elif antigen_count > 1:
        return 'Multiple chains'
    else:
        return 'No chains'


def extract_antibody_chains(pdb_file: str):
    """
    Search input file for the number of antigen chains then extract the antibody chains if there is a single antigen chain

    >>> extract_antibody_chains('test/test1.pdb')
    'test/test1.pdb has no antigen'
    >>> extract_antibody_chains('test/test3.pdb')
    'test/test3.pdb has multiple antigen chains'

    """
    ag_chain_label = get_antigen_chain_label(pdb_file)

    if ag_chain_label == 'Multiple chains':
        return pdb_file + ' has multiple antigen chains'
    elif ag_chain_label == 'No chains':
        return pdb_file + ' has no antigen'
    else:
        #Extract the antibody chains
        # get_antibody_chains = subprocess.run(["pdbgetchain H,L " + pdb_file], shell=True, universal_newlines=True, stdout=subprocess.PIPE)
        ret = call_script([
            'pdbgetchain',
            'H,L',
            pdb_file
        ], decode="utf-8")

    antibody_chains: str = ret['stdout']

    return antibody_chains


def extract_antigen_chain(pdb_file: str):
    """
    Search input PDB file for number of antigen chains then extract the antigen chain if there is a single antigen chain present

    >>> extract_antigen_chain("test/test1.pdb")
    'test/test1.pdb has no antigen'
    >>> extract_antigen_chain("test/test3.pdb")
    'test/test3.pdb has multiple antigen chains'

    """
    # Get the antigen's chain id
    ag_chain_label = get_antigen_chain_label(pdb_file)
    # Filter out files with multiple or no antigen chains
    if ag_chain_label == 'Multiple chains':
        return pdb_file + ' has multiple antigen chains'
    elif ag_chain_label == 'No chains':
        return pdb_file + ' has no antigen'
    else:
        # get_processed_antigen_chain = subprocess.run(["pdbgetchain " + ag_chain_label + " " + PDBfile
        # + " | pdbrotate -x " + str((random.randint(-8,8))) + " -y " + str((random.randint(-8,8))) + " -z " + str((random.randint(-8,8)))
        # + " | pdbtranslate -x " + str((random.randint(5,10))) + " -y " + str((random.randint(5,10))) + " -z " + str((random.randint(5,10)))], stdout=subprocess.PIPE, universal_newlines=True, shell=True)

        # First command: pdbgetchain
        cmd1 = ['pdbgetchain', ag_chain_label, pdb_file]
        p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)

        # Second command: pdbrotate
        rotate_args = [
            'pdbrotate',
            '-x', str(random.randint(-8, 8)),
            '-y', str(random.randint(-8, 8)),
            '-z', str(random.randint(-8, 8))
        ]
        p2 = subprocess.Popen(rotate_args, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.

        # Third command: pdbtranslate
        translate_args = [
            'pdbtranslate',
            '-x', str(random.randint(5, 10)),
            '-y', str(random.randint(5, 10)),
            '-z', str(random.randint(5, 10))
        ]
        p3 = subprocess.Popen(translate_args, stdin=p2.stdout, stdout=subprocess.PIPE)
        p2.stdout.close()  # Allow p2 to receive a SIGPIPE if p3 exits.

        output, error = p3.communicate()

        if p3.returncode != 0:
            raise subprocess.CalledProcessError(p3.returncode, translate_args)

        return output.decode("utf-8")


# Testing functions
if __name__ == "__main__":
    import doctest
    doctest.testmod()