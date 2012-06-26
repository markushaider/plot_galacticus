#!/usr/bin/python

import tables
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import getData

savedpi = 250
fileformat = 'png'
savepath = './positionPlots/'
inputfile = '/media/daten/transfer/galacticus.hdf5'
#inputfile = './galacticus.hdf5'

h5file = tables.openFile(inputfile,"r")

timeTable = getData.getTimestepTable(h5file)
print timeTable

# In order to plot the physical values we need h
h = 0.72

# Boxsize in Mpc, for easy centering
boxSize = 32

# Calculate the center of mass coordinates
# Get dataset at z=0
nodeData = getData.getOutput(h5file,timeTable[len(timeTable)-1,0])
#print 'Check time at center of mass calculation: ', timeTable[len(timeTable)-1,1]
nHalos = len(nodeData.positionX)
comCoord = np.zeros(3)
for i in range(nHalos):
	comCoord[0] += nodeData.positionX[i]
	comCoord[1] += nodeData.positionY[i]
	comCoord[2] += nodeData.positionZ[i]
comCoord = comCoord/nHalos/timeTable[len(timeTable)-1,2]*h
print 'Coordinates of the center of mass: ', comCoord[0], comCoord[1], comCoord[2]

tStart = 0
tEnd = len(timeTable)
for i in range(tStart,tEnd):
#for i in range(tstep,tstep+1):
	tstep = i
	# get the dataset for time = timeTable[tstep,1]
	nodeData = getData.getOutput(h5file,timeTable[tstep,0])

	nHalos = len(nodeData.positionX)
	# ATTENTION: Positions seem to be in Mpc/h
	# ATTENTION: Also check for the masses
	positionX = nodeData.positionX[0:nHalos]/timeTable[tstep,2]*h
	positionY = nodeData.positionY[0:nHalos]/timeTable[tstep,2]*h
	positionZ = nodeData.positionZ[0:nHalos]/timeTable[tstep,2]*h
	nodeMass  = nodeData.nodeMass[0:nHalos]

	# Plot the whole n-body cube
	title = 'Halo Positions'
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(positionX,positionY,positionZ,alpha=0.5,s=1.0)
	ax.set_xlabel('Mpc (comoving)')
	ax.set_ylabel('Mpc')
	ax.set_zlabel('Mpc')
	ax.set_xlim(0,boxSize)
	ax.set_ylim(0,boxSize)
	ax.set_zlim(0,boxSize)
	ax.set_title(title)
	fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
	title = (savepath+title+' '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
	plt.savefig(title,dpi=savedpi,format=fileformat)

	# Plot the inner 2 Mpc and color code them
	plimit=2.0	       # allowed distance from the center in Mpc
	title = 'Halo Positions'
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	# Select points according to position
	pmask=np.zeros(nHalos)
	pmask=pmask.astype(bool)
	# shift the halos to be centered around the center of mass
	for i in range(nHalos):
		positionX[i] = positionX[i]-comCoord[0]
		positionY[i] = positionY[i]-comCoord[1]
		positionZ[i] = positionZ[i]-comCoord[2]

	for i in range(nHalos):
		pmask[i] = (np.abs(positionX[i]) < plimit and
			    np.abs(positionY[i]) < plimit and
			    np.abs(positionZ[i]) < plimit )
	# Select points according to other criteria
	mask=np.zeros(nHalos)
	mask=mask.astype(bool)
	for i in range(nHalos):
		mask[i] = False
		if(nodeMass[i]<1E11):
			mask[i] = True & pmask[i]
	# Attention: Scatter changes the alpha channel according to
	# the distance to the observing point, if you don't want this,
	# use plot3d instead
	if len(positionX[mask])>0:
		ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			   c='k',s=2.0,edgecolors='none')
       #ax.plot3D(positionX[mask], positionY[mask], positionZ[mask],'.',
       #	   c='k',ms=2.0)
	for i in range(nHalos):
		mask[i] = False
		if(1E11<nodeMass[i]<1E12):
			mask[i] = True & pmask[i]
	if len(positionX[mask])>0:
		ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			   c='k',s=10.0,edgecolors='none')
	for i in range(nHalos):
		mask[i] = False
		if(1E12<nodeMass[i]<1E13):
			mask[i] = True & pmask[i]
	if len(positionX[mask])>0:
		   ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			      c='yellow',s=25.0,edgecolors='none')
	for i in range(nHalos):
		mask[i] = False
		if(1E13<nodeMass[i]):
			mask[i] = True & pmask[i]
	if len(positionX[mask])>0:
		ax.scatter(positionX[mask], positionY[mask], positionZ[mask],
			   c='r',s=50.0,edgecolors='none')
        # Set the axis labels
	ax.set_xlabel('Mpc (comoving)')
	ax.set_ylabel('Mpc')
	ax.set_zlabel('Mpc')
	ax.set_xlim3d(-plimit,plimit)	 
	ax.set_ylim3d(-plimit,plimit)
	ax.set_zlim3d(-plimit,plimit)
	ax.set_title(title)
	fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
	title = (savepath+title+' 2Mpc '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
	plt.savefig(title,dpi=savedpi,format=fileformat)

h5file.close()
