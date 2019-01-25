import os
import sys

def basicQC(outdir):
	script=sys.path[0]
	os.system(script + '/utils/get_dup_level.sh ' + outdir)
	os.system(script + '/utils/get_depth_mr.sh ' + outdir)
	os.system(script + '/utils/get_ufrags_mt.sh ' + outdir)
	os.system(script + '/utils/get_lib_size.sh ' + outdir)
	os.system(script + '/utils/get_frip.sh ' + outdir)
	os.system(script + '/utils/get_frac_open.sh ' + outdir)
