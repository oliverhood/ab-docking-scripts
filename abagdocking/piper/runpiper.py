"""
Program: runpiper
File:    runpiper.py

Version:  V1.0
Date:     25.11.2021
Function: Take an antibody and an antigen file as input and run the piper docking algorithm on them.

Author: Oliver E. C. Hood

--------------------------------------------------------------------------

Description:
============
This program takes an antibody and an antigen chain as input, processes them for input into piper, runs the docking algorithm, then makes clusters of the output structures and finds the centre of the largest cluster, outputting this centre as the docking result.

--------------------------------------------------------------------------

Usage:
======
runpiper.py OG_file receptorfile ligandfile OUTPath

Note: Piper takes a long time to run (~2 hours per receptor/ligand pair) so run in background using:

nohup nice -10 runpiper.py <receptor> <ligand> <OUTPath> &> sysouts.txt &

--------------------------------------------------------------------------

Revision History:
=================
V1.0   25.11.2021   Original   By: OECH


"""

# basic
import os
import sys
import shutil
from pathlib import Path
from loguru import logger
import argparse, textwrap
# abagdocking
import abagdocking
from abagdocking.utils.util import call_script, timing_context
from abagdocking.utils.maskNIres import main as mask_ni_res

# ==================== Configuration ====================
BASE = Path(abagdocking.__file__).parent
SCRIPTS_CONFIG = {
    "prepare": BASE.parent
    / "assets"
    / "docking-tools"
    / "piper"
    / "script"
    / "run-prepare.sh",
    "piper": BASE.parent / "assets" / "docking-tools" / "piper" / "piper",
    "prms": BASE.parent / "assets" / "docking-tools" / "piper" / "prms",
    "maskNIres": BASE / "utils" / "maskNIres.py",
    "sblu": Path(shutil.which("sblu")),
}

# assert all scripts are found
for k, v in SCRIPTS_CONFIG.items():
    try:
        assert v.exists()
    except FileNotFoundError:
        logger.error(f"Cannot find the {k} script at {v}")
        sys.exit(1)


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
        "-o", "--outdir", tpye=Path, default=Path.cwd(), help="The output directory"
    )
    parser.add_argument(
        "-prepare",
        "--prepare",
        type=Path,
        default=SCRIPTS_CONFIG["prepare"],
        help="The path to the piper prepare.py",
    )
    parser.add_argument(
        "-piper",
        "--piper",
        type=Path,
        default=SCRIPTS_CONFIG["piper"],
        help="The path to the piper executable",
    )

    args = parser.parse_args()

    return args


# extract as a method
def prepare_input_file(file: Path, output_dir: Path) -> Path:
    run_ret = call_script([PREPARE, str(file)])
    file_original = file.parent / f"{file.stem}_pnon.pdb"
    file_processed = output_dir / f"{file.stem}_pnon.pdb"
    shutil.copy2(file_original, file_processed)
    # if file_processed is not file_original then remove original
    if file_original != file_processed:
        os.unlink(file_original)
    return file_processed


# ==================== Main ====================
# args = cli()
base=Path("/acrm/bsmhome/ucbtiue/UCL/projects/abagdocking/ab-docking-scripts/test")
args = argparse.Namespace(
    complex=base/"pdb1a2y_0P.mar",
    receptor=base/"pdb1a2y_0P_ab.pdb",
    ligand=base/"pdb1a2y_0P_ag.pdb",
    outdir=base,
    prepare=SCRIPTS_CONFIG["prepare"],
    piper=SCRIPTS_CONFIG["piper"],
)

# process args
complex: Path = args.complex  # original (unsplit) PDB file
receptor: Path = args.receptor  # receptor (antibody) file
ligand: Path = args.ligand  # ligand (antigen) file
outdir: Path = args.outdir
interim: Path = outdir.joinpath("interim")
interim.mkdir(exist_ok=True, parents=True)

# PIPER executable path
PREPARE: Path = args.prepare
PIPER: Path = args.piper

try:
    assert PREPARE.exists()
except FileNotFoundError:
    logger.error(f"Cannot find the prepare.py script at {PREPARE}")
    sys.exit(1)

try:
    assert PIPER.exists()
except FileNotFoundError:
    logger.error(f"Cannot find the piper executable at {PIPER}")
    sys.exit(1)

