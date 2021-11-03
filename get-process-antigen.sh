#! /bin/sh
for file in /serv/data/af2/cleanpdbstructures/*.pdb
do
grep 'CHAIN A' /serv/data/af2/cleanpdbstructures/$file | awk '{print $5}'
pdbgetchain $chainid /serv/data/af2/cleanpdbstructures/$file | pdbtranslate -x $(($RANDOM%50-25)) -y $(($RANDOM%50-25)) -z $(($RANDOM%50-25)) | pdbrotate -x $((($RANDOM%270)+45)) -y $((($RANDOM%270)+45)) -z $((($RANDOM%270)+45)) > $file_Ag.pdb
done
#adding comment line for test git push/pull