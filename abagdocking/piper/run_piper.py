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

# abagdocking
import abagdocking
from abagdocking.utils.maskNIres import main as mask_ni_res
from abagdocking.utils.util import call_script, timing_context, temporarily_change_dir, skip_if_output_exists

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
def prepare_input_file(file: Path, output_dir: Path) -> Path:
    logger.debug(f"Preparing input file: {file}")
    run_ret = call_script([
        str(SCRIPTS_CONFIG["prepare"]),
        str(file)
    ])
    file_original = file.parent / f"{file.stem}_pnon.pdb"
    file_processed = output_dir / f"{file.stem}_pnon.pdb"
    logger.debug(f"Original file: {file_original}")
    logger.debug(f"Processed file: {file_processed}")
    # if file_processed is not file_original then remove original
    if file_original != file_processed:
        if file_processed.exists():
            os.unlink(file_processed)
        shutil.move(file_original, output_dir)
    return file_processed


def mask_non_interface_residues(
    complex: Path, receptor: Path, ligand: Path, outdir: Path
) -> Path:
    """Mask non-interface residues."""
    logger.info("Masking non-interface residues ...")
    with timing_context("masking non-interface residues"):
        masked_filepath = mask_ni_res(
            complex=complex,
            receptor=receptor,
            ligand=ligand,
            outdir=outdir,
        )
    logger.info(f"Done. Masked residues written to {masked_filepath}.")
    return masked_filepath


def run_piper(
    piper_executable: Path,
    maskrec: Path,
    prm_atoms: Path,
    prm_coeffs: Path,
    prm_rots: Path,
    receptor: Path,
    ligand: Path,
    work_dir: Path = None,
):
    """Run piper on processed files."""
    logger.info(f"Running piper ...")
    # turn into absolute paths
    piper_executable = piper_executable.resolve()
    maskrec = maskrec.resolve()
    prm_atoms = prm_atoms.resolve()
    prm_coeffs = prm_coeffs.resolve()
    prm_rots = prm_rots.resolve()
    receptor = receptor.resolve()
    ligand = ligand.resolve()
    work_dir = work_dir or Path.cwd()
    # run in work_dir
    with timing_context("piper"):
        with temporarily_change_dir(str(work_dir)):
            call_script(
                [
                    str(piper_executable),
                    "--maskrec",
                    str(maskrec),
                    "-p",
                    str(prm_atoms),
                    "-f",
                    str(prm_coeffs),
                    "-r",
                    str(prm_rots),
                    str(receptor),
                    str(ligand),
                ]
            )
    logger.info(f"Done.")


def gen_pairwise_rmsd_matrix(
    sblu_executable: Path,
    only_interface: bool,
    rec: Path,
    out_filepath: Path,
    ligand: Path,
    piper_out_filepath: Path,
    prm_rots: Path,
    only_CA: bool = None,
    n: int = None,
):
    only_CA = only_CA or True
    n = n or 1000
    logger.info("Creating pairwise RMSD matrices ...")
    with timing_context("creating pairwise RMSD matrices"):
        call_script(
            [
                str(sblu_executable),
                "measure",
                "pwrmsd",
                "-n",
                str(n),
                "--only-CA" if only_CA else "",
                "--only-interface" if only_interface else "",
                "--rec",
                str(rec),
                "-o",
                str(out_filepath),
                str(ligand),
                str(piper_out_filepath),
                str(prm_rots),
            ]
        )
    logger.info("Done.")


def gen_cluster_centers(
    sblu_executable: Path,
    clustermat: Path,
    piper_out_filepath: Path,
    prm_rots: Path,
    ligand: Path,
    out_prefix: Path,
):
    logger.info("Generating cluster centers without minimizing models ...")
    with timing_context("generating cluster centers without minimizing models"):
        call_script(
            [
                str(sblu_executable),
                "docking",
                "gen_cluster_pdb",
                "-l",
                "1",
                str(clustermat),
                str(piper_out_filepath),
                str(prm_rots),
                str(ligand),
                "-o",
                str(out_prefix),
            ]
        )
    logger.info("Done.")


def cluster_on_matrix(sblu_executable: Path, clustermat: Path, out_filepath: Path):
    logger.info("Clustering on the matrix ...")
    with timing_context("clustering on the matrix"):
        call_script(
            [
                str(sblu_executable),
                "docking",
                "cluster",
                "-o",
                str(out_filepath),
                str(clustermat),
            ]
        )
    logger.info("Done.")


def combine_ab_docked_ag(ab: Path, docked_ag: Path, out_filepath: Path):
    """Combine the antibody and the docked antigen into a single PDB file."""
    with open(out_filepath, "w") as f:
        for file in [ab, docked_ag]:
            with open(file) as f1:
                for l in f1:
                    # skip lines containing 'END'
                    if "END" not in l:
                        f.write(l)


