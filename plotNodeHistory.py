#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Rectangle
import pickle
import tables
import os
import sys

import getData

savedpi = 125
fileformat = 'pdf'
savepath = '/home/markus/Desktop/galacticus_auswertung/nodeHistory/'
#inputfile = '/media/daten/transfer/galacticus.hdf5'
inputfile = '/home/markus/Desktop/galacticus_vergleich/galacticus.hdf5_wrongdmmass'

# For converting the lengths (check if also the masses)
# to comoving (instead of comoving/h) we need the hubble
# parameter
h = 0.7

h5file = tables.openFile(inputfile,"r")

# Get new timetable
#timeTable = getData.getTimestepTable(h5file)
#print timeTable

# to save time, read timetable from file
timeTableFile = open('timeTable.pkl','rb')
timeTable = pickle.load(timeTableFile)
timeTableFile.close()



class NodeClass:
	pass

# function needed to format the third yaxis
# in our plots
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.itervalues():
        sp.set_visible(False)


# load the halo data written by getNodeHistory.py
pklFile = open('nodeHistory_'+sys.argv[1]+'.pkl','rb')
nodeHistory = pickle.load(pklFile)
pklFile.close()
# reverse node history so that nodeHistory[0]
# corresponds to the earliest output
nodeHistory.reverse()

# make a directory for the plots
# (if it does not exist yet)
savepath = savepath+'/'+str(nodeHistory[0].nodeIndex)+'/'
if os.path.exists(savepath) == False:
	os.mkdir(savepath)

# get tIndexStart and tIndexEnd from the arguments
tIndexStart = int(sys.argv[2])
tIndexEnd = int(sys.argv[3])

# time index (of the timetable) where we want to start with our plots
# tIndexStart = 0
# tIndex of the z=0 group
# tIndexEnd = len(timeTable)-1


# determine at which time Index the halo starts to contain data
i=0
for i in range(0,len(timeTable)):
	if(timeTable[i,1] == nodeHistory[0].time):
		tIndexNodeDataStart = i
		#print 'First halo data at tIndex ', i
		break
if tIndexNodeDataStart == len(timeTable)-1:
	print 'Attention, halo is only present at z=0?'
	sys.exit(1)
if tIndexNodeDataStart > tIndexEnd:
	print 'Attention, no halo data in selected time range'


