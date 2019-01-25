#!/bin/bash

outdir=$1

echo -e "cell\tfrip" > $outdir/qc_metrics/frip.txt

for i in $outdir/picard/*.bam; do
    cell=$(echo ${i} | rev | cut -f 1 -d/ | rev)
    total=$(samtools idxstats ${i} | addCols stdin | awk '{print $3}')
    peaks=$(intersectBed -a ${i} -b $outdir/aggregate/aggregated_scATAC_peaks.narrowPeak -bed -wa -u | wc -l)
    frip=$(calc $peaks/$total | awk '{print $3}')
    echo -e "${cell%_f2q30_pmd.bam}\t${frip}" >> $outdir/qc_metrics/frip.txt
done