def main(args):
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
    masked_filepath = interim / f"{complex_processed.stem}_maskfile.pdb"
    with skip_if_output_exists(masked_filepath) as execute:
        if execute:
            masked_filepath = mask_non_interface_residues(
                complex=complex_processed,
                receptor=receptor_processed,
                ligand=ligand_processed,
                outdir=interim,
            )

    # ----------------------------------------
    # Run PIPER
    # ----------------------------------------
    opath = interim / "ft.000.00"
    with skip_if_output_exists(opath) as execute:
        if execute:
            run_piper(
                piper_executable=PIPER,
                maskrec=masked_filepath,
                prm_atoms=SCRIPTS_CONFIG["prms"] / "atoms.prm",
                prm_coeffs=SCRIPTS_CONFIG["prms"] / "coeffs.0.0.6.antibody.prm",
                prm_rots=SCRIPTS_CONFIG["prms"] / "rots.prm",
                receptor=receptor_processed,
                ligand=ligand_processed,
                work_dir=interim,
            )

    # ----------------------------------------
    # Process piper output
    # ----------------------------------------
    opath = interim / "clustermat.000.00"
    with skip_if_output_exists(opath) as execute:
        if execute:
            gen_pairwise_rmsd_matrix(
                sblu_executable=SCRIPTS_CONFIG["sblu"],
                only_interface=True,
                rec=receptor_processed,
                out_filepath=interim / "clustermat.000.00",
                ligand=ligand_processed,
                piper_out_filepath=interim / "ft.000.00",
                prm_rots=SCRIPTS_CONFIG["prms"] / "rots.prm",
                only_CA=True,
                n=1000,
            )

    opath = interim / "clustermat.000.00.clusters"
    with skip_if_output_exists(opath) as execute:
        if execute:
            cluster_on_matrix(
                sblu_executable=SCRIPTS_CONFIG["sblu"],
                clustermat=interim / "clustermat.000.00",
                out_filepath=interim / "clustermat.000.00.clusters",
            )

    opath = interim / "lig.000.00.pdb"
    with skip_if_output_exists(opath) as execute:
        if execute:
            gen_cluster_centers(
                sblu_executable=SCRIPTS_CONFIG["sblu"],
                clustermat=interim / "clustermat.000.00.clusters",
                piper_out_filepath=interim / "ft.000.00",
                prm_rots=SCRIPTS_CONFIG["prms"] / "rots.prm",
                ligand=ligand_processed,
                out_prefix=interim / "lig.000",
            )

    # Output PDB file called 'lig.000.00.pdb'
    # ----------------------------------------
    # Combine `ab` and `docked ag` (dag)
    # ----------------------------------------
    opath = outdir / f"{complex.stem}_Piper_result.pdb"
    with skip_if_output_exists(opath) as execute:
        if execute:
            combine_ab_docked_ag(
                ab=receptor_processed,
                docked_ag=interim / "lig.000.00.pdb",
                out_filepath=outdir / f"{complex.stem}_Piper_result.pdb",
            )

    # ----------------------------------------
    # Clean up
    # ----------------------------------------
    # # Remove unneeded files (keeping ft.000.00 bc it takes so long to generate, better safe than sorry!)
    # os.unlink(interim / "clustermat.000.00")
    # os.unlink(interim / "clustermat.000.00.clusters")


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Filter out problematic AbM numbered file identifiers.",
        epilog=textwrap.dedent(
            """
        Example usage:
            python -c /path/to/complex.pdb -r /path/to/receptor.pdb -l /path/to/ligand.pdb -o /path/to/output
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
        "-o", "--outdir", type=Path, default=Path.cwd(), help="The output directory"
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


def app():
    main(cli())


def dev():
    base = Path(
        "/acrm/bsmhome/ucbtiue/UCL/projects/abagdocking/ab-docking-scripts/test/1a2y_0P"
    )
    complex = Path(
        "/acrm/bsmhome/ucbtiue/UCL/projects/abagdocking/ab-docking-scripts/test/pdb1a2y_0P.mar"
    )
    args = argparse.Namespace(
        complex=complex,
        receptor=base / "interim" / "pdb1a2y_0P_ab.pdb",
        ligand=base / "interim" / "pdb1a2y_0P_ag.pdb",
        outdir=base,
        prepare=SCRIPTS_CONFIG["prepare"],
        piper=SCRIPTS_CONFIG["piper"],
    )
    main(args)


# ==================== Main ====================
if __name__ == "__main__":
    app()