# loop over the timesteps from tIndexStart to tIndexEnd
for tIndex in range(tIndexStart,tIndexEnd+1):
	print 'tstep ', tIndex, 'time: ', timeTable[tIndex,1]
	# get the nodeData for tIndex
	nodeData = getData.getOutput(h5file,timeTable[tIndex,0])
	nHalos = len(nodeData.positionX) # number of halos in that timestep
	# ATTENTION: Positions seem to be in Mpc/h
	# ATTENTION: Also check for the masses
	positionX = nodeData.positionX[0:nHalos]/timeTable[tIndex,2]*h
	positionY = nodeData.positionY[0:nHalos]/timeTable[tIndex,2]*h
	positionZ = nodeData.positionZ[0:nHalos]/timeTable[tIndex,2]*h
	
	# Put nodeHistory[tIndex] into plotData values for easier plotting
	if tIndex>=tIndexNodeDataStart:
		# put the data to be plotted into the plotData array
		# the data vector should have length of tIndex-tIndexStart+1
		plotData1 = np.zeros(tIndex-tIndexNodeDataStart+1)
		plotData2 = np.zeros(tIndex-tIndexNodeDataStart+1)
		plotData3 = np.zeros(tIndex-tIndexNodeDataStart+1)
		plotData4 = np.zeros(tIndex-tIndexNodeDataStart+1)
		plotData5 = np.zeros(tIndex-tIndexNodeDataStart+1)
		plotData6 = np.zeros(tIndex-tIndexNodeDataStart+1)
		plotData7 = np.zeros(tIndex-tIndexNodeDataStart+1)
		plotData8 = np.zeros(tIndex-tIndexNodeDataStart+1)
		plotData9 = np.zeros(tIndex-tIndexNodeDataStart+1)
		plotData10 = np.zeros(tIndex-tIndexNodeDataStart+1)
		plotDataPosition = np.zeros((tIndex-tIndexNodeDataStart+1,3))
		for j in range(0,tIndex-tIndexNodeDataStart+1):
			# select the properties to be plotted

			plotData1[j] = nodeHistory[j].diskGasMass
			plotData2[j] = nodeHistory[j].diskStellarMass
			plotData3[j] = nodeHistory[j].outflowedMass
			plotData4[j] = nodeHistory[j].diskStarFormationRate/1E9 # convert Msol/Gyr to Msol/yr
			plotData5[j] = nodeHistory[j].virialRadius*1000 # convert to kpc
			plotData6[j] = nodeHistory[j].diskScaleLength*1000 # convert to kpc
			plotData7[j] = nodeHistory[j].spheroidScaleLength*1000 # convert to kpc
			plotData8[j] = nodeHistory[j].spheroidGasMass
			plotData9[j] = nodeHistory[j].spheroidStarFormationRate/1E9
			plotData10[j] = nodeHistory[j].spheroidStellarMass
			plotDataPosition[j,0] = nodeHistory[j].positionX/timeTable[j+tIndexNodeDataStart,2]*h
			plotDataPosition[j,1] = nodeHistory[j].positionY/timeTable[j+tIndexNodeDataStart,2]*h
			plotDataPosition[j,2] = nodeHistory[j].positionZ/timeTable[j+tIndexNodeDataStart,2]*h
		# check whether we plot quantities at the right time
		if timeTable[tIndex,1] != nodeHistory[tIndex-tIndexNodeDataStart].time:
			print 'Attention, something went wrong with the time indices'


	# make a plot of the halo positions to the left and
	# the time evolution of up to three selected quantities
	# to the right.
	plotFileName = 'Node'	# output file name
	fig = plt.figure(figsize=(17,7)) # sets the aspect ratio of the output file

	ax1 = fig.add_subplot(121, projection='3d')
	# plot all the nodes
	ax1.scatter(positionX,positionY,positionZ,alpha=0.5,s=1.0)
	# plot our traced halo
	if tIndex>=tIndexNodeDataStart:
		# plot the current position of selected nodes as big point
		ax1.scatter([nodeHistory[tIndex-tIndexNodeDataStart].positionX]/timeTable[tIndex,2]*h,
			    [nodeHistory[tIndex-tIndexNodeDataStart].positionY]/timeTable[tIndex,2]*h,
			    [nodeHistory[tIndex-tIndexNodeDataStart].positionZ]/timeTable[tIndex,2]*h
			    ,alpha=0.8,s=40.0,c='r')
		# plot the trajectory of selected nodes up to tIndex
		ax1.plot3D(plotDataPosition[:,0],plotDataPosition[:,1],plotDataPosition[:,2],'r')
	ax1.set_xlabel('Mpc/h (comoving)')
	ax1.set_xlim(0,20)
	ax1.set_ylim(0,20)
	ax1.set_zlim(0,20)

	# plot of the first selected quantity
	ax2 = fig.add_subplot(122)

	if tIndex>=tIndexNodeDataStart:
		p1, = ax2.plot(timeTable[tIndexNodeDataStart:tIndex+1,1],plotData1,'r')
		p2, = ax2.plot(timeTable[tIndexNodeDataStart:tIndex+1,1],plotData2,'y')
		p3, = ax2.plot(timeTable[tIndexNodeDataStart:tIndex+1,1],plotData3,'b')
		p8, = ax2.plot(timeTable[tIndexNodeDataStart:tIndex+1,1],plotData8,'r--')
		p10, = ax2.plot(timeTable[tIndexNodeDataStart:tIndex+1,1],plotData10,'y--')
	ax2.set_xlim(0,14)
	ax2.set_ylim(1E4,1E14)
	ax2.set_yscale('log')
	ax2.set_xlabel('time since big bang (Gyr)')
	ax2.set_ylabel(r'mass (M$_\odot$)')

	# plot a second quantity in the same frame used by ax2
	ax3 = ax2.twinx()
	ax3.set_ylim(1E-4,1E2)
	ax3.set_yscale('log')
	ax3.set_xlim(0,14)
	ax3.set_ylabel(r'Star formation rate (M$_\odot$/year)')
	if tIndex>=tIndexNodeDataStart:
		p4, = ax3.plot(timeTable[tIndexNodeDataStart:tIndex+1,1],plotData4,'g')
		p9, = ax3.plot(timeTable[tIndexNodeDataStart:tIndex+1,1],plotData9,'g--')

	# plot a third quantity in the same frame used by ax2
	ax4 = ax2.twinx()
	# move the axis to the right
	ax4.spines["right"].set_position(("axes",1.14))
	make_patch_spines_invisible(ax4)
	ax4.spines["right"].set_visible(True)
	ax4.set_ylim(0.1,1000)
	ax4.set_yscale('log')
	ax4.set_xlim(0,14)
	ax4.set_ylabel(r'length (kpc)')
	if tIndex>=tIndexNodeDataStart:
		p5, = ax4.plot(timeTable[tIndexNodeDataStart:tIndex+1,1],plotData5,'k')
		p6, = ax4.plot(timeTable[tIndexNodeDataStart:tIndex+1,1],plotData6,'k--')
		p7, = ax4.plot(timeTable[tIndexNodeDataStart:tIndex+1,1],plotData7,'k-.')

	# dummy plots so that the legend can be plotted
	if tIndex<tIndexNodeDataStart:
		p1, = ax2.plot([],[],'r')
		p2, = ax2.plot([],[],'y')
		p3, = ax2.plot([],[],'b')
		p4, = ax2.plot([],[],'g')
		p5, = ax2.plot([],[],'k')
		p6, = ax2.plot([],[],'k--')
		p7, = ax2.plot([],[],'k-.')
		p8, = ax2.plot([],[],'r--')
		p9, = ax2.plot([],[],'g--')
		p10, = ax2.plot([],[],'y--')
	# p1 = Rectangle((0, 0), 1, 1, fc="r")
	# p2 = Rectangle((0, 0), 1, 1, fc="y")
	# p3 = Rectangle((0, 0), 1, 1, fc="b")
	# p4 = Rectangle((0, 0), 1, 1, fc="g")
	# p5 = Rectangle((0, 0), 1, 1, fc="k")
	# p6 = Rectangle((0, 0), 1, 1, fc="k")
	# p7 = Rectangle((0, 0), 1, 1, fc="k")
	# p8 = Rectangle((0, 0), 1, 1, fc="r")
	# p9 = Rectangle((0, 0), 1, 1, fc="g")
	# p10 = Rectangle((0, 0), 1, 1, fc="y")
	leg = ax4.legend( [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10],['disk gas mass','disk stellar mass','outflowed mass','disk star formation rate','virial radius','disk scale length','spheorid scale length','spheroid gas mass','spheorid star formation', 'spheorid stellar mass'],loc='lower right',fancybox=True)
	leg.get_frame().set_alpha(0.5)

	fig.subplots_adjust(left=0.0,wspace=0.1)
	fig.text(0.82,0.95,r'z = %.2f'%timeTable[tIndex,3]) # print the halo id up left
	fig.text(0.05,0.91,r'Halo  %i'%nodeHistory[0].nodeIndex,fontsize=18) # print the redshift up right
	plotFileName = (savepath+plotFileName+' '+str(nodeHistory[0].nodeIndex)+' '+str(tIndex).zfill(4)+
			'.'+fileformat).replace(" ","_") # resulting filename
	plt.savefig(plotFileName,dpi=savedpi,format=fileformat)


h5file.close()
