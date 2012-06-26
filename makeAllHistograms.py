#!/usr/bin/python

import os

tStart=42
tEnd= 197
for tstep in range(tStart,tEnd):
	command = 'python plotHistograms.py '+str(tstep)+' '+str(tstep+1)
	print command
	os.system(command)

print 'finished with all the plots'
