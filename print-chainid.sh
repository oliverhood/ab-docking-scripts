#! /bin/sh
for file in /serv/data/af2/cleanpdbstructures/*.pdb
do
for agfile in "grep ;CHAIN A' $file"
	do
	chainid=$(grep 'CHAIN A' $file | awk '{print $5}')
	echo $chainid
	done
done