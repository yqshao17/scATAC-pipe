from glob import glob

def Readlist(filename):
	filelist=open(filename).readlines()
	filelist=[el.strip() for el in filelist]
	samples=dict()
	for f in filelist:
		aname=f.split('/')[-1].split('.')[0]
		name=aname[:-3]
		samples.setdefault(name, [])
		if aname.endswith('r1'):
			samples[name].insert(0,f)
		elif aname.endswith('r2'):
			samples[name].append(f)
	samples_f=dict()
	for s in samples:
		if len(samples[s])==2:
			samples_f[s]=samples[s] # paired r1 and r2
	return samples_f

def Bamlist(path,outfile):
	bamlist = glob(path+'/*.bam')
	with open(outfile,'w') as output:
		for bam in bamlist:
			output.write(bam+'\n')
	return outfile