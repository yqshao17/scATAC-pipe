#!/bin/bash

outdir=$1

echo -e "cell\tdup_level" > $outdir/qc_metrics/dup_level.txt

for i in $outdir/logs/spicard/*.out; do
    dup=$(grep Unknown ${i} | cut -f 8)
    cell=$(echo ${i} | rev | cut -f 1 -d/ | rev)
    echo -e "${cell%_f2q30_pmd.out}\t${dup}" >> $outdir/qc_metrics/dup_level.txt
done
