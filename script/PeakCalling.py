## Peak calling
# input picard bam file list
# merge bam
# call peak
import os
import config

def merge(bamlist, outdir):
	merged_bam=outdir+'/aggregate/f2q30_merged.bam'
	cmd = "samtools merge -b %s %s" % (bamlist, merged_bam)
	
	os.system(cmd)

def mpicard(outdir, picard):
	wkdir=outdir+'/aggregate/'
	logdir=outdir+'/logs/mpicard/'
	inbam=wkdir+'f2q30_merged.bam'
	outbam=wkdir+'f2q30_merged_pmd.bam'
	outmet=logdir+'f2q30_merged_pmd.out'
	outlog=logdir+'mpicard.log'

	cmd = "java -jar -Xmx4g  %s MarkDuplicates " % picard
	cmd += "INPUT=%s OUTPUT=%s METRICS_FILE=%s " % (inbam, outbam, outmet)
	cmd += "REMOVE_DUPLICATES=true ASSUME_SORTED=true 2>%s" % outlog

	os.system(cmd)

def macs2(outdir,gsize):
	wkdir=outdir+'/aggregate/'
	inbam=wkdir+'f2q30_merged_pmd.bam'
	outlog=outdir+'/logs/macs2/aggregated_scATAC_macs2.log'

	cmd = "macs2 callpeak -t %s " % inbam
	cmd += "-g %s -f BAM -q 0.01 --nomodel " % gsize
	cmd += "--shift -100 --extsize 200 --keep-dup all -B --SPMR " 
	cmd += "--outdir %s -n aggregated_scATAC 2>%s" % (wkdir, outlog)

	os.system(cmd)

def peakcalling(bamlsit, outdir):
	conf = config.conf()
	merge(bamlsit, outdir)
	mpicard(outdir, conf.picard)
	macs2(outdir, conf.gsize)
