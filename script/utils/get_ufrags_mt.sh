#!/bin/bash

outdir=$1

echo -e "cell\tuniq_frags" > $outdir/qc_metrics/uniq_nuc_frags.txt
echo -e "cell\tmt_content" > $outdir/qc_metrics/mt_content.txt

for i in $outdir/picard/*.bam; do
    cell=$(echo ${i} | rev | cut -f 1 -d/ | rev)
    tread=$(samtools idxstats ${i} | addCols stdin | awk '{print $3}')
    mt=$(samtools idxstats ${i} | grep chrM | awk '{print $3}')
    nread=$(calc ${tread}-${mt} | awk '{print $3}')
    nfrag=$(calc ${nread}/2 | awk '{print $3}')
    p=$(calc ${mt}/${tread} | awk '{print $3}')
    echo -e "${cell%_f2q30_pmd.bam}\t${nfrag}" >> $outdir/qc_metrics/uniq_nuc_frags.txt
    echo -e "${cell%_f2q30_pmd.bam}\t${p}" >> $outdir/qc_metrics/mt_content.txt
done
