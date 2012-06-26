#!/usr/bin/python

import sys
import tables
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import getData

savedpi = 250
fileformat = 'png'
savepath = './histograms/'
inputfile = '/media/daten/transfer/galacticus.hdf5'
#inputfile = './galacticus.hdf5'


h5file = tables.openFile(inputfile,"r")
timeTable = getData.getTimestepTable(h5file)
#print timeTable


# tStart = 0
# tEnd = len(timeTable)
# set tStart and tEnd to command line parameters
tStart =int(sys.argv[1])
tEnd   =int(sys.argv[2])


# Function used to generate histograms
def makeHistogram(titlestring,data,binspace,ylimits,xlog,ylog,xlabel):
	# Histogram of Disk Gas Masses
	title = titlestring
	fig = plt.figure()
	ax = fig.add_subplot(111)
	if ylog == 'log':
		cax = ax.hist(data,bins=binspace,log=True,histtype='bar',alpha=0.5,color='gray')
	else:
		cax = ax.hist(data,bins=binspace,log=False,histtype='bar',alpha=0.5,color='gray')
	ax.set_ylim(ylimits)
	if xlog == 'log':
		ax.set_xscale('log')
	ax.set_xlabel(xlabel)
	ax.set_ylabel('#')
	ax.set_title(title)
	fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
	title = (savepath+title+' '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
	plt.savefig(title,dpi=savedpi,format=fileformat)


# loop over timesteps
for i in range(tStart,tEnd):

	tstep=i
	nodeData = getData.getOutput(h5file,timeTable[tstep,0])
	makeHistogram('Histogram of Disk Gas Masses',nodeData.diskGasMass[:],
		      10**np.linspace(6,15,25),(0.8,4000),'log','log',r'M$_\odot$')
	makeHistogram('Histogram of Disk Gas Metallicity',nodeData.diskGasMetals[:]
		      /nodeData.diskGasMass[:]/0.02,np.linspace(0,20,40),(0.8,4000)
		      ,'nonlog','log',r'solar abundances')
	makeHistogram('Histogram of Outflowed Metals',nodeData.outflowedMetals[:],
		      10**np.linspace(0,11,40),(0.8,4000),'log','log',r'M$_\odot$')
	makeHistogram('Histogram of Disk Stellar Mass'   ,nodeData.diskStellarMass[:],
		      10**np.linspace(6,15,20),(0.8,4000),'log','log',r'M$_\odot$')
	makeHistogram('Histogram of Virial Radii',nodeData.nodeVirialRadius[:],
		      np.linspace(0,2,40),(0.8,4000),'nonlog','log',r'Mpc')
	makeHistogram('Histogram of Velocity X' ,nodeData.velocityX[:],
		      np.linspace(-4000,4000,40),(0.8,4000),'nonlog','log',r'km/s')
h5file.close()    

# Here follow the single histogram plots
# without using one function for all the histograms
# # Histogram of Disk Gas Masses
# title = 'Histogram of Disk Gas Masses'
# fig = plt.figure()
# ax = fig.add_subplot(111)
# cax = ax.hist(nodeData.diskGasMass[:],bins=10**np.linspace(8, 15, 25),log=True,histtype='bar',alpha=0.5,color='gray')
# #ax.set_yscale('log')
# ax.set_ylim(0.8,4000)
# ax.set_xscale('log')
# ax.set_xlabel('solar masses')
# ax.set_ylabel('#')
# ax.set_title(title)
# fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
# title = (savepath+title+' '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
# plt.savefig(title,dpi=savedpi,format=fileformat)


# # Histogram of Disk Gas Metallicity
# title = 'Histogram of Disk Gas Metallicity'
# fig = plt.figure()
# ax = fig.add_subplot(111)
# cax = ax.hist(nodeData.diskGasMetals[:],bins=np.linspace(0, 20, 20),log=True,histtype='bar',alpha=0.5,color='gray')
# #ax.set_yscale('log')
# ax.set_ylim(0.8,4000)
# ax.set_xscale('log')
# ax.set_xlabel('solar masses')
# ax.set_ylabel('#')
# ax.set_title(title)
# fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
# title = (savepath+title+' '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
# plt.savefig(title,dpi=savedpi,format=fileformat)

# # Histogram of Outflowed Metals
# title = 'Histogram of Outflowed Metals'
# fig = plt.figure()
# ax = fig.add_subplot(111)
# cax = ax.hist(nodeData.outflowedMetals[:],bins=np.linspace(0, 20, 20),log=True,histtype='bar',alpha=0.5,color='gray')
# #ax.set_yscale('log')
# ax.set_ylim(0.8,4000)
# ax.set_xscale('log')
# ax.set_xlabel('solar masses')
# ax.set_ylabel('#')
# ax.set_title(title)
# fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
# title = (savepath+title+' '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
# plt.savefig(title,dpi=savedpi,format=fileformat)

# # Histogram of Disk Stellar Mass
# title = 'Histogram of Disk Stellar Mass'
# fig = plt.figure()
# ax = fig.add_subplot(111)
# cax = ax.hist(nodeData.diskStellarMass[:],bins=np.linspace(0, 20, 20),log=True,histtype='bar',alpha=0.5,color='gray')
# #ax.set_yscale('log')
# ax.set_ylim(0.8,4000)
# ax.set_xscale('log')
# ax.set_xlabel('solar masses')
# ax.set_ylabel('#')
# ax.set_title(title)
# fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
# title = (savepath+title+' '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
# plt.savefig(title,dpi=savedpi,format=fileformat)

# # Histogram of Node Virial Radii
# title = 'Histogram of Node Virial Radii'
# fig = plt.figure()
# ax = fig.add_subplot(111)
# cax = ax.hist(nodeData.nodeVirialRadius[:],bins=np.linspace(0, 20, 20),log=True,histtype='bar',alpha=0.5,color='gray')
# #ax.set_yscale('log')
# ax.set_ylim(0.8,4000)
# ax.set_xscale('log')
# ax.set_xlabel('solar masses')
# ax.set_ylabel('#')
# ax.set_title(title)
# fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
# title = (savepath+title+' '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
# plt.savefig(title,dpi=savedpi,format=fileformat)

# # Histogram of VelocityX
# title = 'Histogram of Velocity X'
# fig = plt.figure()
# ax = fig.add_subplot(111)
# cax = ax.hist(nodeData.velocityX[:],bins=np.linspace(0, 20, 20),log=True,histtype='bar',alpha=0.5,color='gray')
# #ax.set_yscale('log')
# ax.set_ylim(0.8,4000)
# ax.set_xscale('log')
# ax.set_xlabel('solar masses')
# ax.set_ylabel('#')
# ax.set_title(title)
# fig.text(0.82,0.95,r'z = %.2f'%timeTable[tstep,3])
# title = (savepath+title+' '+str(tstep).zfill(4)+'.'+fileformat).replace(" ","_")
# plt.savefig(title,dpi=savedpi,format=fileformat)

