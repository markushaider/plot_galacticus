#!/usr/bin/python

import tables
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

savedpi = 150
fileformat = 'pdf'
savepath = './'

inputfile = '/media/daten/transfer/galacticus.hdf5'

h5file = tables.openFile(inputfile,'r')

# get the datasets
history = h5file.root.globalHistory
historyTime                  = history.historyTime      # time after big bang
historyExpansion             = history.historyExpansion # scale factor
historyDiskStarFormationRate = history.historyDiskStarFormationRate
historyStarFormationRate     = history.historyStarFormationRate

# calculate the redshift
redshift = np.zeros(len(historyExpansion))
redshift = 1.0/historyExpansion[:]-1.0

# plot the disk star formation history versus time
title = 'Disk Star Formation Rate History'
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(historyTime,historyDiskStarFormationRate[:]*1E-9)
ax.set_xlabel('Time since big bang (Gyr)')
ax.set_ylabel(r'Comoving disk star formation rate density (M$_\odot$/yr/Mpc$^{-3}$)')
ax.set_title(title)
plt.savefig(savepath+title+'.'+fileformat,dpi=savedpi,format=fileformat)

# plot the disk star formation history versus z
title = 'Disk Star Formation Rate History'
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(redshift,historyDiskStarFormationRate[:]*1E-9)
ax.set_xlabel('Redshift')
ax.set_ylabel(r'Comoving disk star formation rate density (M$_\odot$/yr/Mpc$^{-3}$)')
ax.set_title(title)
plt.savefig(savepath+title+' z.'+fileformat,dpi=savedpi,format=fileformat)

# plot the star formation rate history versus time
title = 'Star Formation Rate History'
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(historyTime,historyStarFormationRate[:]*1E-9)
ax.set_xlabel('Time since big bang (Gyr)')
ax.set_ylabel(r'Comoving star formation rate density (M$_\odot$/yr/Mpc$^{-3}$)')
ax.set_title(title)
plt.savefig(savepath+title+'.'+fileformat,dpi=savedpi,format=fileformat)

# plot the star formation rate history versus redshift
title = 'Star Formation Rate History'
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(redshift,historyStarFormationRate[:]*1E-9)
ax.set_xlabel('Redshift')
ax.set_ylabel(r'Comoving star formation rate density (M$_\odot$/yr/Mpc$^{-3}$)')
ax.set_title(title)
plt.savefig(savepath+title+' z.'+fileformat,dpi=savedpi,format=fileformat)

h5file.close()