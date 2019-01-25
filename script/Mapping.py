## Mapping ##
# input fastq1, fastq2
# trim adapter
# mapping
# remove duplicates
# output bam file

import os
import config


def cutadapt(fastq1,fastq2,outdir,adapter1,adapter2):
	wkdir=outdir+'/trim_fq/'
	logdir=outdir+'/logs/cutadapt/'
	sample_name=fastq1.split('/')[-1].split('.')[0][:-3]
	outfq1=wkdir+sample_name+'_r1_trimmed.fq'
	outfq2=wkdir+sample_name+'_r2_trimmed.fq'
	out=logdir+sample_name+'.out'
	err=logdir+sample_name+'.err'

	cmd = "cutadapt -f fastq -m 25 -u -1 -U -1 "
	cmd += "-a %s -A %s " % (adapter1, adapter2)
	cmd += "%s %s " % (fastq1, fastq2)
	cmd += "-o %s -p %s " % (outfq1, outfq2)
	cmd += "1>%s 2>%s" % (out, err)

	os.system(cmd)


def hisat2(sample_name, outdir,index):
	wkdir=outdir+'/hisat2/'
	logdir=outdir+'/logs/hisat2/'
	trimed_fq1=outdir+'/trim_fq/'+sample_name+'_r1_trimmed.fq'
	trimed_fq2=outdir+'/trim_fq/'+sample_name+'_r2_trimmed.fq'
	out_sumary=logdir+sample_name+'_aln_sum.txt'
	tmp=wkdir+sample_name+'_tmp'
	outbam=wkdir+sample_name+'_f2q30.bam'

	cmd = "hisat2 -X 2000 -p 4 --no-spliced-alignment "
	cmd += "-1 %s -2 %s " % (trimed_fq1, trimed_fq2) 
	cmd += "-x %s --summary-file %s " % (index, out_sumary) 
	cmd += "| samtools view -ShuF 4 -f 2 -q 30 - " 
	cmd += "| samtools sort - -T %s -o %s" % (tmp, outbam)

	os.system(cmd)

def spicard(sample_name, outdir,picard):
	wkdir=outdir+'/picard/'
	logdir=outdir+'/logs/spicard/'
	inbam=outdir+'/hisat2/'+sample_name+'_f2q30.bam'
	outbam=wkdir+sample_name+'_f2q30_pmd.bam'
	outmet=logdir+sample_name+'_f2q30_pmd.out'
	outlog=logdir+sample_name+'.log'

	cmd = "java -jar -Xmx4g %s MarkDuplicates " % picard
	cmd += "INPUT=%s OUTPUT=%s METRICS_FILE=%s " % (inbam, outbam, outmet)
	cmd += "REMOVE_DUPLICATES=true ASSUME_SORTED=true 2>%s" % outlog

	os.system(cmd)

def mapping(map_para):
	fastq1, fastq2, outdir = map_para # merged for multiprocessing in py2
	sample_name=fastq1.split('/')[-1].split('.')[0][:-3]
	conf = config.conf()
	cutadapt(fastq1, fastq2, outdir, conf.adapter1, conf.adapter2)
	hisat2(sample_name, outdir, conf.index)
	spicard(sample_name, outdir, conf.picard)
