#!/bin/bash

outdir=$1

echo -e "cell\tlibrary_size" > $outdir/qc_metrics/library_size.txt

for i in $outdir/logs/spicard/*.out; do
    size=$(grep Unknown ${i} | cut -f 9)
    cell=$(echo ${i} | rev | cut -f 1 -d/ | rev)
    echo -e "${cell%_f2q30_pmd.out}\t${size}" >> $outdir/qc_metrics/library_size.txt
done
