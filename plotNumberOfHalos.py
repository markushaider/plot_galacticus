#!/usr/bin/python

import sys
import tables
import numpy as np
import matplotlib.pyplot as plt


savedpi = 250
fileformat = 'png'
savepath = './'
inputfile = './input.hdf5'


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
    title = (savepath+title+fileformat).replace(" ","_")
    plt.savefig(title,dpi=savedpi,format=fileformat)



h5file = tables.openFile(inputfile,"r")
scaleFactor = h5file.root.haloTrees.expansionFactor[:]
nodeMass    = h5file.root.haloTrees.nodeMass[:]

a = 1.0

# get mask of the halos at selected scale factor a
print 'making mask... \n'
scaleFactor = np.ma.masked_equal(scaleFactor,a,copy=True)
mask = np.ma.getmask(scaleFactor)
print 'done making mask... \n'

nodeMass[mask]
makeHistogram('Number of Halos',nodeMass[mask],10**np.linspace(8,16,100),(0.0,10001.),'log','log',r'halo mass M$_\odot$')


h5file.close()
