"""
Program: maskNIres
File     maskNIres.py

Version:  V1.0
Date:     28.11.21
Function: Write PDB file to mask non-interface residues in antibody-antigen complex when running docking algorithms.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program uses AM's findif.pl script to identify interface residues in an input antibody-antigen complex structure then uses these to write residues to a 'mask' PDB file to be used as input to docking algorithms.

--------------------------------------------------------------------------

Usage:
======

maskNIres.py OG_file Ab_file Ag_file OUTPath

--------------------------------------------------------------------------

Revision History:
=================
V1.0   28.11.21   Original   By: OECH

"""

# basic
from pathlib import Path
import argparse, textwrap

# custom
import abagdocking
from abagdocking.utils.util import call_script
from loguru import logger

# ==================== Configuration ====================
BASE = Path(abagdocking.__file__).parent
SCRIPT_CONFIG = {"find_interface": BASE / "common" / "findif.pl"}


# ==================== Function ====================
def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Filter out problematic AbM numbered file identifiers.",
        epilog=textwrap.dedent(
            """
        Example usage:
            python
        """
        ),
    )
    parser.add_argument(
        "-c", "--complex", type=Path, help="The original complex PDB file"
    )
    parser.add_argument(
        "-r", "--receptor", type=Path, help="The receptor (antibody) file"
    )
    parser.add_argument("-l", "--ligand", type=Path, help="The ligand (antigen) file")
    parser.add_argument(
        "-o",
        "--outdir",
        type=Path,
        default=Path.cwd(),
        help="The output path for the mask file",
    )
    args = parser.parse_args()

    return args


# ==================== Main ====================
def main(complex: Path, receptor: Path, ligand: Path, outdir: Path):
    outdir.mkdir(exist_ok=True, parents=True)

    # assert files exist
    assert complex.exists(), f"Complex file {complex} does not exist"
    assert receptor.exists(), f"Receptor file {receptor} does not exist"
    assert ligand.exists(), f"Ligand file {ligand} does not exist"

    # ----------------------------------------
    # Find interface residues
    # ----------------------------------------
    # Define location for interface residues file
    int_res_filepath = outdir / "int_res"

    with open(int_res_filepath, "w") as file:
        call_script(
            [
                str(SCRIPT_CONFIG["find_interface"]),
                str(complex),
                str(receptor),
                str(ligand),
            ],
            stdout=file,
        )
    logger.info(f"Interface residues written to {int_res_filepath}")

    h_int_res = []
    l_int_res = []
    # Read int_res and extract residue numbers
    with open(int_res_filepath) as file:
        # Identify heavy and light chain residues
        for l in file:
            # Heavy chain
            if "H" in l:
                # contents = re.compile("([a-zA-Z]+)([0-9]+)").match(line)
                h_int_res += [l.strip()]
            # Light chain
            if "L" in l:
                # contents = re.compile("([a-zA-Z]+)([0-9]+)").match(l)
                l_int_res += [l.strip()]

    # ----------------------------------------
    # Get PDB lines for residues not in interface
    # ----------------------------------------
    non_int_atom_lines = []
    # Opem Ab file
    with open(receptor) as file:
        for l in file:
            # Filter 'ATOM' lines
            if l.startswith("ATOM"):
                chain_label = l[21]
                res_number = int(l[22:26].strip())
                ins_code = l[26].strip()
                res_label = f"{chain_label}{res_number}{ins_code}"
                # Filter through heavy chain residues
                if chain_label == "H" and res_label not in h_int_res:
                    non_int_atom_lines += [l]
                if chain_label == "L" and res_label not in l_int_res:
                    non_int_atom_lines += [l]

    # ----------------------------------------
    # Write 'Mask' file
    # ----------------------------------------
    # Write maskfile.pdb
    with open(outdir / f"{complex.stem}_maskfile.pdb", "w") as file:
        for l in non_int_atom_lines:
            file.write(l)
    masked_file = outdir / f"{complex.stem}_maskfile.pdb"
    logger.info(f"Mask file written to {masked_file}")

    # ----------------------------------------
    # Clean up
    # ----------------------------------------
    # os.unlink(int_res_filepath)

    return masked_file


def app():
    args = cli()
    main(
        complex=args.complex,
        receptor=args.receptor,
        ligand=args.ligand,
        outdir=args.outdir,
    )


def dev():
    args = argparse.Namespace(
        complex=Path(
            "/acrm/bsmhome/ucbtiue/UCL/projects/abagdocking/ab-docking-scripts/test/outdir/pdb1a2y_0P_pnon.pdb"
        ),
        receptor=Path(
            "/acrm/bsmhome/ucbtiue/UCL/projects/abagdocking/ab-docking-scripts/test/outdir/pdb1a2y_0P_ab_pnon.pdb"
        ),
        ligand=Path(
            "/acrm/bsmhome/ucbtiue/UCL/projects/abagdocking/ab-docking-scripts/test/outdir/pdb1a2y_0P_ag_pnon.pdb"
        ),
        outdir=Path(
            "/acrm/bsmhome/ucbtiue/UCL/projects/abagdocking/ab-docking-scripts/test"
        ),
    )
    main(
        complex=args.complex,
        receptor=args.receptor,
        ligand=args.ligand,
        outdir=args.outdir,
    )


if __name__ == "__main__":
    # # dev
    # dev()
    app()
