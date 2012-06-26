#!/usr/bin/python

import os
import sys

nodeArrayIndex = sys.argv[1]

command = 'python getNodeHistory.py '+nodeArrayIndex
print command
os.system(command)

tStart=174
tEnd= 175
for tstep in range(tStart,tEnd):
	command = 'python plotNodeHistory.py '+nodeArrayIndex+' '+str(tstep)+' '+str(tstep)
	print command
	os.system(command)

print 'finished with all the plots'
