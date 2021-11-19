#!/usr/bin/env python
"""
Script sent by George Jones of the Vajda Lab (ClusPRo, Piper)

george.jones@stonybrook.edu

"""
from argparse import ArgumentParser, FileType
from prody import parsePDBStream, writePDB
import numpy as np
from sblu.ft import (read_ftresults, get_ftresult, read_rotations,
                     apply_ftresult, apply_ftresults_atom_group)

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

parser = ArgumentParser(description="")
parser.add_argument("--index", "-i", default=None, type=int,
                    help="Index of ftresult to apply. Overrides '-n'")
parser.add_argument("--limit", "-n", default=None, type=int,
                    help="Index of ftresult to apply.")
parser.add_argument("--rotation", "-r", default=None, type=int,
                    help="Use ftresult with rotation index <r>")
parser.add_argument("--out-prefix", default=None,
                    help="Prefix of the output pdb file(s)")
parser.add_argument("ftfile",
                    help="")
parser.add_argument("rotations",
                    help="")
parser.add_argument("pdb_file", type=FileType('r'),
                    help="")


args = parser.parse_args()

if args.out_prefix is None:
    args.out_prefix = "output"

pdb = parsePDBStream(args.pdb_file)
rotations = read_rotations(args.rotations)

coords = pdb.getCoords()
center = np.mean(coords, axis=0)
np.subtract(coords, center, coords)

if args.index is not None:
    ftresult = get_ftresult(args.ftfile, args.index)

    coords = pdb.getCoords()
    pdb.setCoords(apply_ftresult(coords, ftresult, rotations))

    writePDB(args.out_prefix+".pdb", pdb)
elif args.rotation is not None:
    ftreults = read_ftresults(args.ftfile)

    writePDB(args.out_prefix+".pdb", pdb)
else:
    ftresults = read_ftresults(args.ftfile, limit=args.limit)

    new_ag = apply_ftresults_atom_group(pdb, ftresults, rotations)

    for i in range(new_ag.numCoordsets()):
        new_ag.setACSIndex(i)
        writePDB("{}.{}.pdb".format(args.out_prefix, i), new_ag, csets=i)


