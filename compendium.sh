# From the directory where this file (compendium.py) is located, execute:
topdir=`pwd`

# Clone repositories:
cd $topdir
git clone https://github.com/pcubillos/repack
cd $topdir/repack
git checkout b3a5474
make

cd $topdir
git clone --recursive https://github.com/pcubillos/pyratbay
cd $topdir/pyratbay
git checkout 80fd85d
make

cd $topdir
git clone https://github.com/pcubillos/pytips
cd $topdir/pytips
make


# Download Exomol data:
cd $topdir/inputs/
wget -i wget_exomol_HCN.txt
wget -i wget_exomol_NH3.txt
bzip2 -d *.bz2

# Download HITRAN/HITEMP data:
cd $topdir/inputs
wget --user=HITRAN --password=getdata -N -i wget_hitemp_H2O.txt
unzip '*.zip'
rm -f *.zip

# Repack HCN line-transition data:
cd $topdir/run01
$topdir/repack/repack.py repack_HCN.cfg

# Format exomol partition functions for PyratBay:
$topdir/pyratbay/scripts/PFformat_Exomol.py \
       $topdir/inputs/1H-12C-14N__Harris.pf \
       $topdir/inputs/1H-13C-14N__Larner.pf

# Make TLI files for PyratBay:
cd $topdir/run01
$topdir/pyratbay/pbay.py -c tli_HCN_compressed.cfg
$topdir/pyratbay/pbay.py -c tli_HCN_control.cfg


# Figure 1:
cd $topdir
python $topdir/fig_flagging.py

# Figure 2:
cd $topdir/run01
python $topdir/fig_hwhm.py

# Figure 3:
cd $topdir/run01
python $topdir/fig_spectrum.py


# Generate partition-function files for H2O and NH3:
cd $topdir/run02
python $topdir/pf_tips_H2O-NH3.py

# Compress LBL databases:
cd $topdir/run02
$topdir/repack/repack.py repack_H2O.cfg
$topdir/repack/repack.py repack_NH3.cfg

