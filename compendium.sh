# From the directory where this file (compendium.py) is located, execute:
topdir=`pwd`

# Clone repositories:
cd $topdir
git clone https://github.com/pcubillos/repack
cd $topdir/repack
git checkout 34d1e9e
make

cd $topdir
git clone --recursive https://github.com/pcubillos/pyratbay
cd $topdir/pyratbay
git checkout 5af22ce
make


# Download Exomol HCN data:
cd $topdir/inputs/
wget -i wget_exomol_hcn.txt
bzip2 -d *.bz2


# Repack HCN line-transition data:
cd $topdir/run
$topdir/repack/repack.py repack_HCN.cfg

# Format exomol partition functions for PyratBay:
$topdir/pyratbay/scripts/PFformat_Exomol.py \
       $topdir/inputs/1H-12C-14N__Harris.pf \
       $topdir/inputs/1H-13C-14N__Larner.pf

# Make TLI files for PyratBay:
cd $topdir/run
$topdir/pyratbay/pbay.py -c tli_HCN_compressed.cfg
$topdir/pyratbay/pbay.py -c tli_HCN_control.cfg


# Figure 1:
cd $topdir
$topdir/fig_flagging.py

# Figure 2:
cd $topdir/run
$topdir/fig_hwhm.py

# Figure 3:
cd $topdir/run
$topdir/fig_spectrum.py
