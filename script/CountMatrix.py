import os
from glob import glob
import pandas as pd

def count(para):
    sample_name, outdir = para
    wkdir=outdir+'/count/'
    peak=outdir+'/aggregate/aggregated_scATAC_peaks.narrowPeak'
    bam=outdir+'/picard/'+sample_name+'_f2q30_pmd.bam'
    output=wkdir+sample_name+'.count'

    cmd = "bedtools coverage "
    cmd += "-a %s -b %s | " % (peak, bam)
    cmd += "cut -f 4,11 >%s" % output

    os.system(cmd)

def generate_cm(outdir, samples):
    df=pd.read_table(outdir+'/count/'+samples[0]+'.count', header=None)
    df.columns=['aggregated_peaks',samples[0]]
    for sample in samples[1:]:
        sdf=pd.read_table(outdir+'/count/'+sample+'.count', header=None)
        sdf.columns=['aggregated_peaks',sample]
        df=pd.merge(df,sdf,on='aggregated_peaks')
    df.to_csv(outdir+'/aggregate/count_matrix_aggregate_narrowPeaks.txt', index=None, sep='\t')
    
