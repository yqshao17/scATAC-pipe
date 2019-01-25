#!/bin/bash

outdir=$1

echo -e "cell\tfrac_open" > $outdir/qc_metrics/frac_open.txt

for i in $outdir/picard/*.bam; do
    total=$(wc -l $outdir/aggregate/aggregated_scATAC_peaks.narrowPeak | awk '{print $1}')
    cov=$(intersectBed -a $outdir/aggregate/aggregated_scATAC_peaks.narrowPeak -b ${i} -wa -u | wc -l)
    frac=$(calc $cov/$total | awk '{print $3}')
    cell=$(echo ${i} | rev | cut -f 1 -d/ | rev)
    echo -e "${cell%_f2q30_pmd.bam}\t${frac}" >> $outdir/qc_metrics/frac_open.txt
done
