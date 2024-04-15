"""
Program: getfasta
File:    getfasta.py

Version:  V1.0
Date:     15.02.2022
Function: Extract fasta sequence from input pdb file and output into separate.fasta format

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file as input and extracts the sequences within it in fasta format using pdb2pir.

--------------------------------------------------------------------------

Usage:
======
getfasta.py PDBFile OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   12.11.21   Original   By: OECH

"""

import os, argparse
from pathlib import Path
import tempfile
from abagdocking.utils.util import call_script


def cli():  # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Extract fasta sequence from input pdb file and output into separate.fasta format"
    )

    # Add the positional arguments
    parser.add_argument("pdb_file", type=Path, help="Input PDB file")
    parser.add_argument(
        "-o", "--outdir", type=Path, default=Path.cwd(), help="Output path (optional)"
    )

    # Parse the command line arguments
    args = parser.parse_args()

    return args


def main(args):
    # Define output file name
    out_filepath = args.outdir / f"{args.pdb_file.stem}.fasta"

    # Run pdb2pir on input file using -f flag for fasta format
    call_script(["pdb2pir", "-f", args.pdb_file, out_filepath])


def app():
    main(cli())


if __name__ == "__main__":
    app()
