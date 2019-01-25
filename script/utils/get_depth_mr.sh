#!/bin/bash

outdir=$1

echo -e "cell\tsequencing_depth" > $outdir/qc_metrics/sequencing_depth.txt
echo -e "cell\tmapping_rate" > $outdir/qc_metrics/mapping_rate.txt

for i in $outdir/logs/hisat2/*_aln_sum.txt; do
    depth=$(grep 'reads; of these:' $i | awk '{print $1}')
    mr=$(grep overall ${i} | awk '{print $1}' | cut -f 1 -d%)
    cell=$(echo ${i} | rev | cut -f 1 -d/ | rev)
    echo -e "${cell%_aln_sum.txt}\t${depth}" >> $outdir/qc_metrics/sequencing_depth.txt
    echo -e "${cell%_aln_sum.txt}\t${mr}" >> $outdir/qc_metrics/mapping_rate.txt
done
