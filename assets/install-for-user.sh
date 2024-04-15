#!/bin/zsh

set -e


# Aim: install bioplib and bioptools
# Dependencies: conda

# Function to print timestamp
print_timestamp() {
  date +"%Y%m%d-%H%M%S"  # e.g. 20240318-085729
}

# print message with time
print_msg() {
  # level: INFO, WARNING, ERROR default INFO
  level=${2:-INFO}
  >&2 echo "[$level] $(print_timestamp): $1"  # send to stderr
}

condaEnv=${1:-base}
BASE=$(dirname $(realpath $0))  # /path/to/.devconatiner/assets
SHELLTYPE=$(basename $SHELL)  # bash or zsh
optDir=$HOME/opt
mkdir -p $optDir

# decompress
pushd $BASE
tar -zxf bioptools-V1.10.tar.gz
tar -zxf bioplib-V3.11.tar.gz
tar -zxf fftw-3.3.10.tar.gz
tar -zxf zrank_linux_64bit.tar.gz  # => zrank_linux_64bit
tar -zxf DockQ.tar.gz  # => DockQ
popd

# ------------------------------------------------------------------------------
# libxml2
# ------------------------------------------------------------------------------
print_msg "Installing libxml2..."
# install libxml2
conda install libxml2 -y
# add lib to LD_LIBRARY_PATH
export LD_LIBRARY_PATH="${CONDA_PREFIX}/lib:${LD_LIBRARY_PATH}"
# echo a message to user to add the above line to .bashrc or .zshrc
echo "You might want to add the following line to your .${SHELLTYPE}rc"
echo "export LD_LIBRARY_PATH=\"\${CONDA_PREFIX}/lib:\${LD_LIBRARY_PATH}\" >> ~/.${SHELLTYPE}rc"

# ------------------------------------------------------------------------------
# bioplib
# ------------------------------------------------------------------------------
print_msg "Installing bioplib..."
pushd $BASE/bioplib-3.11/src
# change installation directory
sed -i "s|DEST=\${HOME}|DEST=$optDir/bioplib|g" Makefile
make
make install
make installdata
echo "export DATADIR=$HOME/data" >> ~/.${SHELLTYPE}rc
popd


# ------------------------------------------------------------------------------
# bioptools
# ------------------------------------------------------------------------------
print_msg "Installing bioptools..."
pushd $BASE/bioptools-1.10/src
./makemake.pl -install=$optDir/bioptools \
    -libdir=$optDir/bioplib/lib \
    -incdir=$optDir/bioplib/include \
    -bindir=$HOME/local/bin \
    -datadir=$optDir/bioptools/data
# add the library to the CFLAGS
oldCFLAGS=$(grep "^CFLAGS" Makefile)
newCFLAGS="$oldCFLAGS -L$CONDA_PREFIX/lib"
sed -i "s|$oldCFLAGS|$newCFLAGS|g" Makefile
make
make install
popd


# ------------------------------------------------------------------------------
# fftw
# ------------------------------------------------------------------------------
print_msg "Installing fftw..."
pushd $BASE/fftw-3.3.10
./configure --enable-float --enable-sse2 --prefix=$optDir/fftw
make
make install
popd

# ------------------------------------------------------------------------------
# zrank
# ------------------------------------------------------------------------------
print_msg "Installing zrank..."
cp zrank_linux_64bit/zrank $HOME/local/bin/zrank


# ------------------------------------------------------------------------------
# DockQ
# ------------------------------------------------------------------------------
print_msg "Installing DockQ..."
pushd $BASE/DockQ
pip install .
popd

# ------------------------------------------------------------------------------
# cleanup
# ------------------------------------------------------------------------------
print_msg "Cleaning up..."
rm -rf bioptools-1.10
rm -rf bioplib-3.11
rm -rf fftw-3.3.10
rm -rf zrank_linux_64bit
rm -rf DockQ