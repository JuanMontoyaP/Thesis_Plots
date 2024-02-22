#!/bin/zsh

source ~/.zshrc
cd $1

Gromacs

# Fix periodicity
echo 1 0 | gmx trjconv \
    -s md_0_1.tpr \
    -f md_0_1.xtc \
    -o md_0_1_noPBC.xtc \
    -pbc mol \
    -center

# Calculate RMS
echo 4 4 | gmx rms \
    -s md_0_1.tpr \
    -f md_0_1_noPBC.xtc \
    -o rmsd.xvg \
    -tu ns

# Calculate gyration
echo 1 | gmx gyrate \
    -s md_0_1.tpr \
    -f md_0_1_noPBC.xtc \
    -o gyrate.xvg