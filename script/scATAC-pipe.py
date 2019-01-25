import argparse
import os
from multiprocessing import Pool

from Mapping import mapping
from PeakCalling import peakcalling
from CountMatrix import count, generate_cm
from BasicQC import basicQC
import config
from utils import Readlist, Bamlist


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='scATAC-pipe')
    parser.add_argument('--list', '-l', type=str, 
        help='list of input fastq, name_r1.fq(.gz) and name_r2.fq(.gz)') 
    parser.add_argument('--outdir', '-o', type=str, default='output/', 
        help='Output path')
    parser.add_argument('--thread', '-n', type=int, default=1, 
        help='Number of available processors')

    args = parser.parse_args()
    outdir = args.outdir
    thread = args.thread
    filelist = args.list

    samples = Readlist(filelist) # dict
    
    os.system('mkdir '+ outdir)
    os.system('mkdir '+ outdir + '/logs')
    
    ## Mapping    
    os.system('mkdir '+ outdir + '/logs/cutadapt')
    os.system('mkdir '+ outdir + '/logs/hisat2')
    os.system('mkdir '+ outdir + '/logs/spicard')   
    os.system('mkdir ' + outdir + '/trim_fq')
    os.system('mkdir ' + outdir + '/hisat2')
    os.system('mkdir ' + outdir + '/picard')  
    p = Pool(thread)
    map_paras=[tuple(samples[elm]+[outdir]) for elm in samples]
    p.map(mapping, map_paras)

    ## Peak calling
    os.system('mkdir '+ outdir + '/logs/mpicard')
    os.system('mkdir '+ outdir + '/logs/macs2')
    os.system('mkdir '+ outdir + '/aggregate')  
    bamlist=Bamlist(outdir+'/picard/', outdir+'/aggregate/merged_bamlist')
    peakcalling(bamlist,outdir)
    
    # CountMatrix
    os.system('mkdir '+ outdir + '/count')
    p = Pool(thread)
    count_paras=[tuple([elm,outdir]) for elm in samples]
    p.map(count, count_paras)  
    generate_cm(outdir, samples.keys())
    
    # BasicQC
    os.system('mkdir '+ outdir + '/qc_metrics')
    basicQC(outdir)

    