# ----------------------------------------
# Prepare input files
# ----------------------------------------
logger.info("Preparing input files ...")
complex_processed = prepare_input_file(complex, interim)
receptor_processed = prepare_input_file(receptor, interim)
ligand_processed = prepare_input_file(ligand, interim)
logger.info("Done.")

# ----------------------------------------
# Mask non-interface residues
# ----------------------------------------
logger.info("Masking non-interface residues ...")
mask_filepath = mask_ni_res(
    complex=complex_processed,
    receptor=receptor_processed,
    ligand=ligand_processed,
    outdir=interim,
)
logger.info(f"Done. Masked residues written to {mask_filepath}.")


# Run piper on processed files
# subprocess.run([f"~/DockingSoftware/piper/piper --maskrec={maskfile} -p ~/DockingSoftware/piper/prms/atoms.prm -f ~/DockingSoftware/piper/prms/coeffs.0.0.6.antibody.prm -r ~/DockingSoftware/piper/prms/rots.prm {receptor_processed} {ligand_processed}"], shell=True)
logger.info(f"Running piper ...")
with timing_context("piper"):
    call_script(
        [
            str(PIPER),
            "--maskrec",
            str(mask_filepath),
            "-p",
            str(SCRIPTS_CONFIG["prms"] / "atoms.prm"),
            "-f",
            str(SCRIPTS_CONFIG["prms"] / "coeffs.0.0.6.antibody.prm"),
            "-r",
            str(SCRIPTS_CONFIG["prms"] / "rots.prm"),
            str(receptor_processed),
            str(ligand_processed),
        ]
    )
logger.info(f"Done.")

sys.exit(0)
# TODO: continue rewriting
# ----------------------------------------
# Process piper output files
# ----------------------------------------
# Create pairwise RMSD matrices
# subprocess.run([f"sblu measure pwrmsd -n 1000 --only-CA --only-interface --rec {receptor_processed} -o clustermat.000.00 {ligand_processed} ft.000.00 ~/DockingSoftware/piper/prms/rots.prm"], shell=True)
call_script(
    [
        str(SCRIPTS_CONFIG["sblu"]),
        "measure",
        "pwrmsd",
        "-n",
        "1000",
        "--only-CA",
        "--only-interface",
        "--rec",
        str(receptor_processed),
        "-o",
        str(interim / "clustermat.000.00"),
        str(ligand_processed),
        "ft.000.00",
        str(SCRIPTS_CONFIG["prms"] / "rots.prm"),
    ]
)

# Run clustering on the matrix
# subprocess.run([f"sblu docking cluster -o clustermat.000.00.clusters clustermat.000.00"], shell=True)
call_script(
    [
        str(SCRIPTS_CONFIG["sblu"]),
        "docking",
        "cluster",
        "-o",
        str(interim / "clustermat.000.00.clusters"),
        "clustermat.000.00",
    ]
)

# Generate cluster centers without minimising models
# subprocess.run([f"sblu docking gen_cluster_pdb -l 1 clustermat.000.00.clusters ft.000.00 ~/DockingSoftware/piper/prms/rots.prm {ligand_processed} -o lig.000"], shell=True)
call_script(
    [
        str(SCRIPTS_CONFIG["sblu"]),
        "docking",
        "gen_cluster_pdb",
        "-l",
        "1",
        str(interim / "clustermat.000.00.clusters"),
        "ft.000.00",
        str(SCRIPTS_CONFIG["prms"] / "rots.prm"),
        str(ligand_processed),
        "-o",
        str(interim / "lig.000"),
    ]
)

# Output Dag PDB file will always be called 'lig.000.00.pdb'

# *************************************************************************
# ----------------------------------------
# Combine `ab` and `docked ag`
# ----------------------------------------
result_file = outdir / Path(complex).stem + "_Piper_result.pdb"

# Define Dag filename
dag_filename = "lig.000.00.pdb"

with open(result_file, "w") as f:
    for file in [receptor, dag_filename]:
        with open(file) as f1:
            for l in f1:
                # skip lines containing 'END'
                if "END" not in l:
                    f.write(l)


# ----------------------------------------
# Clean up
# ----------------------------------------
# Remove unneeded files (keeping ft.000.00 bc it takes so long to generate, better safe than sorry!)
os.unlink("clustermat.000.00")
os.unlink("clustermat.000.00.clusters")
# subprocess.run([f"rm clustermat.000.00 clustermat.000.00.clusters"], shell=True)
