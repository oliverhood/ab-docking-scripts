#! /bin/sh
for file in /serv/data/af2/cleanpdbstructures/*.pdb
do
chainid=$(grep 'CHAIN A' $file | awk '{print $5}')
if [ -z "$chainid" ]
then
:
else
echo $chainid
fi
done