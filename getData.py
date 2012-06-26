#!/usr/bin/python

import tables
import numpy as np

def getTimestepTable(h5file):

	# get the number of output timesteps which contain nodeData
	tsteps = 0
	for output in h5file.root.Outputs:
		if output.nodeData._v_nchildren > 0:
			tsteps += 1
	# Get the list of times and redshifts
	# 0: i, index in the output group loop (starts with 0)
	# 1: time since big bang (Gyr)
	# 2: scale factor
	# 3: redshift
	outputTime = np.zeros((tsteps,4))
	i = 0			# index in the output group loop
	j = 0 			# index in the time table
	for output in h5file.root.Outputs:
		# Only use timesteps which contain nodeData
		# (earliest timesteps may not have nodeData)
		if output.nodeData._v_nchildren > 0:
			outputTime[j,0] = i
			outputTime[j,1] = output._v_attrs.outputTime
			outputTime[j,2] = output._v_attrs.outputExpansionFactor
			outputTime[j,3] = 1.0/outputTime[j,2]-1.0
			j += 1
		i += 1
	# sort the array so that it is in ascending time since big bang
	outputTime=outputTime[outputTime[:,1].argsort()]
	return outputTime


def getOutput(h5file,tstep):
	i = 0
	for output in h5file.root.Outputs:
		if i == tstep:
			break
		i += 1
	return output.nodeData
