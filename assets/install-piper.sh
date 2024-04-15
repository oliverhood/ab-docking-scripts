#!/bin/bash

# Aim: install piper

shellName=$(basename $SHELL)

# init conda
source ~/.${shellName}rc
conda init $shellName > /dev/null 2>&1

# create a py27 environment
conda create -n piper-py27 python=2.7 -y

# config
BASE=$(dirname $(realpath $0))

# install pdb2pqr
conda activate piper-py27
mkdir -p $BASE/docking-tools
tar -zxf haddock.tar.gz -C $BASE/docking-tools/
tar -zxf piper.tar.gz -C $BASE/docking-tools/
pushd docking-tools/piper/pdb2pqr-1.9.0
python scons/scons.py install
popd

# link the piper executable to PATH and make it executable
ln -s $BASE/docking-tools/piper/piper $CONDA_PREFIX/bin/piper
