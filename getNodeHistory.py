#!/usr/bin/python

import tables
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle
import sys

import getData

savedpi = 250
fileformat = 'png'
savepath = './'
inputfile = '/home/markus/Desktop/galacticus_vergleich/galacticus.hdf5_wrongdmmass'
#inputfile = './galacticus.hdf5'

# Give the arrayIndex as argument
aIndex = int(sys.argv[1])

# class which into which we will store the data
# belonging to a node
class NodeClass:
	pass



def findParentIndex(previousNodeData,nodeIndex):
	maxMass = 0
	parentIndex = -1
	for i in range(len(previousNodeData.nodeIndex[:])):
		if previousNodeData.descendentIndex[i] == nodeIndex:
			if previousNodeData.nodeMass[i] > maxMass:
				maxMass = previousNodeData.nodeMass[i]
				parentIndex = i
	return parentIndex

			
		

# open the galacticus file
h5file = tables.openFile(inputfile,"r")

# get the timeTable
timeTable = getData.getTimestepTable(h5file)
# The time table starts at highest redshift
# and goes to redshift = 0. Its length corresponds
# to the number of timesteps in our galacticus file
# Format: nodeDataIndex, time since big bang, scale factor, z

# output the timeTable for debugging purposes
print timeTable
galacticusTimesteps = h5file.root.Outputs._v_nchildren

# Make a list of nodes
nodeHistory = [ NodeClass() ]

# Index of z=0 in our timeTable (end of our simulation)
tIndexEnd = len(timeTable)-1
# Get z=0 Output
nodeData = getData.getOutput(h5file,timeTable[tIndexEnd,0])
# Select the node to trace (at z=0)
# by giving the table index in the nodeData field (starting with 0)
#aIndex = 150
nodeHistory[0].arrayIndex = aIndex
# Get the properties for the selected node at z=0
nodeHistory[0].time = timeTable[tIndexEnd,1] # time in Gyr
nodeHistory[0].nodeIndex = nodeData.nodeIndex[aIndex] # nodeIndex
nodeHistory[0].diskStarFormationRate =  nodeData.diskStarFormationRate[aIndex]
nodeHistory[0].diskGasMass = nodeData.diskGasMass[aIndex]
nodeHistory[0].positionX = nodeData.positionX[aIndex]
nodeHistory[0].positionY = nodeData.positionY[aIndex]
nodeHistory[0].positionZ = nodeData.positionZ[aIndex]
nodeHistory[0].virialRadius = nodeData.nodeVirialRadius[aIndex]
nodeHistory[0].diskScaleLength = nodeData.diskScaleLength[aIndex]
nodeHistory[0].outflowedMass = nodeData.outflowedMass[aIndex]
nodeHistory[0].diskStellarMass = nodeData.diskStellarMass[aIndex]
nodeHistory[0].diskGasMetals = nodeData.diskGasMetals[aIndex]
nodeHistory[0].nodeMass = nodeData.nodeMass[aIndex]
nodeHistory[0].spheroidGasMass = nodeData.spheroidGasMass[aIndex]
nodeHistory[0].spheroidStarFormationRate = nodeData.spheroidStarFormationRate[aIndex]
nodeHistory[0].spheroidStellarMass = nodeData.spheroidStellarMass[aIndex]
nodeHistory[0].spheroidScaleLength = nodeData.spheroidScaleLength[aIndex]
print 'Getting the history for node ', nodeHistory[0].nodeIndex

# Trace the halo backwards through time
# increasing nodeHistory index means decreasing time since big bang
nodeHistoryIndex=range(1,len(timeTable))
for i in nodeHistoryIndex:
	print 'Getting progenitor node Data at timestep ', galacticusTimesteps-i
	# get the dataset for the right time:
	nodeData = getData.getOutput(h5file,timeTable[len(timeTable)-1-i,0])
	# check if the node is present at previous timestep, and if not
	# break the loop
	aIndex = findParentIndex(nodeData,nodeHistory[i-1].nodeIndex)
	if aIndex == -1:
		print 'No progenitor node found at timestep ', galacticusTimesteps-i
		print 'Stopping node history at time ', timeTable[len(timeTable)-i,1]
		print '(z = ', timeTable[len(timeTable)-i,3],')'
		break
	# If node is present at previous timestep add it to nodeHistory
	nodeHistory.append(NodeClass()) # add a new entry to nodeHistory
	nodeHistory[i].arrayIndex = aIndex
	nodeHistory[i].time = timeTable[len(timeTable)-1-i,1] 
	nodeHistory[i].nodeIndex = nodeData.nodeIndex[aIndex]
	# just a check in order we do something stupid
	nodeHistory[i].descendentIndex = nodeData.descendentIndex[aIndex]
	if nodeHistory[i].descendentIndex != nodeHistory[i-1].nodeIndex:
		print 'Attention, ids dont work as expected'
	nodeHistory[i].diskStarFormationRate = nodeData.diskStarFormationRate[aIndex]
	nodeHistory[i].diskGasMass = nodeData.diskGasMass[aIndex]
	nodeHistory[i].positionX = nodeData.positionX[aIndex]
	nodeHistory[i].positionY = nodeData.positionY[aIndex]
	nodeHistory[i].positionZ = nodeData.positionZ[aIndex]
	nodeHistory[i].outflowedMass = nodeData.outflowedMass[aIndex]
	nodeHistory[i].diskStellarMass = nodeData.diskStellarMass[aIndex]
	nodeHistory[i].diskGasMetals = nodeData.diskGasMetals[aIndex]
	nodeHistory[i].nodeMass = nodeData.nodeMass[aIndex]
	nodeHistory[i].virialRadius = nodeData.nodeVirialRadius[aIndex]
	nodeHistory[i].diskScaleLength = nodeData.diskScaleLength[aIndex]
	nodeHistory[i].spheroidGasMass = nodeData.spheroidGasMass[aIndex]
	nodeHistory[i].spheroidStarFormationRate = nodeData.spheroidStarFormationRate[aIndex]
	nodeHistory[i].spheroidStellarMass = nodeData.spheroidStellarMass[aIndex]
	nodeHistory[i].spheroidScaleLength = nodeData.spheroidScaleLength[aIndex]

h5file.close()

# write nodeHistory to disk
outputFile = open('nodeHistory_'+sys.argv[1]+'.pkl','wb')
pickle.dump(nodeHistory,outputFile)
outputFile.close()

# write timeTable to disk
outputFile = open('timeTable.pkl','wb')
pickle.dump(timeTable,outputFile)
outputFile.close()


