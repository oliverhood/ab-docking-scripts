#!/bin/bash

# Aim: run piper on the abdbid dataset
# Input: ../repr_abdbid.txt

ABDB=/acrm/bsmhome/ucbtiue/Dataset/AbDb
DATA=../repr_abdbid.txt
SCRIPT=/acrm/bsmhome/ucbtiue/UCL/projects/abagdocking/ab-docking-scripts/abagdocking/piper/run_piper.py
OUTDIR=$(dirname $(realpath $0))/out
mkdir -p $OUTDIR

# conda
conda init bash > /dev/null 2>&1
source ~/.bashrc
conda activate abagdocking

# ------------------------------------------------------------------------------
# remaining AbDb complexes to process
# ------------------------------------------------------------------------------
# load the abdb ids
abdbIDs=($(cat $DATA))
echo "Total number of abdbids: ${#abdbIDs[@]}"

# find the success and fail ids
successIDs=()
failIDs=()
if [ -f $OUTDIR/success.txt ]; then
  successIDs=($(cat $OUTDIR/success.txt))
fi
if [ -f $OUTDIR/fail.txt ]; then
  failIDs=($(cat $OUTDIR/fail.txt))
fi
echo "Success: ${#successIDs[@]}"
echo "Failed : ${#failIDs[@]}"

# update abdbIDs
abdbIDs=($(comm -23 <(printf "%s\n" "${abdbIDs[@]}" | sort) <(printf "%s\n" "${successIDs[@]}" "${failIDs[@]}" | sort)))
N=${#abdbIDs[@]}
echo "Remaining number of abdbids to process: ${N}"

# ------------------------------------------------------------------------------
# run
# ------------------------------------------------------------------------------
i=0
for abdbid in ${abdbIDs[@]}; do
  echo "Processing $abdbid"
  # create the interim directory
  outDir=$OUTDIR/${abdbid}
  interimDir=$OUTDIR/${abdbid}/interim
  mkdir -p $interimDir
  # split the compelx structure into ab and ag
  split_abag_chains $ABDB/pdb${abdbid}.mar \
    -o $interimDir > $outDir/$abdbid.log 2>&1
  python $SCRIPT \
    -c $ABDB/pdb${abdbid}.mar \
    -r $interimDir/pdb${abdbid}_ab.pdb \
    -l $interimDir/pdb${abdbid}_ag.pdb \
    -o $outDir >> $outDir/$abdbid.log 2>&1

  # Capture the return code
  retCode=$?

  echo "[$((++i))/$N] ${abdbid} done"

  # if the job is done and retCode is 0, echo the id to success.txt, otherwise to fail.txt
  if [ $retCode -eq 0 ]; then
    echo $abdbid >> $OUTDIR/success.txt
  else
    echo $abdbid >> $OUTDIR/fail.txt
  fi

done
