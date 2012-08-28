#!/usr/bin/python

import sys
import tables
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import getData

savedpi = 250
fileformat = 'png'
savepath = './'
inputfile = './galacticus.hdf5'
#inputfile = './galacticus.hdf5'


h5file = tables.openFile(inputfile,"r")
timeTable = getData.getTimestepTable(h5file)
#print timeTable


# tStart = 0
# tEnd = len(timeTable)
# set tStart and tEnd to command line parameters
tStart =int(sys.argv[1])
tEnd   =int(sys.argv[2])




# loop over timesteps
for tstep in range(tStart,tEnd):

	# get the data
	nodeData = getData.getOutput(h5file,timeTable[tstep,0])
	# determine the position of the biggest galaxy
	nHalos = len(nodeData.nodeMass)
	maxMass = nodeData.nodeMass[0]
	maxMassIndex = 0
	for j in range(1,nHalos):
		if nodeData.nodeMass[j] > maxMass:
			maxMass = nodeData.nodeMass[j]
			maxMassIndex = j
	bcg_pos_X = nodeData.positionX[j]
	bcg_pos_Y = nodeData.positionY[j]
	bcg_pos_Z = nodeData.positionZ[j]
	print 'Mass of most massive halo: ', maxMass,'.'
	print 'Position of most massive halo: ', bcg_pos_X, bcg_pos_Y,bcg_pos_Z
	print 'Index of most massive halo:', maxMassIndex
	

	

        # get radial distance array
	rad_dist = np.zeros(nHalos)
	for j in range(0,nHalos):
		rad_dist[j] = np.sqrt((nodeData.positionX[j]-bcg_pos_X)**2+
				      (nodeData.positionY[j]-bcg_pos_Y)**2+
				      (nodeData.positionZ[j]-bcg_pos_Z)**2)
	# make the scatter plot
	title = 'Radial Scatter Plot'
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(rad_dist,nodeData.diskStellarMass[:],c='b')
        ax.set_yscale('log')
	ax.set_ylim(1E-7,1E5)
	ax.set_xlim(0.,30)
	ax.set_xlabel('radial distance')
	ax.set_ylabel('disk gas mass')
	ax.set_title(title)
	fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
	title = (savepath+title+' '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
	plt.savefig(title,dpi=savedpi,format=fileformat)

        # make a radially binned plot
	r_length = 1.5
	nbins = 10
	# make the bin arrays
	bin_borders = np.zeros(nbins+1)
	bin_borders[0] = 0.0
	for j in range(1,nbins+1):
		bin_borders[j] = r_length/nbins*j
	value = np.zeros(nbins)
	ngals = np.zeros(nbins)
	# make an array of the bin centers
	bin_centers = np.zeros(nbins)
	for j in range(0,nbins):
		bin_centers[j] = r_length/nbins*(j+0.5)
	# fill the bins
	for j in range(0,nHalos):
		for k in range(0,len(bin_borders)-1):
			if bin_borders[k] <= rad_dist[j] < bin_borders[k+1]:
				value[k] += nodeData.diskStellarMass[j]
				ngals[k] += 1
	mask=~np.isinf(1.0/ngals) # exclude bins where no galaxies are found
	# plot the binned value
	title = 'Radially Binned Profile'
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(bin_centers[mask],value[mask]/ngals[mask],c='b')
        ax.set_yscale('log')
	#ax.set_ylim(1E-7,1E5)
	ax.set_xlim(0.,r_length)
	ax.set_xlabel('radial distance')
	ax.set_ylabel('disk stellar mass')
	ax.set_title(title)
	fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
	title = (savepath+title+' '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
	plt.savefig(title,dpi=savedpi,format=fileformat)

        # morphology density relation
	spirals  = np.zeros(nbins)
	ellipses = np.zeros(nbins)
	ngals = np.zeros(nbins)
	# fill the bins
	for j in range(0,nHalos):
		for k in range(0,len(bin_borders)-1):
			if bin_borders[k] <= rad_dist[j] < bin_borders[k+1]:
				if nodeData.diskStellarMass[j] < nodeData.spheroidStellarMass[j]:
					ellipses[k] += 1
				if nodeData.diskStellarMass[j] > nodeData.spheroidStellarMass[j]:
					spirals[k] += 1
				ngals[k] += 1
        # make a plot of the quantities
	title = 'Morphology Density Relation'
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(bin_centers[mask],spirals[mask]/ngals[mask],c='b',label="spirals")
	ax.plot(bin_centers[mask],ellipses[mask]/ngals[mask],c='r',label="ellipses")
        #ax.set_yscale('log')
	#ax.set_ylim(1E-7,1E5)
	ax.set_xlim(0.,r_length)
	ax.set_xlabel('radial distance (Mpc)')
	ax.set_ylabel('number fraction')
	ax.legend()
	ax.set_title(title)
	fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
	title = (savepath+title+' '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
	plt.savefig(title,dpi=savedpi,format=fileformat)

	print 'Info on the Morphology Density Relation:'
	print 'Radial Bin Centers:'
	print bin_centers
	print 'Number of Galaxies within the bins'
	print ngals
	print 'Number of Spiral galaxies:'
	print spirals
	print 'Number of Elliptical galaxies:'
	print ellipses



h5file.close()    
