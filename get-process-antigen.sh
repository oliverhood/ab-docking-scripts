#! /bin/sh
for file in /serv/data/af2/cleanpdbstructures/*.pdb
do
chainid="grep 'CHAIN A' $file | awk '{print $5}'"
pdbgetchain $chainid $file | pdbtranslate -x $(($RANDOM%50-25)) -y $(($RANDOM%50-25)) -z $(($RANDOM%50-25)) | pdbrotate -x $((($RANDOM%270)+45)) -y $((($RANDOM%270)+45)) -z $((($RANDOM%270)+45)) > $(basename ${file##*/pdb} .pdb)_Ag.pdb
done
