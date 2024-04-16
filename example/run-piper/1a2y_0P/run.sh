#!/bin/bash

conda init bash >/dev/null 2>&1
source ~/.bashrc
conda activate abagdocking

OUTDIR=$(dirname $(realpath $0))
SCRIPT="/acrm/bsmhome/ucbtiue/UCL/projects/abagdocking/ab-docking-scripts/abagdocking/piper/run_piper.py"
abdbid="1a2y_0P"

echo "Processing $abdbid"

# create the interim directory
outDir=$OUTDIR
interimDir=$outDir/interim
mkdir -p $interimDir

# split the compelx structure into ab and ag
split_abag_chains $ABDB/pdb${abdbid}.mar \
  -o $interimDir > $outDir/$abdbid.log 2>&1

python $SCRIPT \
  -c $ABDB/pdb${abdbid}.mar \
  -r $interimDir/pdb${abdbid}_ab.pdb \
  -l $interimDir/pdb${abdbid}_ag.pdb \
  -o $outDir >> $outDir/$abdbid.log 2>&1
