#!/bin/sh
#BSUB -q Z-ZQF
#BSUB -o output
#BSUB -e error
#BSUB -n 8

script=script

source activate py27
source $script/env.sh

python $script/scATAC-pipe.py -n 4 -l fq_list -o test
