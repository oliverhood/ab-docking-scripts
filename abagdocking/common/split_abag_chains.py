#!/usr/bin/env python3
"""
Program: splitantibodyantigenchains
File:    splitantibodyantigenchains.py

Version:  V1.0
Date:     04.11.21
Function: Extract and process antigen and antibody chains from a PDB file
          for input to docking algorithms.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes a PDB file containing the structure of an antibody (that may or may not be bound by an antigen(s)) and returns the antibody and antigen(s) chains as separate PDB files. The antigen chain is processed (randomly rotated and transformed) before being written to the new PDB file.

--------------------------------------------------------------------------

Usage:
======
splitantibodyantigenchains.py PDBFILE OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   08.11.21   Original   By: OECH
"""
# Import Libraries
# basic
from pathlib import Path
from loguru import logger
import argparse, textwrap
from abagdocking.common.split_abag_chains_lib import (
    get_antigen_chain_label,
    extract_antibody_chains,
    extract_antigen_chain,
)


# ==================== Function ====================
def main(args: argparse.Namespace):
    # process arguments
    pdb_file: Path = args.pdb_file
    outdir: Path = args.outdir

    # create output directory
    outdir.mkdir(exist_ok=True, parents=True)

    # extract antigen chains from PDB file
    ag_chain_label = get_antigen_chain_label(pdb_file)
    logger.info(f"Antigen chain label: {ag_chain_label}")

    # Filter out files with multiple or no antigen chains
    if ag_chain_label != "Multiple chains" and ag_chain_label != "No chains":
        # Extract antibody chains from PDB
        ab_chain = extract_antibody_chains(str(pdb_file))

        # Extract and process antigen chain from PDB
        ag_chain = extract_antigen_chain(str(pdb_file))

        ab_filepath = outdir / f"{pdb_file.stem}_ab.pdb"
        ag_filepath = outdir / f"{pdb_file.stem}_ag.pdb"

        with open(ab_filepath, "w") as f:
            f.write(ab_chain)
        with open(ag_filepath, "w") as f:
            f.write(ag_chain)


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Filter out problematic AbM numbered file identifiers.",
        epilog=textwrap.dedent(
            """
            Example usage:
                python split_abag_chains.py 6x29.pdb -o /path/to/output
        """
        ),
    )
    parser.add_argument("pdb_file", type=Path, help="Path to the pdb file")
    parser.add_argument(
        "-o", "--outdir", type=Path, default=Path.cwd(), help="The output directory"
    )

    args = parser.parse_args()

    return args


def app():
    main(cli())


# ==================== Main ====================
if __name__ == "__main__":
    app()
